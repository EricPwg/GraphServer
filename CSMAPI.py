import requests

class CSMError(Exception):
    pass

class CSMAPI():

    IoTtalk = requests.Session()

    def __init__(self, ENDPOINT=None, TIMEOUT=10):
        self.ENDPOINT = ENDPOINT
        self.TIMEOUT = TIMEOUT    

    def register(self, mac_addr, profile):
        r = self.IoTtalk.post(
            self.ENDPOINT + '/' + mac_addr,
            json={'profile': profile}, timeout=self.TIMEOUT
        )
        if r.status_code != 200: raise CSMError(r.text)
        return True


    def deregister(self, mac_addr):
        r = self.IoTtalk.delete(self.ENDPOINT + '/' + mac_addr)
        if r.status_code != 200: raise CSMError(r.text)
        return True


    def push(self, mac_addr, df_name, data):
        r = self.IoTtalk.put(
            self.ENDPOINT + '/' + mac_addr + '/' + df_name,
            json={'data': data}, timeout=self.TIMEOUT
        )
        if r.status_code != 200: raise CSMError(r.text)
        return True


    def pull(self, mac_addr, df_name):
        r = self.IoTtalk.get(self.ENDPOINT + '/' + mac_addr + '/' + df_name, timeout=self.TIMEOUT)
        if r.status_code != 200: raise CSMError(r.text)
        return r.json()['samples']


    def get_alias(self, mac_addr, df_name):
        r = self.IoTtalk.get(self.ENDPOINT + '/get_alias/' + mac_addr + '/' + df_name, timeout=self.TIMEOUT)
        if r.status_code != 200: raise CSMError(r.text)
        return r.json()['alias_name']


    def set_alias(self, mac_addr, df_name, s):
        r = self.IoTtalk.get(self.ENDPOINT + '/set_alias/' + mac_addr + '/' + df_name + '/alias?name=' + s, timeout=self.TIMEOUT)
        if r.status_code != 200: raise CSMError(r.text)
        return True


    def tree(self):
        r = self.IoTtalk.get(self.ENDPOINT + '/tree')
        if r.status_code != 200: raise CSMError(r.text)
        return r.json()
