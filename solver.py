from schedule import Schedule
import numpy as np
import time
import activities

class ScheduleSolver:
    def __init__(self, pop_size):
        self.max_iters = 100
        self.elitist_pct = 10
        self.mate_fitness_pct = 50

        self.population = np.ndarray((pop_size,),dtype=object)

        for i in range(0,pop_size):
            self.population[i] = Schedule()
    
    def crossover(self,p1,p2):
        # method 1: one point crossover: randomly choose an index along s1 and s2,
        #           c1 = concat(s1[:xover],s2[xover:])
        #           c2 = concat(s2[:xover],s2[xover:])      
        p1_flat = np.ravel(p1.sch)
        p2_flat = np.ravel(p2.sch)

        # chosen such that crossover does not accidentally schedule two legs on an activity that requires only 1
        xover = 2*np.random.randint(0,p1.sch.size // 2)

        c1 = np.reshape(np.concatenate((p1_flat[:xover],p2_flat[xover:])),p1.sch.shape)
        # c2 = np.reshape(np.concatenate((p2_flat[:xover],p1_flat[xover:])),p2.sch.shape)

        return Schedule(num_legs=p1.num_legs,sch=c1)
    
    def mutate(self,sch_obj):
        sch = sch_obj.sch
        act_length = sch.shape[1]

        #swap activity columns. During mutation this guarantees that if the original schedule was completely valid, the mutated schedule will also be valid
        randarr = np.random.randint(0,act_length,2)
        adx1 = randarr[0]
        adx2 = randarr[1]

        temp = np.array(sch[:,adx1,:])
        sch[:,adx1,:] = sch[:,adx2,:]
        sch[:,adx2,:] = temp

        return Schedule(num_legs=sch_obj.num_legs,sch=sch)

    def solve(self):
        found = False
        iter = 0

        while not found and iter < self.max_iters:
            start_time = time.time()
            ## sort in order of fitness
            self.population = np.sort(self.population)
            new_generation = np.ndarray((self.population.size,),dtype=object)

            elitist_slice = np.floor(self.elitist_pct/100*self.population.size).astype(int)

            # x% of the population moves into new generation
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

            print(f'Generation: {iter}')
            print('Generation time: %.1f seconds' % (end_time-start_time))
            print(f'Fitness: {self.population[0].fitness()}\n')

            iter = iter + 1

        return self.population[0]


