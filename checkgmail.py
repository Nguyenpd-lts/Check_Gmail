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



class Check_Mail(ChromeBrowser):
    def __init__(self, email, pwd, proxy=None, w_position=[]):
        super(Check_Mail, self).__init__(proxy_str=proxy, w_position=w_position)

        self.base_url = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
        self.email = email
        self.pwd = pwd
        self.skip_for_now = True

    def check_pass(self, email, pwd):
        resp = False
        try:
            self.browser.get(self.base_url)
            input_mail = self.browser_wait.until(EC.presence_of_element_located((By.ID, 'identifierId')))
            input_mail.send_keys(email)
            but_next = self.browser_wait.until(EC.presence_of_element_located((By.ID, 'identifierNext')))
            but_next.click()
            time.sleep(3)
            input_pwd = self.browser_wait.until(EC.presence_of_element_located((By.ID, 'password')))
            input_pwd.send_keys(pwd)
            time.sleep(1)
            but_sig = self.browser_wait.until(EC.presence_of_element_located((By.ID, 'passwordNext')))
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
            
            return 1, False
        except Exception as e:
            return None, False
    def test(self):
        self.browser.get(self.base_url)
        input("...Wait...")

    def run(self):
        _id, _is_success = self.check_pass(self.email, self.pwd)
        time.sleep(2)
        try:
            self.browser.quit()
            print(_id, _is_success)
        except Exception as e:
            pass
        return _id, _is_success

if __name__ == '__main__':
    try:
        br =  Check_Mail(email='dottydot.martinyo', pwd='Nguyen&Thinh@Dn20CK')
        print(br.run())
    except Exception as e:
        print(str(e))