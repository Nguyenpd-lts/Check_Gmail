import requests
import time
import queue
import configparser
import threading
import configparser

class _OTPSim(object):
    def __init__(self, callback=None):
        print('>> initial OTP Sim')
        self.base_name = 'otpSim'
        self.api_url = 'https://otpsim.com/api/'
        self.is_working = True
        self.id_service_hm = 5
        self.is_login_success = False
        #queue
        self.mess_queue = queue.Queue()
        self.message = None
        self.messages = None
        self.list_queue = None
        self.session = None
        self.balance = None

        self.callback = callback

        conf = configparser.ConfigParser()
        conf.read('config.ini')

        self.api_key = str(conf['Main']['OTP_SIM'])
    
    def log(self, str):
        str_base = "[{base_name}] --> {str}".format(base_name = self.base_name, str=str)
        print(str_base)
    # @property

    def current_balance(self):
        self.log('current balance....')
        """
            Get balance current
        """
        url = self.api_url + "users/balance?token={api_key}".format(api_key=self.api_key)
        # print(url)

        req = requests.get(url)

        if req.status_code == 200:
            response = req.json()
            print(response)
            if response['success'] == True and response['data']:
                self.is_login_success = True
                return response['data']['balance']
            else:
                return "error - {}".format(req.data.balance)
        else:
            return 'get failed, please check account!!'
    
    def request(self):
        """
        Request service 
        """
        self.log('request phone..{api_key}'.format(api_key=self.api_key))
        url = self.api_url + 'phones/request?token={api_key}&service={id_service}'.format(api_key=self.api_key, id_service =self.id_service_hm)
        req = requests.get(url)
        self.log(url)

        if req.status_code == 200:
            response = req.json()
            print(response)
            if response['data']:
                return response['data']['phone_number'], response['data']['session']
            else:
                return 'error - {}'.format(response), 0
        else:
            return "request failed", 0
    def get_message(self):
        self.log('get message phone....')
        while True:
            mess = self.mess_queue.get()
            if mess == None:
                break
            if self.list_queue != None:
                self.list_queue.put(mess)
            self.message = mess
            self.log('New Mess is: {}'.format(mess))
        self.is_working = False
        self.log('exit done')

    def add_out(self):
        self.log('add out phone....')
        self.list_queue = 1

    def check(self):
        """
        Check infor order
        """
        self.log('check phone....')
        # url = self.api_url + 'sessions/{session}?token={api_key}'.format(api_key=self.api_key, session = self.session)
        url = self.api_url + 'sessions/786e5f193b5eec5bf9e5dfe7fb7bab6b?token={api_key}'.format(api_key=self.api_key)
        req = requests.get(url)
        self.log('check phone....{url}'.format(url=url))
        if req.status_code == 200:
            response = req.json()
            return response['data']
        else:
            return -1

    def check_message(self):
        self.log('Waitting message....')
        data = self.check()
        try:
            self.messages = []
            while self.is_working:
                data = self.check()
                if data['status'] == 0:
                    mess = data['messages'][0]['otp']
                    self.log('otp....{ress}'.format(ress= mess))
                    if mess not in self.messages:
                        self.messages.append(mess)
                        self.mess_queue.put(mess)
                        print(self.messages)

                time.sleep(0.5)

        except Exception as e:
            self.log("Error get" + str(e))
        finally:
            self.mess_queue.put(None)

    def cancel(self):
        """
        cancel order
        """
        print('cancel order')
        url = self.api_url + 'sessions/cancel?session={session}?token={api_key}'.format(api_key=self.api_key, session = self.session)
        req = requests.get(url)
        if req.status_code == 200:
            response = req.json()
            return response['message']
        else:
            return "request failed"
    def quit(self):
        self.log('Quit')
        self.is_working = False
        ret = self.cancel()
        self.log("ret{}".format(ret))
    def message_monitor(self):
        self.log('message monitor....')
        worker = threading.Thread(target=self.get_message)
        worker.setDaemon(True)
        worker.start()

        worker = threading.Thread(target=self.check_message)
        worker.setDaemon(True)
        worker.start()
    
    '''
    #service:
    Gmail/Google/Youtube:3 | Hotmail/Outlook:5 | Yahoo:6
    '''
    def run(self):
        print(self.api_key)
        # set up url api
        # Get Balance otpsim
        balance = self.current_balance()
        self.log("current balance is {}".format(balance))
        # Notify request phone
        self.log("Request get phone...")
        _phone, _session = self.request()
        self.session = _session
        self.phone = _phone
        self.log("Phone is: {}".format(self.phone))
        self.log("Session is: {}".format(self.session))

        self.message_monitor()

if __name__ == '__main__':
    try:
        otp = _OTPSim()
        otp.run()
    except Exception as e:
        print('Error' + str(e))
