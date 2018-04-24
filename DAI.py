import time
import pony.orm as pny

from DAN import DAN
import models

host = 'farm.iottalk.tw'

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
           'is_sim': False}


def bao2():
    reg_addr = 'Bao2_DataServer'
    _profile = profile.copy()
    _profile['d_name'] = 'Bao2_DataServer'
    _run(_profile, reg_addr, 'bao2')


def bao3():
    reg_addr = 'Bao3_DataServer'
    _profile = profile.copy()
    _profile['d_name'] = 'Bao3_DataServer'
    _run(_profile, reg_addr, 'bao3')


def _run(profile, reg_addr, field):
    dan = DAN()
    dan.device_registration_with_retry(profile, host, reg_addr)
    try:
        while True:
            # Pull data
            for df in dan.selected_DF:
                data = dan.pull_with_timestamp(df)
                if data:
                    print(field, df, data)
                    timestamp = data[0]
                    value = float(data[1][0])
                    with pny.db_session:
                        _ = getattr(models, df.replace('-O', ''))(timestamp=timestamp, field=field, value=value)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        # dan.deregister()
