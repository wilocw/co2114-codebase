from search import things

Agent = things.Agent
UtilityBasedAgent = things.UtilityBasedAgent

class Hospital(things.Thing):
    def __repr__(self):
        return "🏥"

class House(things.Thing):
    def __repr__(self):
        return "🏠"

class Optimiser(things.Agent):
    def __repr__(self):
        return "📈"