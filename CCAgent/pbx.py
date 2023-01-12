"""
pbx.py
==========

This impliment the function commands for agent to communicate with the pbx

"""
from collections import namedtuple
from typing import Dict,Callable
from pystrix import ami
from pystrix.ami import core

class pbx():
    """
    """
    _manager:   ami.Manager = None
    _connection_status: bool = False
    _call_back_register : Dict[str,Callable] = None

    def __init__(self,host,port,user,password,debug) -> None:
        self._host = host
        self._port = port
        self._username = user
        self._password = password
        self.debug = debug
        self._manager = ami.Manager(debug=debug)
        self.regiser_call_back({
            'Shutdown' : self._handle_shutdown,
            'FullyBooted':self._handle_booting
            })


    def regiser_call_back(self,callbacks:Dict[str,Callable]):
        "regiser callback on ami event to function"
        [
            self._manager.register_callback(event,handler) 
            for event,handler in callbacks.items()
            ]

    def connect(self):
        " Run for connecting to the asterisk"
        try:
            self._manager.connect(self._host,self._port)
            challenge_response = self._manager.send_action(core.Challenge())
            if challenge_response and challenge_response.success:
                log_action = core.Login(
                    self._user,
                    self._password,
                    challenge=challenge_response.result['Challenge']
                    )
                self._manager.send_action(log_action)
            else:
                self._connection_status = False
                raise ConnectionError(
                    "Asterisk did not provide an MD5 challenge token"+
                    (challenge_response is None and ': timed out' or '')
                    )
        except ami.ManagerSocketError as e:
            self._connection_status = False
            raise ConnectionError("Unable to connect to Asterisk server: %(error)s" % {
             'error': str(e),
            })
        except ami.core.ManagerAuthError as reason:
            self._connection_status = False
            raise ConnectionError("Unable to authenticate to Asterisk server: %(reason)s" % {
             'reason': reason,
            })
        except ami.ManagerError as reason:
            self._connection_status = False
            raise ConnectionError("An unexpected Asterisk error occurred: %(reason)s" % {
             'reason': reason,
            })
        self._manager.monitor_connection()
    
    def _handle_shutdown(self):
        self._connection_status = False

    def _handle_booting(self):
        self._connection_status = True

    def is_alive(self):
        return self._connection_status 

    def close(self):
        self._manager.close()


class outbound_dialer(pbx):

    def CreatBridge(self):
        pass


class Error(Exception):
    "base exception for this class"

class ConnectionError(Error):
    "connection related"


