"""CO2114_LAB03.PY

Use this file to edit your Python code and 
  try the exercises in Lab 03
"""
from search.things import *
from search.maze import *
from search.util import queue, stack, manhattan

## Write your class definitions here
class BreadthFirstAgent(MazeRunner, GoalBasedAgent):
    def __init__(self):
        super().__init__()
        self.frontier = queue()  # frontier is a FIFO queue
        self.visited = set()  # set of visited nodes

    @property
    def at_goal(self):
        success = self.location.is_goal
        return success

    def move_to(self, tile):
        if tile.is_passable:  # then can move to it
            self.visited.add(self.location)  # add node to visited set
            self.location.visited = True  # tell node its been visited
            self.location = tile  # move to new tile
            print(f"{self}: visiting {tile}")
        return self.at_goal  # success ?

    def program(self, percepts):
        for node in percepts:  # update frontier
            if not node.is_passable:  # not valid
                continue
            if node in self.visited:  # been there
                continue
            if node in self.frontier: # already on the list
                continue
            if node is self.location: # am there
                continue
            self.frontier.push(node)  # otherwise add to frontier
            print(f"{self}: adding {node} to frontier")
        # then move to next in frontier
        node = self.frontier.pop()  # first in queue
        return ("move", node)  # action

class DepthFirstAgent(BreadthFirstAgent):
    def __init__(self):
        super().__init__()
        self.frontier = stack()  # frontier is a LIFO stack


class GreedyInformedAgent(MazeRunner, UtilityBasedAgent):
    def __init__(self, goal):
        super().__init__()
        self.frontier = set()
        self.visited = set()
        self.goal = goal

    @property
    def at_goal(self):
        success = self.location.is_goal
        return self.location.is_goal
    
    def move_to(self, tile):
        if tile.is_passable:
            self.visited.add(self.location)
            self.location.visited = True
            self.location = tile
            utility = self.utility(("move", tile))
            self.frontier.remove(tile)
            print(f"{self}: visiting {tile} with utility={utility}")
        return self.at_goal

    def heuristic(self, node):
        return manhattan(node.location, self.goal.location)
    
    def update_frontier(self, percepts):
        for node in percepts:  # update frontier
            if not node.is_passable:  # not valid
                continue
            if node in self.visited:  # been there
                continue
            if node in self.frontier: # already on the list
                continue
            self.frontier.add(node)  # add to set
            print(f"{self}: adding {node} to frontier")

    def utility(self, action):
        node = action[1]
        return -self.heuristic(node)  # negative distance
    
    def program(self, percepts):
        self.update_frontier(percepts)
        actions = [("move", node) for node in self.frontier]
        action = self.maximise_utility(actions)
        return action # action

class AStarAgent(GreedyInformedAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moved = 0
        self.g_n = dict()

    def move_to(self, node):
        """ """
        self.moved = self.g_n[node]
        return super().move_to(node)

    def update_frontier(self, percepts):
        for node in percepts:  # update frontier
            if not node.is_passable:  # not valid
                continue
            if node in self.visited:  # been there
                continue
            if node in self.frontier: # already on the list
                continue
            self.frontier.add(node)  # add to set
            self.g_n[node] = self.moved + 1
            print(f"{self}: adding {node} to frontier")


    def utility(self, action):
        _, node = action
        return -(self.g_n[node] + self.heuristic(node))

##
def main(graphical=True, maze_preset=0):
    """ Main method for running script code """
    environment, start_loc = generate_preset_maze(maze_preset)
    
    ## Uninformed search
    # environment.add_agent(BreadthFirstAgent(), start_loc)
    # environment.add_agent(DepthFirstAgent(), start_loc)
    
    ## Informed search
    # agent = GreedyInformedAgent(environment.goal)
    agent = AStarAgent(environment.goal)
    environment.add_agent(agent, start_loc)

    environment.run(graphical=graphical, track_agent=True)


#########################################################
##        DEMONSTRATION CODE                           ##
##          Generate maze from preset                  ##
def generate_preset_maze(preset):
    if preset not in PRESET_MAZES:
        opts = list(PRESET_MAZES.keys())
        raise ValueError(
            f"{preset} not a valid preset, cannot create maze\n options:{opts}")
    template = PRESET_MAZES[preset]
    environment = GraphicMaze.from_template(template)
    
    start_point = PRESET_STARTS[preset]
    return environment, start_point

#########################################################
## DO NOT EDIT BELOW THIS LINE                         ##
##             UNLESS YOU KNOW WHAT YOU                ##
##                       ARE DOING                     ##

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="co2114_lab03")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("-d", "--demo", action="store_true")
    parser.add_argument("-g", "--disable_gui", action="store_true")
    parser.add_argument(
        "-m", "--preset",
        type=int, default=0,
        choices=list(PRESET_MAZES.keys())
        )
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        NotImplemented
    else:
        main(not args.disable_gui, args.preset)