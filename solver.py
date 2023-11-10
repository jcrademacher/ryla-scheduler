from schedule import Schedule
import numpy as np
import time
import activities

class ScheduleSolver:
    def __init__(self, pop_size, num_legs=12, num_slots=48):
        self.max_iters = 1000
        self.elitist_pct = 5
        self.mutate_pct = 20
        self.mate_fitness_pct = 50 
        self.init_mutate_prob = 0.5
        self.init_shuffle_sch_prob = 0.1
        self.init_swap_acts_prob = 1
        self.init_shuffle_breaks_prob = 0.01
        self.init_break_inj_prob = 0.1

        self.mutate_prob = self.init_mutate_prob
        self.shuffle_sch_prob = self.init_shuffle_sch_prob
        self.swap_acts_prob = self.init_swap_acts_prob
        self.shuffle_breaks_prob = self.init_shuffle_breaks_prob
        self.break_inj_prob = self.init_break_inj_prob

        self.exit_status = 0
        

        self.population = np.ndarray((pop_size,),dtype=object)

        for i in range(0,pop_size):
            self.population[i] = Schedule(num_legs=num_legs,num_slots=num_slots)
    
    def exit(self):
        self.exit_status = 1
        print("Exiting...")   

    # takes raveled schedule
    def get_slice_indices(self,sch_obj):   
          sch = np.ravel(sch_obj.sch,order='F')
          act_lengths = sch_obj.act_lengths

          diff = np.abs(np.diff(sch))
          spt = np.split(sch,np.arange(1,sch.size)[diff!=0])
          lens = np.array(list(map(lambda a: act_lengths[a[0]] if a[0] != 0 else a.size, spt)))
          sizes = np.array(list(map(lambda a: a.size, spt)))

          return (np.cumsum(np.repeat(lens,sizes//lens)),np.cumsum(sizes//lens-1))

    def crossover(self,p1,p2):
        # method 1: one point crossover: randomly choose an index along s1 and s2,
        #           c1 = concat(s1[:xover],s2[xover:])
        #           c2 = concat(s2[:xover],s2[xover:])      
        p1_flat = np.ravel(p1.sch,order='F')
        p2_flat = np.ravel(p2.sch,order='F')


        # diff1 = np.abs(np.diff(p1_flat))
        # diff2 = np.abs(np.diff(p2_flat))

        # spt1 = np.split(p1_flat,np.arange(1,p1_flat.size)[diff1!=0])
        # p1_lens = np.array(list(map(lambda a: p1.act_lengths[a[0]], spt1)))

        # spt2 = np.split(p2_flat,np.arange(1,p2_flat.size)[diff2!=0])
        # p2_lens = np.array(list(map(lambda a: p2.act_lengths[a[0]], spt2)))
        # sizes = np.array(list(map(lambda a: a.size, spt)))
        # consec = np.array(spt,dtype=object)[lens != sizes]

        # p1_lengths = p1.act_lengths[p1_flat]
        # p2_lengths = p2.act_lengths[p2_flat]

        # (p1_unq,p1_idx,p1_cnts) = np.unique(p1_flat,return_index=True,return_counts=True)
        # (p2_unq,p2_idx,p2_cnts) = np.unique(p2_flat,return_index=True,return_counts=True)

        # np.logical_and(p1_cnts == )
        # np.mod(p1.act_lengths[p1_unq],p1_cnts) == 0

        # idx1 = np.arange(1,p1_flat.size)[np.logical_or(diff1 != 0, p1_flat[1:] == 0)]
        # idx2 = np.arange(1,p2_flat.size)[np.logical_or(diff2 != 0, p2_flat[1:] == 0)]

        (split_idx1,reps1) = self.get_slice_indices(p1)#np.union1d(idx1,np.cumsum(p1_lens)-p1_lens[0])
        (split_idx2,reps2) = self.get_slice_indices(p2)#np.union1d(idx2,np.cumsum(p2_lens)-p2_lens[0])

        poss_xover = np.intersect1d(split_idx1,split_idx2)
        xover_size = 1

        if poss_xover.size >= xover_size:
            xovers = np.sort(np.random.choice(poss_xover,size=xover_size,replace=False))
            spt1 = np.split(p1_flat,xovers)
            spt2 = np.split(p2_flat,xovers)
            spt1[1::2] = spt2[1::2]

            c1 = np.reshape(np.concatenate(spt1),p1.sch.shape,order='F')
        else:
            c1 = p1.sch

        # c1 = np.hstack((p1.sch[:,:xover],p2.sch[:,xover:]))
        
        # c2 = np.reshape(np.concatenate((p2_flat[:xover],p1_flat[xover:])),p2.sch.shape)

        return Schedule(num_legs=p1.num_legs,num_slots=p1.num_slots,sch=c1)
    
    def mutate(self,sch_obj):
        sch = sch_obj.sch

        # randomly change the activity index in a given slot with probability self.mutate_prob:
        if np.random.rand() < self.mutate_prob:
            (indices,_) = self.get_slice_indices(sch_obj)

            raveled = np.ravel(sch,order='F')
            rand_idx = np.random.randint(0,indices.size-1)
            idx = indices[rand_idx]

            adx = raveled[idx]
            act_len = sch_obj.act_lengths[adx] if adx != 0 else indices[rand_idx+1]-idx

            act_indices = np.arange(0,sch_obj.acts.size)

            leg_idx = idx // sch_obj.tot_len
            leg_sch = sch[:,leg_idx]
            unq_acts = np.unique(leg_sch)
            # unq_acts = unq_acts[unq_acts != 0]
            len_acts = act_indices[sch_obj.act_lengths==act_len]
            choice_acts = np.setdiff1d(len_acts,unq_acts)
            
            if act_len <= np.max(sch_obj.act_lengths):
                if np.random.rand() < self.break_inj_prob:
                    raveled[idx:idx+act_len] = 0
                    # print("Break inj")
                elif choice_acts.size > 0:
                    raveled[idx:idx+act_len] = np.random.choice(choice_acts)
                    # prin("Choice")
                else:
                    pass
                    #raveled[idx:idx+act_len] = np.random.choice(len_acts)
            else:
                rand_act = np.random.choice(act_indices)
                act_len = sch_obj.act_lengths[rand_act]

                print("Too big")
                raveled[idx:idx+act_len] = rand_act
            
            # rand_leg = np.random.randint(0,sch_obj.num_legs)
            # leg_sch = sch[:,rand_leg]

            # diff = np.abs(np.diff(leg_sch))
            # idx = np.arange(1,leg_sch.size)[diff != 0]

            # rand_idx = np.random.choice(idx)

            # adx = leg_sch[rand_idx]
            # act_length = sch_obj.act_lengths[adx]
            # indices = np.arange(0,sch_obj.acts.size)

            # if adx != 0:
            #     leg_sch[rand_idx:rand_idx+act_length] = np.random.choice(indices[np.logical_and(sch_obj.act_lengths==act_length,indices == adx)])
            
            # sch[:,rand_leg] = leg_sch
            sch = np.reshape(sch,sch_obj.sch.shape,order='F')


        if np.random.rand() < self.swap_acts_prob:
            # (indices,_) = self.get_slice_indices(sch_obj)
            # for i in range(sch_obj.num_legs):
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            leg_sch = sch[:,rand_leg]

            oulaps = sch_obj.get_overlaps(rand_leg)
            # (unq,counts) = np.unique(sch[:,rand_leg],return_counts=True)
            act_lengths = sch_obj.act_lengths
            diff = np.abs(np.diff(leg_sch))

            spt = np.split(leg_sch,np.arange(1,leg_sch.size)[diff!=0])
            oulap_spt = list(map(lambda a: a[0],np.split(oulaps,np.arange(1,leg_sch.size)[diff!=0])))
            choices = np.arange(len(spt))[oulap_spt]

            if choices.size >= 2:
                idxs = np.random.choice(choices,replace=False,size=2)
            elif choices.size == 1:
                idxs = np.array([choices[0], np.random.randint(len(spt))])
            else:
                idxs = np.random.choice(np.arange(len(spt)),replace=False,size=2)

            # lsc = list(map(lambda a: (act_lengths[a[0]],a.size,a[0]), spt))
            # sizes = np.array(list(map(lambda a: a.size, spt)))  
            # comp = np.array(list(map(lambda a: a[0],spt)))

            # idxs =

            temp = spt[idxs[0]]
            spt[idxs[0]] = spt[idxs[1]]
            spt[idxs[1]] = temp

            # st = np.random.get_state()
            # np.random.shuffle(unq)
            # np.random.set_state(st)
            # np.random.shuffle(counts)
            # np.random.seed(None)
            # lens = np.array(list(map(lambda a: a[0], lsc)))
            # sizes = np.array(list(map(lambda a: a[1], lsc)))
            # comps = np.array(list(map(lambda a: a[2], lsc)))

            # to_load = np.repeat(comps,sizes)
            # assert(to_load.size == 55)

            sch[:,rand_leg] = np.concatenate(spt)
        
        if np.random.rand() < self.shuffle_sch_prob:
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            (unq,counts) = np.unique(sch[:,rand_leg],return_counts=True)

            st = np.random.get_state()
            np.random.shuffle(unq)
            np.random.set_state(st)
            np.random.shuffle(counts)
            np.random.seed(None)

            sch[:,rand_leg] = np.repeat(unq,counts)

        if np.random.rand() < self.shuffle_breaks_prob:
            rand_leg = np.random.randint(0,sch_obj.num_legs)
            leg_sch = sch[:,rand_leg]
            (sch_no_b, sch_counts) = np.unique(leg_sch[leg_sch != 0],return_counts=True)
            num_breaks = np.sum(leg_sch == 0)
            insert_idx = np.random.randint(0,sch_no_b.size+1,size=num_breaks)

            inserted_unq = np.insert(sch_no_b,insert_idx,0)
            inserted_cnt = np.insert(sch_counts,insert_idx,1)
            sch[:,rand_leg] = np.repeat(inserted_unq,inserted_cnt)

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
        lookback = 10

        fitnesses = np.zeros((self.max_iters,))
        np.random.seed(None)

        start_time = time.time()

        while iter < self.max_iters and not self.exit_status:
            
            ## sort in order of fitness
            self.population = np.sort(self.population)
            new_generation = np.ndarray((self.population.size,),dtype=object)

            elitist_slice = np.floor(self.elitist_pct/100*self.population.size).astype(int)
            mutate_slice = np.floor(self.mutate_pct/100*self.population.size).astype(int)

            # if not (fitnesses[iter-1] == fitnesses[np.max(iter-lookback,0):iter-1]).all() or iter < 100 :
            # self.elitist_pct % of the population moves into new generation
            for i in range(0,elitist_slice):
                new_generation[i] = self.population[i]
            # else:
            #     print("Nudging")
            #     for i in range(0,elitist_slice):
            #         new_generation[i] = self.population[-i]

            
            for i in range(elitist_slice,elitist_slice+mutate_slice):
                new_generation[i] = self.mutate(self.population[i])
            
            # mate the top mate_fitness_pct of schedules 100-x % of the population times
            for i in range(elitist_slice+mutate_slice,self.population.size):
                # crossover selection:
                xovers = np.random.randint(0,np.floor(self.mate_fitness_pct/100*self.population.size).astype(int),2)
                ind1 = xovers[0]
                ind2 = xovers[1]

                child = self.crossover(self.population[ind1],self.population[ind2])
                
                new_generation[i] = child

            self.population = np.array(new_generation)

            end_time = time.time()

            fitness = self.population[0].fitness_val
            fitness_comp = self.population[0].fitness_comp
            (travel_sum,overlap_sum,rep_sum,density_sum,period_sum,req_sum) = fitness_comp

            print(f'Generation: {iter}')
            print('Elasped time: %.2f seconds' % (end_time-start_time))
            print(f'Fitness: {fitness}')
            # print("Shuffle sch prob: %.2f" % self.shuffle_sch_prob)
            # print("Mutate prob: %.2f" % self.mutate_prob)
            print(f"Repetition Penalty: {rep_sum}")
            print(f"Period Penalty: {period_sum}")
            print(f"Requirement Penalty: {req_sum}")
            print(f"Overlap Penalty: {overlap_sum}\n")

            fitnesses[iter] = fitness

            if iter == 0:
                self.start_fitness = fitness
            
            self.mod_prob(fitness,fitness_comp,iter)
           

            if fitness <= 0:
                print("Optimum found")
                break

            iter = iter + 1

        return (self.population[0], fitnesses)
    
    def mod_prob(self,fitness,fitness_comp,iter):
        (travel_sum,overlap_sum,rep_sum,density_sum,period_sum,req_sum) = fitness_comp
        # if rep_sum == 0 and req_sum == 0:
        #     self.mutate_prob = 0
        #     self.shuffle_sch_prob = 1
        #     self.shuffle_breaks_prob = 1
        # else:
        #     self.mutate_prob = self.init_mutate_prob
        #     self.shuffle_sch_prob = self.init_shuffle_sch_prob
        #     self.shuffle_breaks_prob = self.init_shuffle_breaks_prob
        # self.shuffle_sch_prob = (period_sum+overlap_sum)/fitness*self.init_shuffle_sch_prob
        # self.shuffle_breaks_prob = (period_sum+overlap_sum)/fitness*self.init_shuffle_sch_prob
        # self.mutate_prob = (rep_sum/fitness)*self.init_mutate_prob

