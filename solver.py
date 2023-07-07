from schedule import Schedule
import numpy as np
import activities

class ScheduleSolver:

    

    def __init__(self, schs):
        if not isinstance(schs[0], Schedule):
            raise TypeError("schs must must contain instances of Schedule object")
        
        self.penalty_req = 10
        self.penalty_act_overlap = 100
        self.penalty_act_dup = 100

        self.schs = schs
    
    # defines the fitness function of the solver
    # this function outputs a real number between 0 and +infinity
    # COMPONENTS:
    # 1. Travel time between activities, defined as the sum of the squared distance between consecutive activity zones
    # 2. Activity requirement. If a required activity is not scheduled, outputs PENALTY_REQ. If it is scheduled, outputs 0
    # 3. Activity overlap. 2 activities cannot be scheduled at the same time
    # 3. Day preferences, defined as the minimum of the squared distance between scheduled day and preferred days vector
    def fitness(self, sch_obj):
       
        fitness = 0
        sch = sch_obj.sch  
        (req_acts, req_acts_idx) = activities.get_required_activities()
        
        
        travel_times = np.zeros(sch_obj.num_legs)
        req_sums = np.zeros(sch_obj.num_legs)

        for leg in range(1,sch_obj.num_legs+1):
            leg_sch = sch_obj.get_leg_schedule(leg)
            
            #### travel time component: ####
            zoner = np.vectorize(lambda a: 0 if (a is None) else sch_obj.acts[a].zone)
            travel_times[leg-1] = np.sum(np.ediff1d(zoner(leg_sch))**2)

            #### requirement component: ####
            acts_done = np.unique(leg_sch[leg_sch != np.array(None)])
            req_sums[leg-1] = self.penalty_req*np.abs(np.sum(np.isin(req_acts_idx,acts_done))-req_acts_idx.size)

        #### activity overlap component: ####
        overlap_sum = 0
        for slot in range(0,sch.shape[0]):
            flattened = np.ravel(sch[slot,:,:])
            nonzero = flattened[flattened != 0]
            (arr,counts) = np.unique(nonzero,return_counts=True)
            overlap_sum = overlap_sum + (arr[counts>1].size)*self.penalty_act_overlap


        fitness = np.sum(travel_times)+np.sum(req_sums)+overlap_sum

        return fitness

        
        

