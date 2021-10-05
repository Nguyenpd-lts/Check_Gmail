
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

from undetected_chromedriver.options import ChromeOptions
import undetected_chromedriver.v2 as uc

class UChromeBrowser():
    def __init__(self, proxy_str=None, is_headless=False, w_position=None):
        self.options = uc.ChromeOptions()
        #setting profile
        # self.options.add_argument('--user-data-dir=C:/Users/Dinh Nguyen/AppData/Local/Google/Chrome/User Data')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--mute-audio')
        self.options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.options.add_argument('--user-agent="{}"'.format('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'))
        if proxy_str != None:
            self.options.add_argument('--proxy-server=http://{}'.format(proxy_str))
        if w_position and len(w_position) == 4:
            self.options.add_argument('--window-size={},{}'.format(w_position[2], w_position[3]))
            self.options.add_argument('--window-position={},{}'.format(w_position[0], w_position[1]))
        else:
            self.options.add_argument('--window-size={},{}'.format(400, 800))

        self.browser = uc.Chrome(options=self.options, executable_path="chromedriver.exe")
        self.browser_wait = WebDriverWait(self.browser, 3600)
        self.short_wait = WebDriverWait(self.browser, 5)


class ChromeBrowser():
    def __init__(self, proxy_str=None, is_headless=False, w_position=[0, 0, 300, 500]):


        self.options = webdriver.ChromeOptions() 
        # self.options = uc.ChromeOptions()
        #setting profile
        # self.options.add_argument('--user-data-dir=C:/Users/Dinh Nguyen/AppData/Local/Google/Chrome/User Data')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--mute-audio')
        self.options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.options.add_argument('--user-agent="{}"'.format('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'))
        if proxy_str != None:
            self.options.add_argument('--proxy-server=http://{}'.format(proxy_str))
        if w_position and len(w_position) == 4:
            self.options.add_argument('--window-size={},{}'.format(w_position[2], w_position[3]))
            self.options.add_argument('--window-position={},{}'.format(w_position[0], w_position[1]))
        else:
            self.options.add_argument('--window-size={},{}'.format(400, 800))
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        self.browser_wait = WebDriverWait(self.browser, 3600)
        self.short_wait = WebDriverWait(self.browser, 5)