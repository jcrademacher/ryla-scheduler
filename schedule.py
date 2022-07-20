import datetime as dt
import numpy as np
from activities import Activity

class Schedule:
    def __init__(self, num_legs = 12, num_days = 4):
        # the master schedule list, activities objects hold day and time information
        self.sch = []
        self.num_legs = num_legs
        self.num_days = num_days

        self.date = dt.datetime(2023,6,1)

        reg = Activity("Registration at Tabor",Activity.TYPE_ALL,3,start_time=dt.time(hour=8))
        gtky = Activity("Rules/Trust Falls/Get to Know You",Activity.TYPE_ALL,3,start_time=dt.time(hour=9,minute=30))
        bsa_welcome = Activity("BSA Welcome",Activity.TYPE_ALL,3,start_time=dt.time(hour=11))
        
        flag_ceremony = Activity("Flag Ceremony",Activity.TYPE_ALL,0.5,start_time=dt.time(hour=7,minute=15))
        breakfast = Activity("Breakfast",Activity.TYPE_ALL,2,start_time=dt.time(hour=7,minute=30))
        lunch = Activity("Lunch",Activity.TYPE_ALL,2,start_time=dt.time(hour=12,minute=30),id=0)
        dinner = Activity("Dinner",Activity.TYPE_ALL,2,start_time=dt.time(hour=18,minute=30))
        campsite = Activity("Campsite",Activity.TYPE_ALL,3,start_time=dt.time(hour=20,minute=30))
        lights_out = Activity("Lights OUT",Activity.TYPE_ALL,1,start_time=dt.time(hour=22))

        interact = Activity("Interact Discussions: Dining Hall",Activity.TYPE_ALL,2,start_time=dt.time(hour=19,minute=30))
        polio_plus = Activity("Polio Plus: Dining Hall",Activity.TYPE_ALL,2,start_time=dt.time(hour=19,minute=30))
        
        skit_prep = Activity("Skit Prep",Activity.TYPE_ALL,2,start_time=dt.time(hour=17,minute=30))
        free_block = Activity("Free Block",Activity.TYPE_ALL,1,start_time=dt.time(hour=19,minute=30))
        final_campfire = Activity("Final Campfire",Activity.TYPE_ALL,3,start_time=dt.time(hour=20))
        final_ref = Activity("Final Reflection",Activity.TYPE_ALL,3,start_time=dt.time(hour=21,minute=30))
        lights_out_last = Activity("Lights OUT",Activity.TYPE_ALL,1,start_time=dt.time(hour=23))

        lunch_last = Activity("Lunch",Activity.TYPE_ALL,2,start_time=dt.time(hour=13),id=1)
        solo_prep = Activity("SOLO PREP",Activity.TYPE_ALL,1,start_time=dt.time(hour=14))
        solos = Activity("SOLOs",Activity.TYPE_ALL,4,start_time=dt.time(hour=14,minute=30))
        pack_up = Activity("Pack Up Camp",Activity.TYPE_ALL,1,start_time=dt.time(hour=16,minute=30))
        bbq = Activity("Final BBQ",Activity.TYPE_ALL,4,start_time=dt.time(hour=17))

        # generate the bare bones required blocks, such as meals, flag ceremony, solos, etc.
        for leg in range(0,num_legs):
            self.sch.append([])
            for day in range(0,num_days):
                if day == 0:
                    self.sch[leg].append(reg.set_day(day))
                    self.sch[leg].append(gtky.set_day(day))
                    self.sch[leg].append(bsa_welcome.set_day(day))
                    self.sch[leg].append(lunch.set_day(day))
                    self.sch[leg].append(dinner.set_day(day))
                    self.sch[leg].append(interact.set_day(day))
                    self.sch[leg].append(campsite.set_day(day))
                    self.sch[leg].append(lights_out.set_day(day))

                elif day == 1:
                    self.sch[leg].append(flag_ceremony.set_day(day))
                    self.sch[leg].append(breakfast.set_day(day))
                    self.sch[leg].append(lunch.set_day(day))
                    self.sch[leg].append(dinner.set_day(day))
                    self.sch[leg].append(polio_plus.set_day(day))
                    self.sch[leg].append(campsite.set_day(day))
                    self.sch[leg].append(lights_out.set_day(day))

                elif day == 2:
                    self.sch[leg].append(flag_ceremony.set_day(day))
                    self.sch[leg].append(breakfast.set_day(day))
                    self.sch[leg].append(lunch.set_day(day))
                    self.sch[leg].append(skit_prep.set_day(day))
                    self.sch[leg].append(dinner.set_day(day))
                    self.sch[leg].append(free_block.set_day(day))
                    self.sch[leg].append(final_campfire.set_day(day))
                    self.sch[leg].append(final_ref.set_day(day))
                    self.sch[leg].append(lights_out_last.set_day(day))

                elif day == 3:
                    self.sch[leg].append(flag_ceremony.set_day(day))
                    self.sch[leg].append(breakfast.set_day(day))
                    self.sch[leg].append(lunch_last.set_day(day))
                    self.sch[leg].append(solo_prep.set_day(day))
                    self.sch[leg].append(solos.set_day(day))
                    self.sch[leg].append(pack_up.set_day(day))
                    self.sch[leg].append(bbq.set_day(day))
    

    def when_activity(self,act):
        return dt.datetime.combine(self.date+dt.timedelta(days=act.day),act.start_time)

    ## adds activity in the specified day/time within activity and also ensures that the addition does not conflict with other legs
    def add_activity(self,leg,act):
        leg_sch = self.sch[leg]
        ## if time or day not specified find next open gap
        if act.start_time is None or act.day is None:
            (index,day,opening_delta) = self.find_earliest_gap(leg)

            start_time = self.when_activity(leg_sch[index-1])
            self.sch[leg].insert(index,act.set_day_time()) ##### UNFINISHED


    # returns activity index where gap ends, and the time delta associated with that gap
    def find_earliest_gap(self,leg):
        leg_sch = self.sch[leg]

        # find next gap
        prev_act = None
        index = 0
        for act in leg_sch:
            if prev_act is None:
                prev_act = act
                index += 1
                continue
            
            # generate datetime objects representing the day and time the activity occurs
            prev_act_when = dt.datetime.combine(self.date+dt.timedelta(days=prev_act.day),prev_act.start_time)
            act_when = dt.datetime.combine(self.date+dt.timedelta(days=act.day),act.start_time)
            
            # check for a gap (and statement prevents the gap from lights out --> breakfast on the next day from generating a gap)
            if prev_act_when + prev_act.duration < act_when and prev_act.day == act.day:
                return (index,act.day,act_when - (prev_act_when+prev_act.duration))

            prev_act = act
            index += 1

    def validate_all(self):
        retval = []
        for leg in range(0,self.num_legs):
            retval.append(self.validate_leg(leg))

        return retval
    
    ## validation function that checks if there are no open gaps/crossovers/repeated activities in the leg's schedule
    # return value: a 3-tuple of (list_gaps (type: (datetime,timedelta)), list_crossovers (type: (Activity1, Activity2)), list_rep (type: (Activity1, Activity1)))
    def validate_leg(self,leg):
        leg_sch = self.sch[leg]

        running_act = []

        list_gaps = []
        list_crossovers = []
        list_rep = []
        
        # find gaps and crossovers
        prev_act = None
        for act in leg_sch:
            if prev_act is None:
                prev_act = act
                continue
            
            # generate datetime objects representing the day and time the activity occurs
            prev_act_when = dt.datetime.combine(self.date+dt.timedelta(days=prev_act.day),prev_act.start_time)
            act_when = dt.datetime.combine(self.date+dt.timedelta(days=act.day),act.start_time)
            
            # check for a gap (and statement prevents the gap from lights out --> breakfast on the next day from generating a gap)
            if prev_act_when + prev_act.duration < act_when and prev_act.day == act.day:
                list_gaps.append((prev_act_when+prev_act.duration,act_when - (prev_act_when+prev_act.duration)))
            elif prev_act_when + prev_act.duration > act_when and prev_act.day == act.day:
                list_crossovers.append((prev_act,act))

            prev_act = act

        # find repetitions
        # filter out all activities that all legs do (TYPE_ALL)
        filtered_sch = list(filter(lambda x: x.type != Activity.TYPE_ALL,leg_sch))

        for act in filtered_sch:
            if act in running_act:
                el = (running_act[running_act.index(act)],act)
                list_rep.append(el)
            else:
                running_act.append(act)

        return (list_gaps,list_crossovers,list_rep)

                
