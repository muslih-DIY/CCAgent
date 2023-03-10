"""
pbx.py
==========

This impliment the function commands for agent to communicate with the pbx

"""
#from collections import namedtuple
from typing import Dict,Callable
from pystrix import ami
from pystrix.ami import core
import functools

class pbx():
    """
    --_pbx base class
    """
    _manager:   ami.Manager = None
    _connection_status: bool = False
    _call_back_register : Dict[str,Callable] = None

    def __init__(self,host:str,port:int,user:str,password:str,debug=False) -> None:
        self._host = host
        self._port = int(port)
        self._username = user
        self._password = password
        self.debug = debug.lower() in ('1','true','yes')
        self._manager = ami.Manager(debug=debug)
        self.regiser_call_back({
            'Shutdown' : self._handle_shutdown,
            'FullyBooted':self._handle_booting
            })


    def regiser_call_back(self,callbacks:Dict[str,Callable]):
        "regiser callback on ami event to function"

        for event,handler in callbacks.items():
            self._manager.register_callback(event,handler)

    def connect(self):
        " Run for connecting to the asterisk"
        try:
            self._manager.connect(self._host,self._port)
            challenge_response = self._manager.send_action(core.Challenge())
            if challenge_response and challenge_response.success:
                log_action = core.Login(
                    self._username,
                    self._password,
                    challenge=challenge_response.result['Challenge']
                    )
                self._manager.send_action(log_action)
            else:
                self._connection_status = False
                raise PBXConnectionError(
                    "Asterisk did not provide an MD5 challenge token"+
                    (challenge_response is None and ': timed out' or '')
                    )
        except ami.ManagerSocketError as error:
            self._connection_status = False
            raise PBXConnectionError(f"Unable to connect to Asterisk server: {error}") from error

        except ami.core.ManagerAuthError as reason:
            self._connection_status = False
            raise PBXConnectionError(f"Unable to authenticate to Asterisk server:{reason}") from reason

        except ami.ManagerError as reason:
            self._connection_status = False
            raise PBXConnectionError(f"An unexpected Asterisk error occurred: {reason}") from reason

        self._manager.monitor_connection()

    def _handle_shutdown(self, event, manager):
        self._connection_status = False

    def _handle_booting(self, event, manager):
        self._connection_status = True

    @property
    def live(self):
        "return live or not"
        return self._connection_status

    def close(self):
        "close connection with the asterisk"
        self._manager.close()
        self._connection_status = False
    
    @staticmethod
    def sendaction(amiaction):

        @functools.wraps(amiaction)
        def decorate(self,*args,**kwargs):
    
            return self._manager.send_action(amiaction(self,*args,**kwargs))
        
        return decorate


    @sendaction
    def Originate(self,
        channel: str, context: str,extension: str,
        priority: int=1,timeout = None,callerid: str = None,
        variables: dict = {},account: str = None,async_: bool = True):
        "originate a call to extension and join to another extension"
        return core.Originate_Context(channel,context,extension,priority,timeout,callerid,variables,account,async_)

    @sendaction
    def ConfbridgeKick(self,conference_id: str, channel: str):
        return ami.app_confbridge.ConfbridgeKick(conference_id,channel)


class outbound_pbx(pbx):
    """obd"""
    @staticmethod
    def get_bridge_id(agentid:str)->str:
        'It return the id for an agent'
        return ''.join(['OBDBRIDGE',agentid])

    @staticmethod
    def get_channel(endpoint:str)->str:
        'It return the id for an agent'
        return f"PJSIP/{endpoint}"

    def creat_bridge(
        self,
        agentid:str
        ):
        "It will create a bridge by calling "
        conference_id = outbound_pbx.get_bridge_id(agentid)
        print('originate.....')
        return self.Originate(f'PJSIP/{agentid}','agent-conf',conference_id,1)
         

    def leave_bridge(
        self,
        agentid:str
        ):
        "It will kick the agent out of the Bridge and Others may stay or not"

        conference_id = outbound_pbx.get_bridge_id(agentid)
        channel_id = outbound_pbx.get_channel(agentid)
        return self.ConfbridgeKick(conference_id,channel_id)

    def caller_join_bridge(
        self,
        number:str,
        bridge:str,
        ):
        "call a number and join to a bridge/Agent"
        print('INFO:',f'originated : calling {number} to bridge {bridge}')
        return 1

    def caller_kick_bridge(
        self,
        number:str,
        bridge:str,
        ):
        "kick a caller out of the Bridge"
        print('INFO:',f'KickAgent : Kick {number} out of the bridge {bridge}')
        return 1




class PBXError(Exception):
    "base exception for this class"

class PBXConnectionError(PBXError):
    "connection related"


