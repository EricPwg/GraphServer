import requests, time, CSMAPI, random, threading, socket, uuid

class DAN:
    def __init__(self):
        self.state = 'SUSPEND'
        self.selectedDF = []
        self.control_channel_timestamp = None
        self.timestamp = {}
        self.profile = {}
        self.mac = None
        self.csmapi = CSMAPI.CSMAPI()

    def control_channel(self):
        while True:
            time.sleep(2)
            try:
                ch = self.csmapi.pull(self.mac, '__Ctl_O__')
                if ch != []:
                    if self.control_channel_timestamp == ch[0][0]: continue
                    self.control_channel_timestamp = ch[0][0]
                    self.state = ch[0][1][0]
                    if self.state == 'SET_DF_STATUS' :
                        self.csmapi.push(self.mac, '__Ctl_I__',['SET_DF_STATUS_RSP',{'cmd_params':ch[0][1][1]['cmd_params']}])
                        DF_STATUS = list(ch[0][1][1]['cmd_params'][0])
                        self.selectedDF = []
                        index=0            
                        for STATUS in DF_STATUS:
                            if STATUS == '1':
                                self.selectedDF.append(self.profile['df_list'][index])
                            index=index+1
            except Exception as e:
                print (e)

    def get_mac_addr(self):
        mac = uuid.uuid4().hex
        # mac = ''.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        return mac

    def register_device(self):

        if self.profile['d_name'] == None: 
            self.profile['d_name']= str(int(random.uniform(1, 100)))+'.'+ self.profile['dm_name']

        for i in self.profile['df_list']: 
            self.timestamp[i] = ''

        print('IoTtalk Server = {}'.format(self.csmapi.ENDPOINT))
        if self.csmapi.register(self.mac, self.profile):
            print ('This device has successfully registered.')
            print ('Device name = ' + self.profile['d_name'])

            thx=threading.Thread(target=self.control_channel)
            thx.daemon = True
            thx.start()
            
            return True
        else:
            print ('Registration failed.')
            return False

    def device_registration_with_retry(self, profile=None, IP=None, addr=None):
        if profile == None or IP == None:
            print('IoTtalk server IP and device profile can not be ignore!')
            return
        self.mac = addr if addr != None else self.get_mac_addr()    
        self.profile = profile
        print(profile)
        self.csmapi.ENDPOINT = 'http://' + IP + ':9999'
        success = False
        while not success:
            try:
                self.register_device()
                success = True
            except Exception as e:
                print ('Attach failed: '),
                print (e)
            time.sleep(1)

    def pull(self, FEATURE_NAME):

        data = self.csmapi.pull(self.mac, FEATURE_NAME) if self.state == 'RESUME' else []

        if data != []:
            if self.timestamp[FEATURE_NAME] == data[0][0]:
                return None
            self.timestamp[FEATURE_NAME] = data[0][0]
            if data[0][1] != []:
                return (data[0][0], data[0][1])
            else: return None
        else:
            return None

    def push(self, FEATURE_NAME, *data):
        if self.state == 'RESUME':
            return self.csmapi.push(self.mac, FEATURE_NAME, list(data))
        else: return None

    def get_alias(self, FEATURE_NAME):
        try:
            alias = self.csmapi.get_alias(self.mac, FEATURE_NAME)
        except Exception as e:
            print (e)
            return None
        else:
            return alias

    def set_alias(self, FEATURE_NAME, alias):
        try:
            alias = self.csmapi.set_alias(self.mac, FEATURE_NAME, alias)
        except Exception as e:
            print (e)
            return None
        else:
            return alias        
        
    def deregister(self):
        return self.csmapi.deregister(self.mac)
