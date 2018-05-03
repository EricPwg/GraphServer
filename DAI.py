import time
import pony.orm as pny

from DAN import DAN
import models

host = '140.113.199.199'

profile = {'dm_name': 'DataServer_plant',
           'df_list': [
                       'CO2-O',                       
                       'Humidity-O',
					   'O2-O',
					   'Temperature-O',
                       'WatchingDog-O',
                       'WaterLevel-O',
                       ],
           'is_sim': False}


def bao2():
    reg_addr = 'Bao2_DataServer'
    _profile = profile.copy()
    _profile['d_name'] = 'Bao2_DataServer_plantbox'
    _run(_profile, reg_addr, 'bao2')



def _run(profile, reg_addr, field):
    dan = DAN()
    dan.device_registration_with_retry(profile, host, reg_addr)
    dan.selected_DF = profile['df_list']
    try:
        while True:
            # Pull data
            for df in dan.selected_DF:
            #for df in profile['df_list']:
                #print (df)
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
