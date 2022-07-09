import datetime as dt
import numpy as np
from activities import Activity

class Schedule:
    def __init__(self, num_legs = 12, num_days = 4):
        # the master schedule 3d matrix. 1st index is LEG, 2nd index is day, 3rd index is activity
        self.sch = []

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
        solo_prep = Activity("SOLO PREP",Activity.TYPE_ALL,1,)

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

                elif day == 1:
                    self.sch[leg][day].append(flag_ceremony)
                    self.sch[leg][day].append(breakfast)
                    self.sch[leg][day].append(lunch)
                    self.sch[leg][day].append(dinner)
                    self.sch[leg][day].append(polio_plus)
                    self.sch[leg][day].append(campsite)

                elif day == 2:
                    self.sch[leg]
