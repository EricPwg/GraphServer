import time, requests, random
import pony.orm as pny

import DAN 
from models import Input1, Input2, Input3, Input4, Input5

ServerIP = '140.113.131.68' #Change to your IoTtalk IP or None for autoSearching
Reg_addr = None # if None, Reg_addr = MAC address

profile = { 'dm_name' : 'DataServer',
            'df_list' : ['Input1', 'Input2', 'Input3', 'Input4', 'Input5'],
            'is_sim': False,
            # None for autoNaming
            'd_name' : 'SmartGraph'  }         
def dai():
    dan = DAN.DAN()
    dan.device_registration_with_retry(profile, ServerIP, Reg_addr)

    try:
        while True:
            #Pull data
            for df in dan.selectedDF:
                data = dan.pull(df)
                if data != None:
                    timestamp = data[0]
                    value = float(data[1][0])
                    with pny.db_session:
                        re = globals()[df](timestamp = timestamp, value = value)
            time.sleep(1)
    except KeyboardInterrupt:
        dan.deregister()
