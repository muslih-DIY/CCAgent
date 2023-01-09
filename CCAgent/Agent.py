from __future__ import annotations
from abc import ABC ,abstractmethod

class CCAgent():
    
    _state: AgentState = None
    _Agentid :str = None
    
    def __init__(self,agentid:str) -> None:

        self._Agentid = agentid

    def update_state(self,state:AgentState):
        
        self._state = state
        self._state.Agent = self

    def Login(self)->None:

        self._state.Login()

    def Logout(self)->None:
        
        self._state.Logout()

    def pause(self)->None:

        self._state.pause()

    def dial(self)->None:
        
        self._state.dial()

    def hold(self)->None:
        
        self._state.hold()

    def hang(self)->None:
        
        self._state.hang()



class AgentState(ABC):
    
    @property
    def Agent(self)-> CCAgent:

        return self._CCAgent

    @Agent.setter
    def Agent(self,ccagent:CCAgent)-> None:

        self._CCAgent = ccagent

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
    def hold()->None:
        pass

    @abstractmethod
    def hang()->None:
        pass

