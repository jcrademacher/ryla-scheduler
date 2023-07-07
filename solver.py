from schedule import Schedule
import numpy as np

class ScheduleSolver:
    def __init__(self, sch):
        if not isinstance(sch, Schedule):
            raise TypeError("sch must be an instance of Schedule object")
        
        self.sch = sch
    
    # defines the objective function of the solver
    # this function outputs a real number between 0 and +infinity
    # COMPONENTS:
    # 1. Travel time between activities, defined as the sum of the squared distance between consecutive activity zones
    # 2. Activity requirement. If a required activity is not scheduled, outputs +inf. If it is scheduled, outputs 0
    # 3. Day preferences, defined as the minimum of the squared distance between scheduled day and preferred days vector
    def objective(self):
        # travel time component:
        sum = np.zeros(self.sch.num_legs)

        for leg in range(1,self.sch.num_legs+1):
            slot = 0
            while slot < self.sch.shape[0]:
                
                slot = slot + 1


