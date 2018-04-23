import requests

class CSMError(Exception):
    pass

class CSMAPI():

    IoTtalk = requests.Session()
    IoTtalk.keep_alive = False

    def __init__(self, ENDPOINT=None, TIMEOUT=20):
        self.ENDPOINT = ENDPOINT
        self.TIMEOUT = TIMEOUT    

    def register(self, mac_addr, profile, UsingSession=IoTtalk):
        r = UsingSession.post(
            self.ENDPOINT + '/' + mac_addr,
            json={'profile': profile}, timeout=self.TIMEOUT
        )
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return True


    def deregister(self, mac_addr, UsingSession=IoTtalk):
        r = UsingSession.delete(self.ENDPOINT + '/' + mac_addr, timeout=self.TIMEOUT)
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return True


    def push(self, mac_addr, df_name, data, UsingSession=IoTtalk):
        r = UsingSession.put(
            self.ENDPOINT + '/' + mac_addr + '/' + df_name,
            json={'data': data}, timeout=self.TIMEOUT,
            headers={'Connection': 'close'}
        )
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return True


    def pull(self, mac_addr, df_name, UsingSession=IoTtalk):
        r = UsingSession.get(self.ENDPOINT + '/' + mac_addr + '/' + df_name, timeout=self.TIMEOUT, headers={'Connection': 'close'})
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return r.json()['samples']


    def get_alias(self, mac_addr, df_name, UsingSession=IoTtalk):
        r = UsingSession.get(self.ENDPOINT + '/get_alias/' + mac_addr + '/' + df_name, timeout=self.TIMEOUT)
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return r.json()['alias_name']


    def set_alias(self, mac_addr, df_name, s, UsingSession=IoTtalk):
        r = UsingSession.get(self.ENDPOINT + '/set_alias/' + mac_addr + '/' + df_name + '/alias?name=' + s, timeout=self.TIMEOUT)
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return True


    def tree(self, UsingSession=IoTtalk):
        r = UsingSession.get(self.ENDPOINT + '/tree')
        if r.status_code != 200: 
            r.close()
            raise CSMError(r.text)
        r.close()
        return r.json()
