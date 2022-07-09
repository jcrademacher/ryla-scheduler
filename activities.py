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
                preferred_days = [1,2,3,4], 
                group_size = 1, 
                id = 0,
                alias = "",
                start_time = None):
        self.name = name
        self.type = type
        self.zone = zone
        self.length = length
        self.preferred_days = preferred_days
        self.group_size = group_size
        self.id = id
        self.required = required
        self.alias = alias
        self.start_time = start_time

    def __eq__(self,other):
        return self.name == other.name
    
    def __ne__(self,other):
        return self.name != other.name

    def __str__(self):
        if self.alias == "":
            if self.id == 0:    
                return self.name
            else:
                return self.name + " " + str(self.id)
        else:
            return self.alias
    

def get_all_activities():
    activities = [
        Activity("Moby Deck",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Full House",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Lord of the Rings",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Tire Traverse",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Spider Web",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("Christa's Crossing",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Mohawk Walk",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("River Crossing",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("TP Shuffle",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE,preferred_days=[2,3,4]), 
        Activity("Birdie's Nest",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Giant's Finger",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Leighton's Leap",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE), 
        Activity("Wobbly Bob",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE),
        Activity("The Wall",Activity.TYPE_ELEMENT,3,Activity.ZONE_RIDGE,required=True,preferred_days=[3,4],id=1,alias="Gagne's Gateway"),
        Activity("The Wall",Activity.TYPE_ELEMENT,3,Activity.ZONE_RIDGE,required=True,preferred_days=[3,4],id=2,alias="Mancini's Mountain"),
        Activity("Blind Maze",Activity.TYPE_ELEMENT,2,Activity.ZONE_WATERFRONT,preferred_days=[2,3,4],id=1),
        Activity("Blind Maze",Activity.TYPE_ELEMENT,2,Activity.ZONE_CENTRAL,preferred_days=[2,3,4],id=2),
        Activity("See Saw",Activity.TYPE_ELEMENT,2,Activity.ZONE_RIDGE,preferred_days=[2,3],group_size=2),
        Activity("Community Build",Activity.TYPE_PROGRAM,3,Activity.ZONE_CENTRAL,preferred_days=[2,3],group_size=2,required=True),
        Activity("Ethics",Activity.TYPE_PROGRAM,3,required=True,preferred_days=[2,3]),
        Activity("Escape Room",Activity.TYPE_PROGRAM,3,Activity.ZONE_CENTRAL,required=True),
        Activity("Public Speaking",Activity.TYPE_PROGRAM,3,Activity.ZONE_CENTRAL,required=True,preferred_days=[2,3]),
        Activity("Leadership With",Activity.TYPE_PROGRAM,3,Activity.ZONE_WATERFRONT,required=True,preferred_days=[2,3]),
        Activity("Water Program",Activity.TYPE_PROGRAM,4,Activity.ZONE_WATERFRONT,required=True,preferred_days=[2,3],group_size=2),
        Activity("High Ropes",Activity.TYPE_PROGRAM,4,Activity.ZONE_CENTRAL,required=True,preferred_days=[1,2,3],group_size=2),
    ]

    return activities

def get_required_activities():
    return list(filter(lambda x: x.required,get_all_activities()))