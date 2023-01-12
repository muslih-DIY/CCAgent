
from .Agent import AgentState

class UnAvailable(AgentState):
    pass

class Ready(AgentState):
    pass

class Paused(AgentState):
    pass

class Calling(AgentState):
    pass

class Hold(AgentState):
    pass

class Ringing(AgentState):
    pass

