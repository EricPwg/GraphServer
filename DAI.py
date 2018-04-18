import time
import pony.orm as pny

import DAN
import models

ServerIP = 'farm.iottalk.tw'
Reg_addr = 'Bao3_DataServer'

profile = {'dm_name': 'DataServer',
           'df_list': ['AtPressure-O',
                       'CO2-O',
                       'Temperature-O',
                       'Humidity-O',
                       'WindSpeed-O',
                       'RainMeter-O',
                       'Bugs-O',
                       'UV1-O',
                       'UV2-O',
                       'UV3-O',
                       'Moisture1-O',
                       'PH1-O',
                       'Moisture2-O',
                       'PH2-O',
                       'Moisture3-O',
                       'PH3-O',
                       'Moisture4-O',
                       'PH4-O'],
           'is_sim': False,
           'd_name': 'Bao3_DataServer'}


def dai():
    dan = DAN.DAN()
    dan.device_registration_with_retry(profile, ServerIP, Reg_addr)

    try:
        while True:
            # Pull data
            for df in dan.selectedDF:
                data = dan.pull(df)
                if data != None:
                    timestamp = data[0]
                    value = float(data[1][0])
                    with pny.db_session:
                        re = getattr(models, df.replace('-O', ''))(timestamp=timestamp, value=value)
            time.sleep(1)
    except KeyboardInterrupt:
        dan.deregister()
