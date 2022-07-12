import datetime as dt
import numpy as np
from activities import Activity

class Schedule:
    def __init__(self, num_legs = 12, num_days = 4):
        # the master schedule 3d matrix. 1st index is LEG, 2nd index is day, 3rd index is activity
        self.sch = []
        self.num_legs = num_legs
        self.num_days = num_days

        reg = Activity("Registration at Tabor",Activity.TYPE_ALL,3,start_time=dt.time(hour=8))
        gtky = Activity("Rules/Trust Falls/Get to Know You",Activity.TYPE_ALL,3,start_time=dt.time(hour=9,minute=30))
        bsa_welcome = Activity("BSA Welcome",Activity.TYPE_ALL,3,start_time=dt.time(hour=11))
        
        flag_ceremony = Activity("Flag Ceremony",Activity.TYPE_ALL,0.5,start_time=dt.time(hour=7,minute=15))
        breakfast = Activity("Breakfast",Activity.TYPE_ALL,2,start_time=dt.time(hour=7,minute=30))
        lunch = Activity("Lunch",Activity.TYPE_ALL,2,start_time=dt.time(hour=12,minute=30),id=0)
        dinner = Activity("Dinner",Activity.TYPE_ALL,2,start_time=dt.time(hour=18,minute=30))
        campsite = Activity("Campsite",Activity.TYPE_ALL,3,start_time=dt.time(hour=20))
        lights_out = Activity("Lights OUT",Activity.TYPE_ALL,1,start_time=dt.time(hour=22))

        interact = Activity("Interact Discussions: Dining Hall",Activity.TYPE_ALL,2,start_time=dt.time(hour=19,minute=30))
        polio_plus = Activity("Polio Plus: Dining Hall",Activity.TYPE_ALL,2,start_time=dt.time(hour=19,minute=30))
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
                self.sch[leg].append([])
                if day == 0:
                    self.sch[leg][day].append(reg)
                    self.sch[leg][day].append(gtky)
                    self.sch[leg][day].append(bsa_welcome)
                    self.sch[leg][day].append(lunch)
                    self.sch[leg][day].append(dinner)
                    self.sch[leg][day].append(interact)
                    self.sch[leg][day].append(campsite)
                    self.sch[leg][day].append(lights_out)

                elif day == 1:
                    self.sch[leg][day].append(flag_ceremony)
                    self.sch[leg][day].append(breakfast)
                    self.sch[leg][day].append(lunch)
                    self.sch[leg][day].append(dinner)
                    self.sch[leg][day].append(polio_plus)
                    self.sch[leg][day].append(campsite)
                    self.sch[leg][day].append(lights_out)

                elif day == 2:
                    self.sch[leg][day].append(flag_ceremony)
                    self.sch[leg][day].append(breakfast)
                    self.sch[leg][day].append(lunch)
                    self.sch[leg][day].append(free_block)
                    self.sch[leg][day].append(dinner)
                    self.sch[leg][day].append(free_block)
                    self.sch[leg][day].append(final_campfire)
                    self.sch[leg][day].append(final_ref)
                    self.sch[leg][day].append(lights_out_last)

                elif day == 3:
                    self.sch[leg][day].append(flag_ceremony)
                    self.sch[leg][day].append(breakfast)
                    self.sch[leg][day].append(lunch_last)
                    self.sch[leg][day].append(solo_prep)
                    self.sch[leg][day].append(solos)
                    self.sch[leg][day].append(pack_up)
                    self.sch[leg][day].append(bbq)

    def validate_all(self):
        retval = []
        for leg in range(0,self.num_legs):
            if not self.validate_leg(leg):
                retval.append(leg)

        return retval
    
    ## validation function that checks if there are no open gaps/crossovers/repeated activities in the schedule
    # return value: a 3-tuple of (list_gaps (type: datetime), list_crossovers (type: (Activity1, Activity2)), list_rep (type: (Activity1, Activity1)))
    def validate_leg(self,leg):
        leg_sch = self.sch[leg]
        # check for repetitions
        leg_sch_filt = leg_sch #list(map(lambda day: list(filter(lambda act: act.type != Activity.TYPE_ALL,day)),leg_sch))
        leg_sch_filt_flat = [act for day in leg_sch_filt for act in day]

        running_act = []
        list_rep = []
        for act in leg_sch_filt_flat:
            if act in running_act:
                el = (running_act[running_act.index(act)],act)
                list_rep.append(el)
            else:
                running_act.append(act)

                
