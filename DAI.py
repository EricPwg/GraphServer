import time, DAN, requests, random

ServerIP = 'test.iottalk.tw' #Change to your IoTtalk IP or None for autoSearching
Reg_addr = None # if None, Reg_addr = MAC address

profile = { 'dm_name' : 'Dummy_Device',
            'df_list' : ['Dummy_Control'],
            'is_sim': False,
            # None for autoNaming
            'd_name' : 'smart'  }         
dan = DAN.DAN()
dan.device_registration_with_retry(profile, ServerIP, Reg_addr)

try:
    while True:
        try:
            #Pull data
            for df in dan.selectedDF:
                data = dan.pull(df)
                if data != None:
                    timestamp =data[0]
                    value = data[1]
                    print(df, timestamp, value)

        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
            dan.device_registration_with_retry(profile, ServerIP, Reg_addr)
        time.sleep(1)
except KeyboardInterrupt:
    dan.deregister()
