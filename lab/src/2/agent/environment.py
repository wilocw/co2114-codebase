"""ENVIRONMENT.PY
    This contains code for agent environments
"""
import math
import random
from collections.abc import *

from .engine import App 
from .things import *

from .colors import *


class BaseEnvironment:
    """ Base Environment
            Adapted from AIMI code
    """
    def __repr__(self):
        return self.__class__.__name__
    @property
    def is_done(self):
        NotImplemented
    def step(self):
        NotImplemented
    def run(self, steps=100):
        print(f"{self}: Running for {steps} iterations.")
        for i in range(steps):
            if self.is_done:
                print(f"{self}: Stopping after {i} of {steps} iterations.")
                return
            self.step()

class Environment(BaseEnvironment):
    """ Environment
            An Environment is a BaseEnvironment that has Things and Agents
    """
    def __init__(self):
        self.things = set()
        self.agents = set()
    @property
    def is_done(self):
        return len(self.agents) == 0  # cannot simulate with no agents
    
    def step(self):
        if not self.is_done:
            actions = {agent:agent.program(self.percept(agent))
                for agent in self.agents}  # dictionary of actions by agents
            
            for agent, action in actions.items():
                self.execute_action(agent, action)
            if self.is_done:
                print(f"{self}: Task environment complete. No further actions.")

    def percept(self, agent:Agent):
        NotImplemented
    def execute_action(self, agent:Agent, action):
        NotImplemented

    def add_thing(self, thing:Thing, location=None):
        if not isinstance(thing, Thing):
            print(f"{self}: Tried to add {thing} but its not a Thing.")
            return
    
        if thing in self.things:
            print(f"{self}: Tried and failed to add duplicate {thing}.")
            return
        
        if location:
            thing.location = location
            print(f"{self}: Adding {thing} at {location}")
            self.things.add(thing)

        if isinstance(thing, Agent):
            print(f"{self}: Adding {thing} to list of agents.")
            self.agents.add(thing)
    
    def add_agent(self, agent:Agent, location=None):
        if not isinstance(agent, Agent):
            print(f"{self}: {agent} is not an Agent. Adding as Thing instead.")
        self.add_thing(agent, location)

    def delete_thing(self, thing:Thing):
        if thing not in self.things:
            return
        self.things.remove(thing)
        if isinstance(thing, Agent):
            self.agents.remove(thing)

    def things_at(self, location):
        return [thing for thing in self.things if thing.location == location]
    def __call__(self, location):
        return self.things_at(location)

class XYEnvironment(Environment):
    DEFAULT_BG = COLOR_BLACK

    def __init__(self, width=10, height=10):
        super().__init__()
        self.color = self.DEFAULT_BG
        self.width, self.height = width, height
        self.observers = []
        self.x_start, self.x_end = 0, width
        self.y_start, self.y_end = 0, height

    def things_near(self, location, radius=1):
        # TODO
        raise NotImplementedError
    
    def add_walls(self):
        class Wall(Obstacle):
            pass
    
        if self.width > 2:
            for y in range(self.height):
                self.add_thing(Wall(), (0, y))
                if self.width > 1:
                    self.add_thing(Wall(), (self.width-1, y))
            self.x_start, self.x_end = 1, self.width - 1
        if self.height > 2:
            for x in range(self.width):
                self.add_thing(Wall(), (x, 0))
                if self.height > 1:
                    self.add_thing(Wall(), (x, self.height - 1))
            self.y_start, self.y_end = 1, self.height - 1
    
    def is_valid(self, location):
        if not isinstance(location, Iterable): return False
        if len(location) != 2:  return False
        if any(map(lambda x: not isinstance(x,int), location)): return False
        return True
    
    def is_inbounds(self, location):
        if not self.is_valid(location): return False
        x,y = location
        if not (x >= self.x_start and x < self.x_end): return False
        if not (y >= self.y_start and y < self.y_end): return False
        return True

    def add_thing(self, thing:Thing, location):
        if location is None:
            location = (self.x_start, self.y_start)
        elif self.is_inbounds(location):
            location = tuple(location)  # force tuple to make hashable
        else:
            print(f"Tried and failed to add {thing} to environment")
            return
        super().add_thing(thing, location)

        assert thing in self.things_at(location)

    def add_thing_randomly(self, thing:Thing):
        x = random.randint(self.x_start, self.x_end)
        y = random.randint(self.y_start, self.y_end)
        self.add_thing(thing, (x,y))

class EnvironmentApp(App):
    pass