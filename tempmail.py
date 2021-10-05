import requests
import time
import queue
import configparser
import threading
import configparser
import json
import re

class _TempMail(object):

    def __init__(self, callback=None):
        print('>> initial TempMail')
        self.base_name = 'TempMail'
        self.api_url = 'https://api.internal.temp-mail.io/api/v3/email/'
        self.is_working = True
        self.id_service_hm = 5
        self.is_login_success = False
        #queue
        self.mess_queue = queue.Queue()
        self.message = None
        self.messages = None
        self.list_queue = None
        self.mailbox = None

    def log(self, str):
        str_base = "[{base_name}] --> {str}".format(base_name = self.base_name, str=str)
        print(str_base)

    def request(self):
        """
        Request service 
        """
        url = self.api_url + 'new'
        req = requests.post(url)
        print(req.status_code)
        if req.status_code == 200:
            response = req.json()
            print(response)
            return response['email'], response['token']
        else:
            return "request failed", 0
    
    def check(self):
        """
        Check infor order
        https://api.internal.temp-mail.io/api/v3/email/hkce0g20@mac-24.com/messages
        """
        self.log('check Messages....')
        url = self.api_url + '{email}/messages'.format(email = self.mailbox)
        # url = 'https://api.internal.temp-mail.io/api/v3/email/hkce0g20@mac-24.com/messages'
        req = requests.get(url)

        if req.status_code == 200:
            response = req.json()
            body_text = response[0]['body_text']
            text = re.findall(r"code: [0-9]*", body_text)
            code = re.search(r"[0-9]*$", text[0])
            textcode = int(code.group())
            self.log("{}".format(textcode))
            return code
        else:
            return -1

    def get_message(self):
        self.log('get message Mail....')
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

    def check_message(self):
        self.log('Waitting message....')
        data = self.check()
        try:
            self.messages = []
            while self.is_working:
                mess = self.check()
                if mess not in self.messages:
                    self.messages.append(mess)
                    self.mess_queue.put(mess)
                    self.log('messages....{ress}'.format(ress= self.messages))
                time.sleep(0.5)

        except Exception as e:
            self.log("Error get" + str(e))
        finally:
            self.mess_queue.put(None)

    def message_monitor(self):
        self.log('message monitor....')
        worker = threading.Thread(target=self.get_message)
        worker.setDaemon(True)
        worker.start()

        worker = threading.Thread(target=self.check_message)
        worker.setDaemon(True)
        worker.start()

    def test():
        import re
        stra = "Please use the following security code for the Microsoft account ed*****@hotmail.com.\n\nSecurity code: 7900\n\nIf you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.\n\nThanks,\nThe Microsoft account team "
        mat = re.match(r"Security code: [0-9]*", stra)

    def run(self):
        # set up url api
        # Notify request token
        self.check()
        self.log("Request get token...")
        _mailbox, _token = self.request()
        self.mailbox = _mailbox
        self.token = _token
        self.log("mailbox is: {}".format(self.mailbox))

        self.message_monitor()

if __name__ == '__main__':
    try:
        otp = _TempMail()
        otp.run()
    except Exception as e:
        print('Error' + str(e))
