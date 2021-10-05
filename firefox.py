import os
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options as Firefox_Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import UnexpectedAlertPresentException

class Geckodriver(object):
    def __init__(self):

        self.options = webdriver.FirefoxOptions()
        self.options.set_preference("permissions.default.image", 2)
        self.options.set_preference("dom.webdriver.enabled", False)
        self.browser = webdriver.Firefox(executable_path='bin/geckodriver.exe', options=self.option)
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(400, 800)
        self.browser_wait = WebDriverWait(self.browser, 10)