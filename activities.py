import datetime as dt
import copy
import numpy as np

class Activity:
    ZONE_CENTRAL = 0
    ZONE_RIDGE = 1
    ZONE_WATERFRONT = -1

    TYPE_ELEMENT = 0
    TYPE_PROGRAM = 1
    TYPE_ALL = 2

    def __init__(self, 
                name, 
                type, 
                length, 
                zone=None, 
                required = False, 
                preferred_days = [0,1,2,3], 
                group_size = 1, 
                id = 0,
                alias = "",
                start_dt = None):
        self.name = name
        self.type = type
        self.zone = zone
        self.length = length
        self.duration = dt.timedelta(minutes=30*length)
        self.preferred_days = preferred_days
        self.group_size = group_size
        self.id = id
        self.required = required

        if alias:
            self.alias = alias
        else:
            self.alias = name

        self.start_dt = start_dt

    # def __eq__(self,other):
    #     return self.alias == other.alias
    
    # def __ne__(self,other):
    #     return self.alias != other.alias

    def __str__(self):
        if self.alias == "":
            if self.id == 0:    
                return self.name
            else:
                return self.name + " " + str(self.id)
        else:
            return self.alias

    def set_start_dt(self,dt):
        self.start_dt = dt

        return copy.deepcopy(self)

def get_all_activities():
    activities = [
        Activity("Break",Activity.TYPE_ALL,1,Activity.ZONE_CENTRAL),
        Activity("Moby Deck",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Full House",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Lord of the Rings",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Tire Traverse",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Spider Web",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Christa's Crossing",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Mohawk Walk",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("River Crossing",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("TP Shuffle",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE,preferred_days=[1,2,3]), 
        Activity("Birdie's Nest",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Giant's Finger",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Leighton's Leap",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Wobbly Bob",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Gagne's Gateway",Activity.TYPE_ELEMENT,3,Activity.ZONE_RIDGE,required=True,preferred_days=[2,3],id=1,alias="The Wall"),
        # Activity("Mancini's Mountain",Activity.TYPE_ELEMENT,3,Activity.ZONE_RIDGE,required=True,preferred_days=[2,3],id=2,alias="The Wall"),
        Activity("Blind Maze 1",Activity.TYPE_ELEMENT,2,Activity.ZONE_WATERFRONT,preferred_days=[1,2,3],id=1,alias="Blind Maze"),
        # Activity("Blind Maze 2",Activity.TYPE_ELEMENT,2,Activity.ZONE_CENTRAL,preferred_days=[1,2,3],id=2,alias="Blind Maze"),
        Activity("See Saw",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE,preferred_days=[1,2],group_size=2),
        Activity("Community Build",Activity.TYPE_PROGRAM,3,Activity.ZONE_CENTRAL,preferred_days=[1,2],group_size=2,required=True),
        Activity("Ethics",Activity.TYPE_PROGRAM,3,Activity.ZONE_WATERFRONT,required=True,preferred_days=[1,2]),
        Activity("Escape Room",Activity.TYPE_PROGRAM,3,Activity.ZONE_CENTRAL,required=True),
        Activity("Public Speaking",Activity.TYPE_PROGRAM,3,Activity.ZONE_CENTRAL,required=True,preferred_days=[1,2]),
        Activity("Leadership With",Activity.TYPE_PROGRAM,3,Activity.ZONE_WATERFRONT,required=True,preferred_days=[1,2]),
        Activity("Water Program",Activity.TYPE_PROGRAM,4,Activity.ZONE_WATERFRONT,required=True,preferred_days=[1,2],group_size=2),
        Activity("High Ropes",Activity.TYPE_PROGRAM,4,Activity.ZONE_CENTRAL,required=True,preferred_days=[0,1,2],group_size=1)
        # Activity("Break",Activity.TYPE_ALL,1,Activity.ZONE_CENTRAL)
    ]

    return np.array(activities)

def get_dict_activities():
    activities = get_all_activities()

    act_dict = {}

    for act in activities:
        act_dict[act.name] = act;

    return act_dict

def get_required_activities():
    acts = get_all_activities()
    mapper = np.vectorize(lambda act: act.required)
    return (acts[mapper(acts)],np.arange(0,acts.size)[mapper(acts)])

def get_activities_mapped(ufunc):
    acts = get_all_activities()
    mapper = np.vectorize(ufunc)
    return mapper(acts)

# def get_aliased_activities():
#     acts = get_all_activities()
