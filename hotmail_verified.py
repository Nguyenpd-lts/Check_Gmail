import os
import queue
from subprocess import run
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from undetected_chromedriver.options import ChromeOptions
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from chromecore import ChromeBrowser
from firefox import Geckodriver
from optsim import _OTPSim
from tempmail import _TempMail

class Hotmail_Veri(ChromeBrowser):
    def __init__(self, email, pwd, proxy=None, w_position=[]):
        super(Hotmail_Veri, self).__init__(proxy_str=proxy, w_position=w_position)

        self.base_url = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1627918294&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d1dc7f809-ec84-8d8c-def4-bfe89cdbd2f2&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015"
        self.email = email
        self.pwd = pwd
        self.skip_for_now = True

    def test(self, url):
        self.browser.get(url)
        input("...Wait...")

    def hotmail_verify(self, email, pwd):
        resp = False
        try:
            self.browser.get(self.base_url)
            input_mail = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@type="email"]')))
            input_mail.send_keys(email)
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@type="submit"]')))
            but_next.click()
            time.sleep(3)
            input_pwd = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@type="password"]')))
            input_pwd.send_keys(pwd)
            time.sleep(1)
            but_sig = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@type="submit"]')))
            but_sig.click()
            time.sleep(3)

            base_urls = [
                'ppsecure/post.srf?wa=wsignin1.0&rpsnv=13', #wrong pass
                'account.live.com/Abuse?mkt=EN-US&uiflavor=web', #block
                '/proofs/Add?mkt=', #choice mail
            ]

            _id = None
            _loop = 30
            while _loop > 0 and _id == None:
                for _i in range(len(base_urls)):
                    if base_urls[_i] in self.browser.current_url:
                        _id = _i
                        break
                _loop += 1
                time.sleep(1)
            
            _is_success = False

            if _id == 0:
                text_error_pass = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwordError"]')))
                if text_error_pass is None:
                    _id = 3
                    print('Login thanh cong')
                    but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='idSIButton9']")))
                    but_next.click()
                    but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='iCancel']")))
                    but_next.click()
                    _is_success == True
            if _id == 1:
                but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="StartAction"]')))
                but_next.click()
                select = Select(self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Country code"]'))))
                select.select_by_value('VN')
                # input_phone = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Next"]')))
                # inputs = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id]')))
                inputs = self.browser_wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id]')))
                _id_string = 'wlspispHIPPhoneInput'
                _input_phone = None
                _loop1 = 30
                while _loop1 > 0 and _input_phone == None:
                    for _input in inputs:
                        _id_inputs = _input.get_attribute('id')
                        if _id_string in _id_inputs:
                            _input_phone = _input
                            break
                    _loop1 += 1
                    time.sleep(1)
                # verify with phone
                print('->>Threading Otp')
                self.otp_sim = _OTPSim()
                self.otp_sim.run()
                self.phone = '0{}'.format(self.otp_sim.phone)
                _input_phone.send_keys(self.phone)
            
                but_sendcode = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Send code']")))
                but_sendcode.click()
                resp = True
                time.sleep(1)
                code = self.get_otp_code()
                print('[Code]---->' + str(code))
                self.otp_sim.quit()
                print('[Next Button ]---->')
                input_code = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Enter the access code"]')))
                input_code.send_keys(code)
                but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='ProofAction']")))
                but_next.click()
                but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='FinishAction']")))
                but_next.click()
                _is_success = True
                self.temp_mail()
                time.sleep(3)

            if _id == 2:
                self.temp_mail()
                _is_success = True

            return _id, _is_success
        except Exception as e:
            return None, False

    def temp_mail(self):
        if self.skip_for_now:
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='iShowSkip']")))
            but_next.click()
        else:
            select = Select(self.browser_wait.until(EC.presence_of_element_located((By.ID, 'iProofOptions'))))
            select.select_by_value('Email')
            self.temp_mail_box = _TempMail()
            self.temp_mail_box.run()
            self.mailbox = '{}'.format(self.temp_mail_box.mailbox)
            input_email = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='EmailAddress']")))
            input_email.send_keys(self.mailbox)
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='iNext']")))
            but_next.click()
            time.sleep(2)
            code_mail = self.get_otp_code_mail()
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='iOttText']")))
            input_email.send_keys(code_mail)
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='iNext']")))
            but_next.click()
            time.sleep(2)
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='idSIButton9']")))
            but_next.click()
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='iCancel']")))
            but_next.click()

    def thr_mail(self):
        self.ql = queue.Queue()
        self.temp_mail_box.add_out()
        while True:
            text = self.ql.get()
            print('[TempMail service text]' + str(text))
            if text == None:
                break
            self.text = text
    def get_otp_code_mail(self):
        print('[TempMail service]-> wwaiting code')
        run_thread = threading.Thread(target= self.thr_mail)
        run_thread.setDaemon(True)
        run_thread.start()

        ti = 120
        while self.text == None and ti > 0:
            ti -= 1
            time.sleep(1)
        self.ql.put(None)
        if self.text!=None:
            return self.text
        return 0

    def thr(self):
        self.ql = queue.Queue()
        self.otp_sim.add_out()
        while True:
            text = self.ql.get()
            print('[Sim service text]' + str(text))
            if text == None:
                break
            self.text = text
    def get_otp_code(self):
        print('[Sim service]-> wwaiting code')
        run_thread = threading.Thread(target= self.thr)
        run_thread.setDaemon(True)
        run_thread.start()

        ti = 120
        while self.text == None and ti > 0:
            ti -= 1
            time.sleep(1)
        self.ql.put(None)
        if self.text!=None:
            return self.text
        return 0

    def run(self):
        _id, _is_success = self.hotmail_verify(self.email, self.pwd)
        time.sleep(2)
        try:
            self.browser.quit()
            print(_id, _is_success)
        except Exception as e:
            pass
        return _id, _is_success

if __name__ == '__main__':
    try:
        br =  Hotmail_Veri(email='tamy_dosantos@hotmail.com', pwd='01Z33d2T6z')
        print(br.run())
    except Exception as e:
        print(str(e))