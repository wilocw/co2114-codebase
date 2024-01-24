"""CO2114_LAB03.PY

Use this file to edit your Python code and 
  try the exercises in Lab 03
"""
from search.things import *
from search.maze import *
from search.util import queue, stack


class BreadthFirstAgent(MazeRunner, GoalBasedAgent):

    def __init__(self):
        super().__init__()
        self.frontier = queue()
        self.visited = set()

    @property
    def at_goal(self):
        success = self.location.is_goal
        return self.location.is_goal

    def move_to(self, tile):
        if tile.is_passable:
            self.visited.add(self.location)
            self.location.visited = True
            self.location = tile
            print(f"{self}: visiting {tile}")
        return self.at_goal

    def program(self, percepts):
        for node in percepts:
            if not node.is_passable:
                continue
            if node in self.visited:
                continue
            if node in self.frontier:
                continue
            if node is self.location:
                continue
            self.frontier.push(node)
            print(f"{self}: adding {node} to frontier")

        node = self.frontier.pop()
        return ("move", node)  #action

class DepthFirstAgent(BreadthFirstAgent):
    def __init__(self):
        super().__init__()
        self.frontier = stack()


def manhattan(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx-ax) + abs(by-ay)

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
            utility = self.utility(("",tile))
            print(f"{self}: visiting {tile} with utility={utility}")
        return self.at_goal
    
    def utility(self, action):
        node = action[1] 
        # maximise utility means minimise heuristic
        return -self.heuristic(node)


    def heuristic(self, node):
        return manhattan(node.location, self.goal.location)

    def update_frontier(self, percepts):
        for node in percepts:
            if not node.is_passable:
                continue
            if node in self.visited:
                continue
            if node in self.frontier:
                continue
            if node is self.location:
                continue
            self.frontier.add(node)
            print(f"{self}: adding {node} to frontier")

    def program(self, percepts):

        self.update_frontier(percepts)

        max_u = -1e100  # very low
        for node in self.frontier:
            action = ("move", node)
            u = self.utility(action)
            if u > max_u:
                max_u = u
                next = node
        self.frontier.remove(next)
        return ("move", next)  #action

class AStarAgent(GreedyInformedAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moved = 0
        self.g_n = dict()

    def move_to(self, node):
        super().move_to(node)
        self.moved = self.g_n[node]
        return self.at_goal

    def update_frontier(self, percepts):
        for node in percepts:
            if not node.is_passable:
                continue
            if node in self.visited:
                continue
            if node in self.frontier:
                continue
            if node is self.location:
                continue
            self.frontier.add(node)
            self.g_n[node] = self.moved + 1
            print(f"{self}: adding {node} to frontier")

    def utility(self, action):
        node = action[1] 
        # maximise utility means minimise heuristic
        astar = self.g_n[node] + self.heuristic(node)
        return -astar


## 
def main(graphical=False, maze_preset=0):
    """ Main method for running script code """
    # write your non-class code here
    template = PRESET_MAZES[maze_preset]
    environment = GraphicMaze.from_template(template)
    
    goal = [tile for tile in environment.maze if tile.is_goal][0]

    # agent = BreadthFirstAgent()
    # agent = DepthFirstAgent()
    # agent = GreedyInformedAgent(goal)
    agent = AStarAgent(goal)
    environment.add_agent(
        agent, 
        location=PRESET_STARTS[maze_preset])

    if graphical:
        environment.run(graphical=graphical, track_agent=True)
    else:
        environment.run(graphical=False)

#########################################################
##        DEMONSTRATION CODE                           ##
##                                                     ##


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
    parser.add_argument("-m", "--preset", type=int, default=0)
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        NotImplemented
    else:
        main(not args.disable_gui, args.preset)