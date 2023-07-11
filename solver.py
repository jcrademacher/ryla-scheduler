from schedule import Schedule
import numpy as np
import time
import activities

class ScheduleSolver:
    def __init__(self, pop_size, num_legs=12, num_slots=48):
        self.max_iters = 1000
        self.elitist_pct = 10
        self.mate_fitness_pct = 50
        self.mutate_prob = 1
        self.shuffle_sch_prob = 1/num_legs
        self.break_inj_prob = 1/4

        self.population = np.ndarray((pop_size,),dtype=object)

        for i in range(0,pop_size):
            self.population[i] = Schedule(num_legs=num_legs,num_slots=num_slots)
    
    def crossover(self,p1,p2):
        # method 1: one point crossover: randomly choose an index along s1 and s2,
        #           c1 = concat(s1[:xover],s2[xover:])
        #           c2 = concat(s2[:xover],s2[xover:])      
        p1_flat = np.ravel(p1.sch)
        p2_flat = np.ravel(p2.sch)


        diff1 = np.abs(np.diff(p1_flat))
        diff2 = np.abs(np.diff(p2_flat))

        idx1 = np.arange(0,p1_flat.size-1)[diff1 == 0]
        idx2 = np.arange(0,p2_flat.size-1)[diff2 == 0]

        poss_xover = np.intersect1d(idx1,idx2)

        if poss_xover.size > 0:
            xover = np.random.choice(poss_xover)
        else:
            xover = np.random.randint(0,p1.sch.size)

        c1 = np.reshape(np.concatenate((p1_flat[:xover],p2_flat[xover:])),p1.sch.shape)
        # c2 = np.reshape(np.concatenate((p2_flat[:xover],p1_flat[xover:])),p2.sch.shape)

        return Schedule(num_legs=p1.num_legs,num_slots=p1.num_slots,sch=c1)
    
    def mutate(self,sch_obj):
        sch = sch_obj.sch
        act_length = sch.shape[1]

        #swap activity columns. During mutation this guarantees that if the original schedule was completely valid, the mutated schedule will also be valid
        # randarr = np.random.randint(0,act_length)
        # adx1 = randarr[0]
        # adx2 = randarr[1]

        # temp = np.array(sch[:,adx1,:])
        # sch[:,adx1,:] = sch[:,adx2,:]
        # sch[:,adx2,:] = temp

        # randomly change the activity index in a given slot with probability self.mutate_prob:
        if np.random.randint(0,1/self.mutate_prob) == 0:
            raveled = np.ravel(sch)
            raveled[np.random.randint(0,raveled.size)] = np.random.randint(0,sch_obj.acts.size)
            sch = np.reshape(raveled,sch.shape)
        
        if np.random.randint(0,1/self.shuffle_sch_prob) == 0:
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            (unq,counts) = np.unique(sch[:,rand_leg],return_counts=True)
            st = np.random.get_state()
            np.random.shuffle(unq)
            np.random.set_state(st)
            np.random.shuffle(counts)
            np.random.seed(None)
            sch[:,rand_leg] = np.repeat(unq,counts)

        if np.random.randint(0,1/self.break_inj_prob) == 0:
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            sch[:,rand_leg] = -1

        return Schedule(num_legs=sch_obj.num_legs,num_slots=sch_obj.num_slots,sch=sch)

    def solve(self):
        # best = np.sort(self.population)[0]
        # print(f'Fitness: {best.fitness()}\n')
        # return best

        found = False
        iter = 0

        fitnesses = np.zeros((self.max_iters,))

        while not found and iter < self.max_iters:
            start_time = time.time()
            ## sort in order of fitness
            self.population = np.sort(self.population)
            new_generation = np.ndarray((self.population.size,),dtype=object)

            elitist_slice = np.floor(self.elitist_pct/100*self.population.size).astype(int)

            # self.elitist_pct % of the population moves into new generation
            for i in range(0,elitist_slice):
                new_generation[i] = self.population[i]

            # mate the top mate_fitness_pct of schedules 100-x % of the population times
            for i in range(elitist_slice,self.population.size):
                # crossover selection:
                xovers = np.random.randint(0,np.floor(self.mate_fitness_pct/100*self.population.size).astype(int),2)
                ind1 = xovers[0]
                ind2 = xovers[1]

                child = self.mutate(self.crossover(self.population[ind1],self.population[ind2]))
                new_generation[i] = child

            self.population = np.array(new_generation)

            end_time = time.time()

            fitness = self.population[0].fitness_val
            print(f'Generation: {iter}')
            print('Generation time: %.2f seconds' % (end_time-start_time))
            print(f'Fitness: {fitness}\n')
            fitnesses[iter] = fitness

            if fitness <= 0:
                print("Optimum found")
                break

            iter = iter + 1

        return (self.population[0], fitnesses)


