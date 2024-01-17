"""ENVIRONMENT.PY
    This contains code for agent environments
"""
import warnings
import math
import random
from collections.abc import *

with warnings.catch_warnings(action="ignore"):
    import pygame

from .engine import App
from .colors import COLOR_BLACK, COLOR_WHITE
from .things import Thing, Agent, Obstacle

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
    def run(self, steps=100, pause_for_user=True):
        if pause_for_user:
            input("Press enter to start simulation")
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
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError(f"{self}: dimensions must be integers")
        if width < 1 or height < 1:
            raise ValueError(f"{self}: dimensions must be greater than zero")
        super().__init__()
        self.color = self.DEFAULT_BG
        self.width, self.height = width, height
        self.observers = []
        self.x_start, self.x_end = 0, width
        self.y_start, self.y_end = 0, height

    def things_near(self, location, radius=1):
        # TODO
        raise NotImplementedError
    
    def _add_wall(self, location):
        class Wall(Obstacle):
            pass
        if all(not isinstance(obj, Obstacle) 
               for obj in self.things_at(location)):
            self.add_thing(Wall(), location)

    def add_walls(self):
        if self.width > 2:
            for y in range(self.height):
                self._add_wall((0, y))
                if self.width > 1:
                    self._add_wall((self.width-1, y))
        if self.height > 2:
            for x in range(self.width):
                self._add_wall((x, 0))
                if self.height > 1:
                    self._add_wall((x, self.height - 1))
            self.y_start, self.y_end = 1, self.height - 1
        if self.width > 2:
            self.x_start, self.x_end = 1, self.width - 1
    
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

class GraphicEnvironment(XYEnvironment):
    def run(self, graphical=True, steps=100, **kwargs):
        if graphical:
            EnvironmentApp(self, steps=steps, **kwargs).run()
        else:
            super().run(steps=steps, **kwargs)

class EnvironmentApp(App):
    """EnvironmentApp
            Graphical version of 
    """
    # size = width, height = 600, 400  # uncomment to override
    def __init__(self, environment:XYEnvironment=None, steps=100, **kwargs):
        if environment is None:
            print(f"{self}: No environment specified, using default")
            environment = XYEnvironment(12, 8)
        if not isinstance(environment, XYEnvironment):
            raise TypeError(f"{self}: environment must be XYEnvironment")

        self.environment = environment
        self._fit_to_environment()
        super().__init__(**kwargs)

        self.thing_font = pygame.font.SysFont("segoe-ui-symbol", 28)
        self.counter = -1
        self.steps = steps
        
    def _fit_to_environment(self):
        """ Fit width and height ratios to match environment """
        _flag = self.environment.width > self.environment.height
        if _flag:
            xy_ratio = self.environment.width/self.environment.height
            a, b = self.height, self.width
        else:
            xy_ratio = self.environment.height/self.environment.width
            b, a = self.height, self.width

        a = b // xy_ratio
        b = int(a*xy_ratio)

        self.height, self.width = (a,b) if _flag else (b,a)
        self.size = self.width, self.height

    def update(self):
        if self.counter < 0:
            self.counter += 1
            return
        if self.counter < self.steps and not self.environment.is_done:
            self.environment.step()
            self.counter += 1
    
    def render(self):
        self.screen.fill(self.environment.color)
        self.render_grid()
        self.render_things()

    def render_grid(self):
        """ render tiles """
        nx,ny = self.environment.width, self.environment.height
        self.tile_size = self.width // nx
        tile_origin = (0, 0)
        tiles = []
        for i in range(ny):
            row = []
            for j in range(nx):
                tileRect = pygame.Rect(
                    tile_origin[0] + j * self.tile_size,
                    tile_origin[1] + i * self.tile_size,
                    self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, COLOR_WHITE, tileRect, 1)

                row.append(tileRect)
            tiles.append(row)
        self.tiles = tiles

    def render_things(self):
        """ render things """
        locations = {}
        for thing in self.environment.things:
            if thing.location in locations:
                locations[thing.location].append(thing)
            else:
                locations[thing.location] = [thing]
        for location, things in locations.items():
            n_things = len(things)
            if n_things > 1:
                thing = things[random.randint(0,n_things-1)]
            elif n_things == 1:
                thing = things[0]
            else:
                continue
            renderLoc = self.tiles[location[1]][location[0]].center
            thingRender = self.thing_font.render(str(thing), True, COLOR_WHITE)
            thingRect = thingRender.get_rect()
            thingRect.center = renderLoc
            self.screen.blit(thingRender, thingRect)
