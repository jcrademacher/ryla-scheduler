from schedule import Schedule
import numpy as np
import time
import activities

class ScheduleSolver:
    def __init__(self, pop_size, num_legs=12, num_slots=48):
        self.max_iters = 10000
        self.elitist_pct = 5
        self.mate_fitness_pct = 50
        self.init_mutate_prob = 1
        self.init_shuffle_sch_prob = 1/num_legs
        self.init_shuffle_breaks_prob = 1/num_legs
        self.init_break_inj_prob = 1/num_legs

        self.mutate_prob = self.init_mutate_prob
        self.shuffle_sch_prob = self.init_shuffle_sch_prob
        self.shuffle_breaks_prob = self.init_shuffle_breaks_prob
        self.break_inj_prob = self.init_break_inj_prob

        self.exit_status = 0
        

        self.population = np.ndarray((pop_size,),dtype=object)

        for i in range(0,pop_size):
            self.population[i] = Schedule(num_legs=num_legs,num_slots=num_slots)
    
    def exit(self):
        self.exit_status = 1
        print("Exiting...")        

    def crossover(self,p1,p2):
        # method 1: one point crossover: randomly choose an index along s1 and s2,
        #           c1 = concat(s1[:xover],s2[xover:])
        #           c2 = concat(s2[:xover],s2[xover:])      
        p1_flat = np.ravel(p1.sch)
        p2_flat = np.ravel(p2.sch)


        # diff1 = np.abs(np.diff(p1_flat))
        # diff2 = np.abs(np.diff(p2_flat))

        # idx1 = np.arange(0,p1_flat.size-1)[diff1 == 0]
        # idx2 = np.arange(0,p2_flat.size-1)[diff2 == 0]

        # poss_xover = np.intersect1d(idx1,idx2)

        # if poss_xover.size > 0:
        #     xover = np.random.choice(poss_xover)
        # else:
        xover = np.random.randint(0,p1_flat.size)

        # c1 = np.hstack((p1.sch[:,:xover],p2.sch[:,xover:]))
        c1 = np.reshape(np.concatenate((p1_flat[:xover],p2_flat[xover:])),p1.sch.shape)
        # c2 = np.reshape(np.concatenate((p2_flat[:xover],p1_flat[xover:])),p2.sch.shape)

        return Schedule(num_legs=p1.num_legs,num_slots=p1.num_slots,sch=c1)
    
    def mutate(self,sch_obj):
        sch = sch_obj.sch

        # randomly change the activity index in a given slot with probability self.mutate_prob:
        if np.random.rand() < self.mutate_prob:
            raveled = np.ravel(sch)
            raveled[np.random.randint(0,raveled.size)] = np.random.randint(1,sch_obj.acts.size)
            sch = np.reshape(raveled,sch.shape)
        
        if np.random.rand() < self.shuffle_sch_prob:
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            np.random.shuffle(sch[:,rand_leg])

        if np.random.rand() < self.shuffle_breaks_prob:
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            leg_sch = sch[:,rand_leg]
            sch_no_b = leg_sch[leg_sch != 0]
            num_breaks = np.sum(leg_sch == 0)
            sch[:,rand_leg] = np.insert(sch_no_b,np.random.randint(0,sch_no_b.size+1,size=num_breaks),0)

        # if np.random.rand() < self.break_inj_prob:
        #     rand_leg = np.random.randint(0,sch_obj.num_legs)
        #     rand_slot = np.random.randint(0,sch_obj.num_slots)
        #     sch[rand_slot,rand_leg] = 0

        return Schedule(num_legs=sch_obj.num_legs,num_slots=sch_obj.num_slots,sch=sch)

    def solve(self):
        # best = np.sort(self.population)[0]
        # print(f'Fitness: {best.fitness()}\n')
        # return best
        iter = 0

        fitnesses = np.zeros((self.max_iters,))

        while iter < self.max_iters and not self.exit_status:
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
            (travel_sum,overlap_sum,rep_sum,density_sum,period_sum) = self.population[0].fitness_comp

            print(f'Generation: {iter}')
            print('Generation time: %.2f seconds' % (end_time-start_time))
            print(f'Fitness: {fitness}')
            print("Shuffle sch prob: %.2f" % self.shuffle_sch_prob)
            print("Mutate prob: %.2f" % self.mutate_prob)
            print(f"Validity: {rep_sum + overlap_sum + period_sum}\n")

            fitnesses[iter] = fitness

            if iter == 0:
                self.start_fitness = fitness
            
            self.mod_prob(fitness)
           

            if fitness < 5:
                print("Optimum found")
                break

            iter = iter + 1

        return (self.population[0], fitnesses)
    
    def mod_prob(self,fitness):
        pass
        # self.shuffle_sch_prob = (1-fitness/(self.start_fitness+1))**5*self.init_shuffle_sch_prob
        # self.shuffle_breaks_prob = (1-fitness/(self.start_fitness+1))*self.init_shuffle_breaks_prob
        # self.mutate_prob = (fitness/self.start_fitness)**(1/3)*self.init_mutate_prob

