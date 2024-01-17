"""THINGS.PY

Contains class definitions for some things
"""
from collections.abc import *

class Thing:
    """The base class for all things"""
    def __repr__(self):
        return "❓"

## Some physical things

class Obstacle(Thing):
    def __repr__(self):
        return "🚧"


class Food(Thing):
    def __repr__(self):
        return "🍔"


class Water(Thing):
    def __repr__(self):
        return "💧"


class Animal(Thing):
    pass


class Dog(Animal):
    """If it looks like a dog and it barks like a dog ..."""
    def __repr__(self):
        return "🐶"

## Some agent things

class Agent(Thing):
    pass


class RationalAgent(Agent):
    """ Base class for rational agent """
    def __init__(self, program):
        self.performance = 0
        if program is None or not isinstance(program, Callable):
            raise ValueError("No valid program provided")
        self.program = program


class ModelBasedAgent(RationalAgent):
    def __init__(self):
        super().__init__(self.program)

    def program(self, percepts):
        raise NotImplementedError

## State
class State(Thing):
    def __repr__(self):
        return self.__class__.__name__
    
class Bump(State):
    pass