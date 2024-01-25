from agent import things
from numpy import inf

Thing, Agent, RationalAgent, ModelBasedAgent = (
    things.Thing, 
    things.Agent, 
    things.RationalAgent,
    things.ModelBasedAgent)


class MazeRunner(Agent):
    def __repr__(self):
        return "👾"

class GoalBasedAgent(ModelBasedAgent):
    @property
    def at_goal(self):
        NotImplemented

class UtilityBasedAgent(GoalBasedAgent):
    def maximise_utility(self, actions):
        """ calculates maximum utility from list of actions """
        max_u = -inf  # negative infinity
        for action in actions:
            u = self.utility(action)
            if u > max_u:
                max_u = u
                output = action
        return output

    def utility(self, action):
        NotImplemented
