from agent import things

Thing, Agent, ModelBasedAgent = (
    things.Thing, things.Agent, things.ModelBasedAgent)


class MazeRunner(Agent):
    def __repr__(self):
        return "👾"

class GoalBasedAgent(ModelBasedAgent):
    @property
    def at_goal(self):
        NotImplemented

class UtilityBasedAgent(GoalBasedAgent):
    def utility(self, action):
        NotImplemented
