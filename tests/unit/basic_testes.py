
from CCAgent.pbx import pbx,outbound_pbx
import time
from dotenv import dotenv_values

config = dotenv_values('tests/data/.env')

def test_of_test():
    "pytest configuration is success"
    assert config , 'please create a tests/data/.env file similar to tests/data/ami.env'



def test_connectivity_ami():
    "connection test"
    pbx_manager = pbx(**config)

    pbx_manager.connect()

    assert pbx_manager.live

    pbx_manager.close()

    assert pbx_manager.live != True

def test_obd_agent_login_or_bridge_create():
    "test obd agent login"
    def kick(self,manager,event):
        time.sleep(3)
        print(event)
        #self.ConfbridgeKick()
    obdpbx = outbound_pbx(**config)

    obdpbx.connect()
    bridge = obdpbx.creat_bridge('3001')
    print('originate:',bridge)
    time.sleep(10)
    confid = obdpbx.get_bridge_id('3001')
    channel = obdpbx.get_channel('3001')
    obdpbx.ConfbridgeKick(confid,channel)






