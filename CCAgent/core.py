from __future__ import annotations
from abc import ABC ,abstractmethod

class CCAgent(ABC):
    """
    Base class of an agent
    This may have different type of sub agents such as.
        OBD Agent.
        INBOUBD Agent.
    """
    
    _state: AgentState = None
    _agent :str = None
   
    def __init__(self,agent:str) -> None:
        self._agent = agent
    
    def update_state(self,state:AgentState):
        
        self._state = state
        self._state.Agent = self
    
    @property
    def state(self)->None:
        "state of the agent"
        return self._state

    @state.setter
    def state(self,state:AgentState)->None:
        self._state = state
        self._state.Agent = self

    @abstractmethod
    def login(self)->None:
        pass

    @abstractmethod
    def logout(self)->None:
        pass

    @abstractmethod
    def pause(self)->None:
        pass
    
    @abstractmethod
    def dial(self)->None:        
        pass

    @abstractmethod
    def hold(self)->None:        
        pass

    @abstractmethod
    def hang(self)->None:        
        pass



class AgentState(ABC):

    __CCAgent:CCAgent = None

    @property
    def Agent(self)-> CCAgent:

        return self.__CCAgent

    @Agent.setter
    def Agent(self,ccagent:CCAgent)-> None:

        self.__CCAgent = ccagent

    @abstractmethod
    def Login(self)->None:
        pass

    @abstractmethod
    def Logout(self)->None:
        pass
    
    @abstractmethod
    def pause(self)->None:
        pass

    @abstractmethod
    def dial(self)->None:
        pass

    @abstractmethod
    def hold(self)->None:
        pass

    @abstractmethod
    def hang(self)->None:
        pass

