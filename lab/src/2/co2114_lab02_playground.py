"""CO2114_LAB02.PY

Use this file to edit your Python code and 
  try the exercises in Lab 02
"""
from agent.environment import *
from agent.things import *
from agent.colors import *

from random import choice, choices

## Write your class definitions here
class BlindDog(Dog, RationalAgent):
    def move(self, direction):
        """ perform move action """
        x,y = self.location
        msg = f"{self}: Moving {direction} from {(x,y)} to "
        match direction:
            case "forward":
                self.location = (x+1, y)
            
        print(msg + f"{self.location}")
        return ((x,y),(self.location))
    
    def eat(self, thing):
        """ eat thing (if possible) """
        if isinstance(thing, Food):
            print(f"{self}: Ate {thing} at {self.location}")
            return True
        return False

    def drink(self, thing):
        """ drink thing (if possible) """
        if isinstance(thing, Water):
            print(f"{str(self)}: Drank {thing} at {self.location}")
            return True
        return False
    

class EnergeticDog(BlindDog):
    def move(self, direction):
        """ perform move action """
        self.direction = direction
        x,y = self.location
        msg = f"{self}: Moving {direction} from {(x,y)} to "
        match direction:
            case "forward":
                self.location = (x+1, y)
            case "backward":
                self.location = (x-1, y)
            case "left":
                self.location = (x, y-1)
            case "right":
                self.location = (x, y+1)
        print(msg + f"{self.location}")
        return ((x,y),(self.location))

class ParkEnvironment(GraphicEnvironment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COLOR_GREEN_GRASS  # export from agent.colors

    def __repr__(self):
        return "🏞️"  # give it a string representation

    def percept(self, agent):
        things = self.things_at(agent.location)
        return things

    def execute_action(self, agent, action):
        """ Executes an action (action, thing/direction)"""
        direction = thing = action[1]  # thing
        match action[0]:  # action string
            case "move":
                if direction in {"forward"}:
                    prev, curr = agent.move(direction)
                if not self.is_inbounds(curr):
                    print(f"{self}: {agent} out of bounds, returning to position {prev}")
                    agent.location = prev
            case "eat":
                if agent.eat(thing):  # success
                    self.delete_thing(thing)  # remove from environment
            case "drink":
                if agent.drink(thing):  # success
                    self.delete_thing(thing)  # remove from environment

    @property
    def is_done(self):
        if len(self.agents) == 0: return True  # if there are no agents
        return not any(
            isinstance(thing, Food) or
                isinstance(thing, Water)
            for thing in self.things)  # or if there isn't any Food or Water

class BigParkEnvironment(ParkEnvironment):
    def execute_action(self, agent, action):
        """ Executes an action (action, thing/direction)"""
        direction = thing = action[1]  # thing
        match action[0]:  # action string
            case "move":
                if direction in {"forward", "backward", "left", "right"}:
                    prev, curr = agent.move(direction)
                if not self.is_inbounds(curr):
                    print(f"{self}: {agent} out of bounds, returning to position {prev}")
                    agent.location = prev
                    self.bumped.add(agent)
            case "eat":
                if agent.eat(thing):  # success
                    self.delete_thing(thing)  # remove from environment
            case "drink":
                if agent.drink(thing):  # success
                    self.delete_thing(thing)  # remove from environment
    def percept(self, agent):
        percepts = super().percept(agent)
        if agent in self.bumped:
            self.bumped.remove(agent)
            percepts.append(Bump())
        return percepts

class ModelBasedEnergeticDog(EnergeticDog, ModelBasedAgent):
    def __init__(self):
        super().__init__()
        self.direction = "forward"
        self.ate = False
    
    def program(self, percepts):
        for thing in percepts:
            if isinstance(thing, Food):
                self.ate = True
                return ("eat", thing)
            if isinstance(thing, Water):
                return ("drink", thing)
        weights = (1, 1, 1, 1)
        directions = ("forward", "backward", "left", "right")
        bump = any(isinstance(thing, Bump) for thing in percepts)
        for i, d in enumerate(directions):
            if d == self.direction:
                weights[i] = 0.1 if bump else 10
        if self.ate:        
            direction = self.direction
            self.ate = False 
        else:
            direction = choices(directions, weights)[0]
        self.direction = direction
        return ("move", direction)
        

## 
def main(graphical=False):
    """ Main method for running script code """
    # write your non-class code here
    def blind_dog_in_park():
        environment = ParkEnvironment(width=10, height=1)
        
        environment.add_thing(Food(), location=(4,0))
        environment.add_thing(Water(), location=(5,0))
        environment.add_thing(Food(), location=(8,0))

        def program(percepts):
            for thing in percepts:
                if isinstance(thing, Food):
                    return ("eat", thing)
                if isinstance(thing, Water):
                    return ("drink", thing)
            return ("move", "forward")

        agent = BlindDog(program)
        environment.add_agent(agent, location=(0, 0))

        environment.run(steps=20, graphical=graphical)
    
    blind_dog_in_park()

    def energetic_dog_in_big_park():


        environment = BigParkEnvironment(width=7, height=7)
        

        # environment.add_thing(Food(), location=(4,3))
        # environment.add_thing(Water(), location=(5,1))
        # environment.add_thing(Food(), location=(8,2))
        for _ in range(3):
            environment.add_thing(
                Food, (
                    choice(range(environment.width)),
                    choice(range(environment.height))))
            environment.add_thing(
                Water, (
                    choice(range(environment.width)),
                    choice(range(environment.height))))

        def program(percepts):
            for thing in percepts:
                if isinstance(thing, Food):
                    return ("eat", thing)
                if isinstance(thing, Water):
                    return ("drink", thing)
            
            direction = choices(
                ("forward", "backward", "left", "right"),
                (0.25, 0.25, 0.25, 0.25))[0]
            return ("move", direction)

        agent = EnergeticDog(program)
        environment.add_agent(agent, location=(0,3))

        environment.run(steps=100, graphical=graphical)
    
    # energetic_dog_in_big_park()


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