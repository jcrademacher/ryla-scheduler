import datetime as dt
import numpy as np
from activities import Activity
import activities

class Schedule:
    def __init__(self, num_legs = 12, num_slots=48, sch=None):
        # master schedule is defined as an array of 30 min time slots, with the number of 
        # rows = total activity time at RYLA (in 30 min timeslot units) and
        # cols = number of activities
        # the final schedule output is an array of leg #'s in each index of the array representing the master schedule
        self.penalty_req = 1
        self.penalty_act_overlap = 2
        self.penalty_act_dup = 2
        self.penalty_act_length = 2    

        self.acts = activities.get_all_activities()

        self.num_legs = num_legs
        self.num_slots = num_slots

        (req_acts, req_acts_idx) = activities.get_required_activities()
        self.req_acts_idx = req_acts_idx

        self.act_lengths = activities.get_activities_mapped(lambda a: a.length)
        self.act_gsizes = activities.get_activities_mapped(lambda a: a.group_size)

        mapper = np.vectorize(lambda a: a.alias)
        unq, unq_idx, unq_cnt = np.unique(mapper(self.acts), return_inverse=True, return_counts=True)
        cnt_mask = unq_cnt > 1
        cnt_idx, = np.nonzero(cnt_mask)
        idx_mask = np.in1d(unq_idx, cnt_idx)
        idx_idx, = np.nonzero(idx_mask)
        srt_idx = np.argsort(unq_idx[idx_mask])
        self.dup_idx = np.split(idx_idx[srt_idx], np.cumsum(unq_cnt[cnt_mask])[:-1])

        if sch is None:
            self.init_schedule()
        else:
            self.sch = sch
        
        self.fitness_val = self.fitness()

    # randomizes the initial schedule
    def init_schedule(self):
        # -1 indicates no activity is scheduled
        self.sch = np.random.randint(-1,self.acts.size,size=(self.num_slots,self.num_legs))
        # acts = self.acts
        
        # # don't need the last iteration since all activities are of length at least 2
        # for slot in range(0,self.sch.shape[0]-1):
        #     avail_acts = self.get_available_activities(slot)

        #     ffunc = np.vectorize(lambda x: slot+x.length <= self.sch.shape[0])
        #     act_idx = avail_acts[ffunc(acts[avail_acts])]

        #     for leg in range(1,self.num_legs+1):
        #         # skips processing of this leg if it is already scheduled in a slot
        #         if leg in self.sch[slot,:]:
        #             continue
                
        #         leg_idx = self.get_leg_activities(leg)
        #         avail_idx = np.setdiff1d(act_idx,leg_idx)

        #         # choose a random activity from the available list
        #         if avail_idx.size != 0:
        #             a = np.random.choice(avail_idx)
        #         else:
        #             a = np.random.choice(act_idx)

        #         activity = acts[a]
        #         # adx = 

        #         # # wait until a random activity is found to be available (including group activities) and the leg has not already done this activity
        #         # while self.sch[slot,a][0:acts[a].group_size].all() or leg in self.sch[:,a]:
        #         #     a = list(dict_acts.keys()).index(random.choice(filtered_activities).name)

        #         self.sch[slot:slot+activity.length,a,0] = leg

        #         if activity.group_size == 2:
        #             other_legs = np.unique(np.concatenate((self.sch[slot,:],self.sch[:,a]),axis=0))
        #             avail_legs = np.setdiff1d(np.array(range(0,self.num_legs+1)),other_legs)

        #             if avail_legs.shape[0] > 0:
        #                 partner_leg = np.random.choice(avail_legs)
        #             else: # find legs who have activites scheduled ALONE, remove them and partner with existing leg
        #                 # first find legs who have activities starting now
        #                 partner_leg = 0

        #             if leg == partner_leg:
        #                 pass

        #             self.sch[slot:slot+activity.length,a,1] = partner_leg

        #         # remove activity index from available activities after scheduling
        #         act_idx = np.setdiff1d(act_idx,np.array(a))
                
        # return self.sch       

    # function checks if leg is double scheduled in same period
    def validate_duplicates(self):
        dups = np.zeros(self.sch)
        for slot in range(0,self.sch.shape[0]):
            trimmed = list(filter(None,self.sch[slot,:]))

    # returns the indices of the activities that are available to schedule from a given slot
    def get_available_activities(self,slot):
        gsize = np.vectorize(lambda x: x.group_size)

        avail_single_acts = np.logical_and(self.sch[slot,:,0]==0,gsize(self.acts)==1)
        avail_double_acts = np.logical_and((self.sch[slot,:] == 0).any(axis=1),gsize(self.acts)==2)

        return np.arange(self.acts.shape[0])[np.logical_or(avail_single_acts,avail_double_acts)]

    
    # returns the indices of the activities that the leg has already done
    def get_leg_activities(self,leg):
        done_idx = np.arange(0,self.acts.shape[0])[(self.sch == leg).any(axis=2).any(axis=0)]

        # inserts the activity that has the same alias but wasn't necessarily scheduled into the done_idx array
        # this is done so that activities that have different locations and can in fact be scheduled simultaneously
        # are NOT rescheduled for the same leg. i.e. ensures that that leg is not repeating multi-location elements
        # such as blind maze 1 and 2 or the wall (gagne's gateway and mancini's mountain)
        for dup in self.dup_idx:
            isect = np.intersect1d(done_idx,dup)
            if isect.size != 0:
                done_idx = np.unique(np.append(done_idx,dup))
        
        return done_idx
    
    # returns a 1D array of the activity indices the leg has scheduled, in the 30 min time slots. Inserts "None" if no activity is scheduled (a break)
    def get_leg_schedule(self,leg):
        act_list = []
        slot = 0
        while slot < self.sch.shape[0]:
            adx = np.arange(0,self.acts.size)[(self.sch[slot,:] == leg).any(axis=1)]

            if adx.size != 0:
                act_list.append(adx[0])
            else:
                act_list.append(None)

            slot = slot + 1
        
        return np.array(act_list)

    # defines the fitness function of the solver
    # this function outputs a real number between 0 and +infinity
    # COMPONENTS:
    # 1. Travel time between activities, defined as the sum of the squared distance between consecutive activity zones
    # 2. Activity requirement. If a required activity is not scheduled, outputs PENALTY_REQ. If it is scheduled, outputs 0
    # 3. Activity overlap. 2 activities cannot be scheduled at the same time
    # 4. Day preferences, defined as the minimum of the squared distance between scheduled day and preferred days vector
    def fitness(self):

        fitness = 0
        sch = self.sch  
        
        req_acts_idx = self.req_acts_idx
        
        travel_times = np.zeros(self.num_legs)
        req_sums = np.zeros(self.num_legs)

        #### activity overlap component
        def act_overlap_operator(arr):
            (arr,counts) = np.unique(arr, return_counts=True)

            unq_acts = arr[arr != -1]
            counts = counts[arr != -1]

            return np.sum((self.act_gsizes[unq_acts]-counts)**2)

        overlap_sum = self.penalty_act_overlap*np.sum(np.apply_along_axis(act_overlap_operator,1,sch))

        #### activity length, repetition, and "consecutiveness" component #### 
        def length_operator(arr):
            leg_sch = arr

            (arr,counts) = np.unique(leg_sch,return_counts=True)
            tval = arr != -1
            arr = arr[tval]
            counts = counts[tval]

            # the number of times a unique activity index appears in the schedule should be exactly equal to its length
            len_rep_sum = np.sum((self.act_lengths[arr]-counts)**2)

            diffs = np.abs(np.diff(leg_sch[leg_sch != -1],axis=0))
            diffs[diffs >= 1] = 1
            diff_sum = np.sum(diffs)

            # intuition here is that the number of unique activities that any given leg is performing should
            # be equal to 1+the number of "transitions" encountered in a leg's schedule
            # a transition is defined as when the activity changes. Thus there should be 1 less transition than unique activities performed
            consec_sum = np.sum((arr.size-(diff_sum+1))**2)

            return len_rep_sum+consec_sum

        len_sum = self.penalty_act_length*np.sum(np.apply_along_axis(length_operator,0,sch))
        
        #### travel time component: ####
        zoner = np.vectorize(lambda a: 0 if (a == -1) else self.acts[a].zone)
        zones = zoner(sch)
        travel_sum = 0 #np.sum(np.diff(zones,axis=0)**2)

        #### activity repetition component 
        # def act_rep_operator(arr):
        #     (arr,counts) = np.unique(arr,return_counts=True)
        #     return np.sum((counts-1)**2)
        
        rep_sum = 0#self.penalty_act_dup*np.sum(np.apply_along_axis(act_rep_operator,0,sch))
        # for leg in range(1,self.num_legs+1):
        #     leg_sch = self.get_leg_schedule(leg)
            
        #     #### travel time component: ####
        #     zoner = np.vectorize(lambda a: 0 if (a is None) else self.acts[a].zone)
        #     travel_times[leg-1] = np.sum(np.ediff1d(zoner(leg_sch))**2)

        #     #### requirement component: ####
        #     acts_done = np.unique(leg_sch[leg_sch != np.array(None)])
        #     req_sums[leg-1] = self.penalty_req*np.abs(np.sum(np.isin(req_acts_idx,acts_done))-req_acts_idx.size)

        # #### leg overlap component: ####
        # overlap_sum = 0
        # for slot in range(0,sch.shape[0]):
        #     flattened = np.ravel(sch[slot,:,:])
        #     nonzero = flattened[flattened != 0]
        #     (arr,counts) = np.unique(nonzero,return_counts=True)
        #     overlap_sum = overlap_sum + (arr[counts>1].size)*self.penalty_act_overlap

            #### travel time component #### 
            # indices = np.argsort(flattened) // 2 # integer division by two to get original activity indices
        
        #### schedule density component: ###
        density_sum = (sch[sch==-1].size)**2

        fitness = travel_sum+overlap_sum+len_sum+rep_sum+density_sum

        return fitness

    def __gt__(self, other):
        return self.fitness_val > other.fitness_val
    
    def __lt__(self,other):
        return self.fitness_val < other.fitness_val
    
    def __ge__(self,other):
        return self.fitness_val >= other.fitness_val
    
    def __le__(self,other):
        return self.fitness_val <= other.fitness_val
    
    def __eq__(self,other):
        return self.fitness_val == other.fitness_val
    
    def __ne__(self,other):
        return self.fitness_val != other.fitness_val

    # returns a 1D list of the leg schedule 
    # def get_leg_schedule(self,leg):
    #     leg_sch = np.zeros(self.sch.shape[0])
    #     slot = 0
    #     while slot < self.sch.shape[0]:
    #         slot_sch = self.sch[slot,:]

    # ## adds activity in the specified day/time. If day/time not specified adds activity at earliest gap
    # # returns true if activity was added successfully, returns false if the activity could not be added
    # def add_activity(self,leg,act,start_dt = None):
    #     leg_sch = self.sch[leg]
    #     ## if time or day not specified find next open gap
    #     if start_dt is None:
    #         (index,gap_start,gap_delta) = self.find_gap_after(leg)

    #         while gap_delta < act.duration:
    #             (index,gap_start,gap_delta) = self.find_gap_after(leg,gap_start)

    #         if index < 0:
    #             return False

    #         start_time = leg_sch[index-1].start_dt+leg_sch[index-1].duration

    #         leg_sch.insert(index,act.set_start_dt(start_time))

    #         return True

    # # returns activity index where gap ends, the start datetime, and the time delta associated with that gap
    # # if day and start_time are provided will search for gap after day and time
    # def find_gap_after(self,leg,after_dt = None):
    #     leg_sch = self.sch[leg]

    #     # find next gap
    #     prev_act = None
    #     index = 0
    #     for act in leg_sch:
    #         act_when = act.start_dt
    #         if prev_act is None or (after_dt is not None and act_when < after_dt):
    #             prev_act = act
    #             index += 1
    #             continue
        
    #         # generate datetime objects representing the day and time the activity occurs
    #         prev_act_when = prev_act.start_dt
            
    #         # check for a gap (and statement prevents the gap from lights out --> breakfast on the next day from generating a gap)
    #         if prev_act_when + prev_act.duration < act_when and prev_act.start_dt.day == act.start_dt.day:
    #             return (index,prev_act_when+prev_act.duration,act_when - (prev_act_when+prev_act.duration))

    #         prev_act = act
    #         index += 1

    #     # indicates no gaps found
    #     return (-1,None,None)

    # def validate_all(self):
    #     retval = []
    #     for leg in range(0,self.num_legs):
    #         retval.append(self.validate_leg(leg))

    #     return retval
    
    # ## validation function that checks if there are no open gaps/crossovers/repeated activities in the leg's schedule
    # # return value: a 3-tuple of (list_gaps (type: (datetime,timedelta)), list_crossovers (type: (Activity1, Activity2)), list_rep (type: (Activity1, Activity1)))
    # def validate_leg(self,leg):
    #     leg_sch = self.sch[leg]

    #     running_act = []

    #     list_gaps = []
    #     list_crossovers = []
    #     list_rep = []
        
    #     # find gaps and crossovers
    #     prev_act = None
    #     for act in leg_sch:
    #         if prev_act is None:
    #             prev_act = act
    #             continue
            
    #         # generate datetime objects representing the day and time the activity occurs
    #         prev_act_when = dt.datetime.combine(self.date+dt.timedelta(days=prev_act.day),prev_act.start_time)
    #         act_when = dt.datetime.combine(self.date+dt.timedelta(days=act.day),act.start_time)
            
    #         # check for a gap (and statement prevents the gap from lights out --> breakfast on the next day from generating a gap)
    #         if prev_act_when + prev_act.duration < act_when and prev_act.day == act.day:
    #             list_gaps.append((prev_act_when+prev_act.duration,act_when - (prev_act_when+prev_act.duration)))
    #         elif prev_act_when + prev_act.duration > act_when and prev_act.day == act.day:
    #             list_crossovers.append((prev_act,act))

    #         prev_act = act

    #     # find repetitions
    #     # filter out all activities that all legs do (TYPE_ALL)
    #     filtered_sch = list(filter(lambda x: x.type != Activity.TYPE_ALL,leg_sch))

    #     for act in filtered_sch:
    #         if act in running_act:
    #             el = (running_act[running_act.index(act)],act)
    #             list_rep.append(el)
    #         else:
    #             running_act.append(act)

    #     return (list_gaps,list_crossovers,list_rep)

    # ## TO BO IMPLEMENTED. Checks that there are no conflicts amongst legs
    # def cross_validate(self):
    #     pass

                
