"""CO2114_LAB02.PY

Use this file to edit your Python code and 
  try the exercises in Lab 02
"""
from agent.environment import *
from agent.things import *
from agent.colors import *

## Write your class definitions here


## 
def main(graphical=False):
    """ Main method for running script code """
    # write your non-class code here
    NotImplemented


#########################################################
##        DEMONSTRATION CODE FROM TUTORIAL 2           ##
##             ROBOT VACUUM AND DIRTY FLOOR            ##
class DirtyFloor(Environment):
    def __init__(self):
        super().__init__()
        self.floor = [False, True]  # initial state
        
    def __repr__(self):
        return "\u259e"
    @property
    def is_done(self):
        """If no tile is dirty"""
        return not any(self.is_dirty)
    @property
    def is_dirty(self):
        """ State of floor """
        return self.floor
    
    def percept(self, agent):
        """ Tell agent if location is dirty """
        return self.is_dirty[agent.location]

    def execute_action(self, agent, action):
        """ Execute and react to actions by agent """
        match action:
            case "move":
                agent.move()
            case "clean":
                agent.clean()
                self.is_dirty[agent.location] = False


class Vacuum(RationalAgent):
    def __init__(self, program):
        super().__init__(program)
        self.location = 0
    
    def __repr__(self):
        return "🤖"

    def clean(self):  # actuator
        self.performance += 1
        print(f"{self}: cleaning floor at {self.location}")

    def move(self):  # actuator
        self.location += 1
        print(f"{self}: moved to {self.location}")


def run_vacuum_demo():
    """ Demo for simulating vacuum """
    program = lambda percept: "clean" if percept else "move"

    environment = DirtyFloor()  # create environment
    vacuum = Vacuum(program)  # create agent

    environment.add_agent(vacuum)  # add agent to environment
    environment.run(2)  # run simulation for 2 steps


#########################################################
## DO NOT EDIT BELOW THIS LINE                         ##
##             UNLESS YOU KNOW WHAT YOU                ##
##                       ARE DOING                     ##     

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="co2114_lab02")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("-d", "--demo", action="store_true")
    parser.add_argument("-g", "--graphical", action="store_true")
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        run_vacuum_demo()
    else:
        main(args.graphical)