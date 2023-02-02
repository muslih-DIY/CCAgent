
from CCAgent.pbx import pbx
import time

def test_of_test():
    "pytest configuration is success"
    assert True

def test_connectivity_ami():
    "connection test"
    pbx_manager = pbx(
        '10.196.212.200',
        80,
        'CCagent',
        'agent007',
        True
        )

    pbx_manager.connect()
    time.sleep(2)
    assert pbx_manager.live

    pbx_manager.close()
    time.sleep(2)
    assert pbx_manager.live != True
    
