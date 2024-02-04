from numpy import inf as infinity
from .things import *
from agent.environment import GraphicEnvironment
from search.util import manhattan


PRESET_STATES = {
    '0': {
        "hospitals": [(4,0), (9,3)],
        "houses": [(2,1),(1,3),(8,0),(6,4)],
        "height": 5, 
        "width": 10},
    '1': {
        "houses": [(2,1),(1,3),(8,0),(6,4)],
        "height": 5, 
        "width": 10},
    "empty": None
}



class HospitalOptimiser(Optimiser, UtilityBasedAgent):
    def explore(self, state):
        if not state: return
        print(f"{self}: exploring state\n    {state['hospitals']}")
        for hospital, loc in state["hospitals"].items():
            hospital.location = loc

    def utility(self, state):
        """ calculate distance from each hospital to houses """
        obj = 0
        houses, hospitals = state["houses"], state["hospitals"]
        for house in houses:
            dist_to_nearest = infinity   # very big
            for hospital in hospitals:
                dist = manhattan(
                    houses[house],
                    hospitals[hospital])
                if dist < dist_to_nearest:
                    dist_to_nearest = dist
            obj += dist_to_nearest
        return -obj


class HospitalPlacement(GraphicEnvironment):
    def __init__(self, init=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialise_state(init)

    @property
    def state(self):
        return {
            "hospitals": {
                thing: thing.location
                    for thing in self.things
                        if isinstance(thing, Hospital)},
            "houses": {
                thing: thing.location
                    for thing in self.things
                        if isinstance(thing, House)},
            "bounds": {
                "xmin": 0, "xmax": self.width-1,
                "ymin": 0, "ymax": self.height-1}
        }

    @property
    def neighbours(self):
        neighbours = []
        for i, hospital in enumerate(self.state["hospitals"]):
            location = hospital.location
            for x,y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                proposal = location[0] + x, location[1] + y
                if self.is_inbounds(proposal):
                    candidate = self.state.copy()
                    candidate["hospitals"][hospital] = proposal
                    neighbours.append(candidate)
        return neighbours

    def is_inbounds(self, location):
        if not super().is_inbounds(location):
            return False
        return len(self.things_at(location)) == 0

    def add_agent(self, agent:Agent):
        if not isinstance(agent, Agent):
            raise TypeError(f"{self}: {agent} is not an Agent.")
        self.agents.add(agent)

    def initialise_state(self, state_dict):
        if state_dict is None:
            return
        if "height" in state_dict:
            self.height = state_dict["height"]
        if "width" in state_dict:
            self.width = state_dict["width"]
        self.size = self.width, self.height
        if "hospitals" in state_dict:
            for loc in state_dict["hospitals"]:
                self.add_thing(Hospital(), location=loc)
        for loc in state_dict["houses"]:
            self.add_thing(House(), location=loc)
        

    @property
    def is_done(self):
        if len(self.agents) == 0: return True  # if there are no agents
        return hasattr(self, "success") and self.success

    def percept(self, agent):
        return self.state, self.neighbours

    def execute_action(self, agent, action):
        """ Execute an action """
        command, state = action
        match command:
            case "done":
                if state:
                    agent.explore(state)
                self.success = True
            case "explore":
                agent.explore(state)