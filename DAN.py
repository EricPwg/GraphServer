# -*- coding: UTF-8 -*-
import requests, time, csmapi, random, threading, socket, uuid, sys
from asyncio.tasks import sleep

class DAN:
    def __init__(self):
        self.state = 'SUSPEND'
        self.selectedDF = []
        self.control_channel_timestamp = None
        self.timestamp = {}
        self.profile = {}
        self.mac = None
        self.IP = None
        self.control_thread = None;
        self.control_thread_runing = True;
        self.csmapi = csmapi.CSMAPI()

    def control_channel(self):
        #print ('Control Channel Runing')
        #sys.stdout.flush();
        ControlSession=requests.Session()
        while True:
            time.sleep(1)
            try:
                ch = self.csmapi.pull(self.mac, '__Ctl_O__', ControlSession)
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
                if self.control_thread_runing != True:
                    break;
            except Exception as e:
                time.sleep(5)
                typestr = str(e);
                
                pos = typestr.find("HTTPConnectionPool",0,300)
                #if pos == -1:
                    #print ("control_channel:",e)
                    #sys.stdout.flush();
                
                pos = typestr.find("mac_addr not found",0,300)
                if pos != -1:
                    time.sleep(60)
                    if self.control_thread_runing != True:
                        break;
                    self.device_registration_with_retry(self.profile, self.IP, self.mac)

    def get_mac_addr(self):
        mac = uuid.uuid4().hex
        # mac = ''.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        return mac

    def detect_local_ec(self):
        EASYCONNECT_HOST=None
        UDP_IP = ''
        UDP_PORT = 17000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((UDP_IP, UDP_PORT))
        while EASYCONNECT_HOST==None:
            #print ('Searching for the IoTtalk server...')
            #sys.stdout.flush();
            data, addr = s.recvfrom(1024)
            if str(data.decode()) == 'easyconnect':
                EASYCONNECT_HOST = 'http://{}:9999'.format(addr[0])
                self.csmapi.ENDPOINT=EASYCONNECT_HOST
                #print('IoTtalk server = {}'.format(self.CSMAPI.ENDPOINT))
                #sys.stdout.flush();

    def register_device(self, **registerSession):
        if self.csmapi.ENDPOINT == None: self.detect_local_ec()

        if self.profile['d_name'] == None: 
            self.profile['d_name']= str(int(random.uniform(1, 100)))+'.'+ self.profile['dm_name']

        for i in self.profile['df_list']: 
            self.timestamp[i] = ''

        #print('IoTtalk Server = {}'.format(self.csmapi.ENDPOINT))
        #sys.stdout.flush();
        if self.control_thread_runing != True:
            return False
        
        if registerSession:
            ##print("in register_device if");
            if self.csmapi.register(self.mac, self.profile, registerSession["Session"]):
                #print ('This device has successfully registered.')
                #print ('Device name = ' + self.profile['d_name'])
                #sys.stdout.flush();
    
                if self.control_thread == None: 
                    self.control_thread=threading.Thread(target=self.control_channel)
                    self.control_thread.daemon = True
                    self.control_thread.start()
                
                return True
            else:
                #print ('Registration failed.')
                #sys.stdout.flush();
                return False
        else:
            if self.csmapi.register(self.mac, self.profile):
                #print ('This device has successfully registered.')
                #print ('Device name = ' + self.profile['d_name'])
                #sys.stdout.flush();
    
                if self.control_thread == None: 
                    self.control_thread=threading.Thread(target=self.control_channel)
                    self.control_thread.daemon = True
                    self.control_thread.start()
                
                return True
            else:
                #print ('Registration failed.')
                #sys.stdout.flush();
                return False

    def device_registration_with_retry(self, profile=None, IP=None, addr=None, **registerSession):
        if profile == None or IP == None:
            #print("profile = ",profile)
            #print("IP = ", IP)
            #print('IoTtalk server IP and device profile can not be ignore!')
            #sys.stdout.flush();
            return
        self.mac = addr if addr != None else self.get_mac_addr()    
        self.profile = profile
        self.IP = IP
        #print(profile)
        #sys.stdout.flush();
        self.csmapi.ENDPOINT = 'http://' + IP + ':9999'
        success = False
        while not success:
            try:
                if registerSession:
                    ##print("in device_registration_with_retry if");
                    self.register_device(**registerSession)
                else:
                    self.register_device()
                success = True
            except Exception as e:
                stre = str(e)
                #print ('Attach failed: '),
                #print (e)
                #sys.stdout.flush();
            time.sleep(5)

    def pull(self, FEATURE_NAME, **pullSession):
        data =None;
        
        #if(self.state != 'RESUME'):
        #    time.sleep(5);
        #    self.state = 'RESUME';
            
        try:
            if pullSession:
                ##print("in pull if");
                data = self.csmapi.pull(self.mac, FEATURE_NAME, pullSession["Session"]) if self.state == 'RESUME' else []
            else:
                data = self.csmapi.pull(self.mac, FEATURE_NAME) if self.state == 'RESUME' else []
        except Exception as e:
            #print (e)
            #print ("pull error:",e)
            #sys.stdout.flush();
            typestr = str(e);
            pos = typestr.find("mac_addr not found",0,100)
            if pos != -1:
                time.sleep(60)
                if self.control_thread_runing != True:
                    return None
                self.device_registration_with_retry(self.profile, self.IP, self.mac)
                return None
            else:
                raise e;

        if data != []:
            if self.timestamp[FEATURE_NAME] == data[0][0]:
                return None
            self.timestamp[FEATURE_NAME] = data[0][0]
            if data[0][1] != []:
                return data[0][1]
            else: return None
        else:
            return None

    def push(self, FEATURE_NAME, *data, **pushSession):
        #if(self.state != 'RESUME'):
        #    time.sleep(5);
        #    self.state = 'RESUME';
            
        if self.state == 'RESUME':
            try:
                if pushSession:
                    ##print("in push if");
                    return self.csmapi.push(self.mac, FEATURE_NAME, list(data), pushSession["Session"])
                else:
                    return self.csmapi.push(self.mac, FEATURE_NAME, list(data))
            except Exception as e:
                #print (e)
                #print ("push error:",e)
                #sys.stdout.flush();
                typestr = str(e);
                pos = typestr.find("mac_addr not found",0,100)
                if pos != -1:
                    time.sleep(60)
                    if self.control_thread_runing != True:
                        return None
                    self.device_registration_with_retry(self.profile, self.IP, self.mac)
                    return None
                else:
                    raise e;
        else: return None;

    def get_alias(self, FEATURE_NAME, **getaliasSession):
        aliasreturn =None;
        
        #if(self.state != 'RESUME'):
        #    time.sleep(5);
        #    self.state = 'RESUME';
            
        try:
            if getaliasSession:
                #print("in get_alias if");
                aliasreturn = self.csmapi.get_alias(self.mac, FEATURE_NAME, getaliasSession["Session"])
            else:
                aliasreturn = self.csmapi.get_alias(self.mac, FEATURE_NAME)
        except Exception as e:
            #print (e)
            #print ("get alias error:",e)
            #sys.stdout.flush();
            typestr = str(e);
            pos = typestr.find("mac_addr not found",0,100)
            if pos != -1:
                time.sleep(60)
                if self.control_thread_runing != True:
                    return None
                self.device_registration_with_retry(self.profile, self.IP, self.mac)
                return None
            else:
                raise e;
        else:
            return aliasreturn;

    def set_alias(self, FEATURE_NAME, alias, **setaliasSession):
        aliasreturn =None;
        
        #if(self.state != 'RESUME'):
        #    time.sleep(5);
        #    self.state = 'RESUME';
            
        try:
            if setaliasSession:
                #print("in set_alias if");
                aliasreturn = self.csmapi.set_alias(self.mac, FEATURE_NAME, alias, setaliasSession["Session"])
            else:
                aliasreturn = self.csmapi.set_alias(self.mac, FEATURE_NAME, alias)
        except Exception as e:
            #print (e)
            #print ("set alias error:",e)
            #sys.stdout.flush();
            typestr = str(e);
            pos = typestr.find("mac_addr not found",0,100)
            if pos != -1:
                time.sleep(60)
                if self.control_thread_runing != True:
                    return None
                self.device_registration_with_retry(self.profile, self.IP, self.mac)
                return None
            else:
                raise e;
        else:
            return aliasreturn;        
        
    def deregister(self, **deregisterSession):
        self.control_thread_runing = False;
        deregisterreturn = None;
        index = 0;
        """
        if deregisterSession:
            #print("in deregister if");
            return self.csmapi.deregister(self.mac, deregisterSession["Session"])
        else:
            #print("in else");
            return self.csmapi.deregister(self.mac)
        """
        while True:
            try:
                #print("deregisterSession: ", deregisterSession)
                if deregisterSession:
                    #print("in if");
                    deregisterreturn = self.csmapi.deregister(self.mac, deregisterSession["Session"])
                else:
                    #print("in else");
                    deregisterreturn = self.csmapi.deregister(self.mac)
                break;
                    
            except Exception as e:
                #print(e);
                time.sleep(1)
                index = index + 1;
                if(index < 3):
                    continue;
                else:
                    return e;
        return deregisterreturn;
        