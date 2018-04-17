import time, requests, random
import pony.orm as pny

import DAN 
from models import Input1, Input2, Input3, Input4, Input5
        
def dai():
    ServerIP = 'test.iottalk.tw' #Change to your IoTtalk IP or None for autoSearching
    Reg_addr = None # if None, Reg_addr = MAC address

    DAN.profile['dm_name'] = 'DataServer'
    DAN.profile['df_list'] = ['Input1', 'Input2', 'Input3', 'Input4', 'Input5']
    DAN.profile['d_name'] = 'SmartGraph'
    DAN.device_registration_with_retry(ServerIP, Reg_addr)

    while True:
        try:
            for df in DAN.SelectedDF:
                data = DAN.pull(df)
                if data != None:
                    timestamp = data[0]
                    value = float(data[1][0])
                    with pny.db_session:
                        re = globals()[df](timestamp = timestamp, value = value)

        except Exception as e:
            print(e)
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
        except KeyboardInterrupt:
            DAN.deregister()
        time.sleep(0.2)
