"""CO2114_LAB02.PY

Use this file to edit your Python code and 
  try the exercises in Lab 02
"""
from agent.environment import *
from agent.things import *
from agent.colors import *

## Write your class definitions here
class BlindDog(Dog, RationalAgent):    
    def move(self, direction):
        x,y = self.location
        msg = f"{self}: Moving {direction} from {(x,y)} to "
        match direction:
            case "forward":
                self.location = (x+1, y)
            
        print(msg + f"{self.location}")

    def eat(self, thing):
        if isinstance(thing, Food):
            print(f"{self}: Ate {thing} at {self.location}")
            return True
        return False

    def drink(self, thing):
        if isinstance(thing, Water):
            print(f"{str(self)}: Drank {thing} at {self.location}")
            return True
        return False


class ParkEnvironment(GraphicEnvironment):
    def __init__(self, width=24, height=18):
        super().__init__(width, height)
        self.color = (80, 240, 100) 

    def __repr__(self):
        return "🏞️"

    def percept(self, agent):
        things = self.things_at(agent.location)
        return things
    
    def execute_action(self, agent, action):
        """ Executes an action (action, thing/direction)"""
        thing = action[1]
        match action[0]:
            case "move":
                match action[1]:
                    case "forward":
                        agent.move("forward")
            case "eat":
                if agent.eat(thing):
                    self.delete_thing(thing)
            case "drink":
                if agent.drink(thing):
                    self.delete_thing(thing)
            
    @property
    def is_done(self):
        if len(self.agents) == 0: return True
        return not any(
            isinstance(thing, Food) or isinstance(thing, Water)
            for thing in self.things)
    
    @classmethod
    def demo(self, graphical=True):
        environment = ParkEnvironment(14,1)

        environment.add_thing(Food(), (6,0))
        environment.add_thing(Water(), (1,0))

        environment.add_thing(Food(), (8,0))
        # environment.add_thing(Water(), (8,5))

        environment.add_thing(Food(), (11, 0))

        # environment.add_walls()

        def program(percepts):
            for p in percepts:
                if isinstance(p, Food):
                    return ("eat", p)
                if isinstance(p, Water):
                    return ("drink", p)
            return ("move", "forward")

        agent = BlindDog(program)
        environment.add_agent(agent, (0,0))

        environment.run(graphical=graphical)

## 
def main(graphical=False):
    """ Main method for running script code """
    # write your non-class code here
    ParkEnvironment.demo(graphical)


#################################
## DO NOT EDIT BELOW THIS LINE ##
##   UNLESS YOU KNOW WHAT YOU  ##
##     ARE DOING               ##
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="co2114_lab02")
    parser.add_argument("-d","--demo", action="store_true")
    parser.add_argument("-g", "--graphical", action="store_true")
    args = parser.parse_args()
    if args.demo:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    else:
        main(args.graphical)