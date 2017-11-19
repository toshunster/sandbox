#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import logging
from selenium import webdriver
from pyvirtualdisplay import Display

try:
    display = Display(visible=0, size=(800, 600))
    display.start()
except:
    pass

LAST_EMAIL_FILE_NAME = 'last_email.txt'
URL_PATTERN = re.compile( r'href="(?P<url>[^\"]*?)"' )
URL_2_PATTERN = re.compile( r'(https?://\S+)' )

FORMAT = '[%(asctime)s] [%(levelname)s] - %(message)s'
logger = logging.getLogger('main')
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter( logging.Formatter( FORMAT, "%Y-%m-%d %H:%M:%S" ) )
out_hdlr.setLevel( logging.DEBUG )
logger.addHandler( out_hdlr )
logger.setLevel( logging.DEBUG )

action_logger = logging.getLogger('action_logger')
action_logger_hdlr = logging.FileHandler('action.log', mode='a')
formatter = logging.Formatter('%(asctime)s  %(message)s', "%Y-%m-%d %H:%M:%S")
action_logger_hdlr.setFormatter(formatter)
action_logger.setLevel( logging.DEBUG )
action_logger.addHandler( action_logger_hdlr )


def auth_3dhub( requester, name, password ):
    LOGIN_URL = "https://www.3dhubs.com/user?destination=home%3Faction"
    requester.get( LOGIN_URL )
    # Get elements and fill inputs.
    requester.browser.find_element_by_id( 'edit-name' ).send_keys( name )
    requester.browser.find_element_by_id( 'edit-pass' ).send_keys( password )
    # Click 'Log in' button.
    requester.browser.find_element_by_id( 'edit-submit' ).click()
    
class Requester:
    DELAY = 1 # seconds
    def __init__(self):
        # Chrome
        self.browser = self.init_chrome()
        # PhatnomJS
        #self.browser = self.init_phantomjs()
        # Firefox
        #self.browser = self.init_firefox()
        self.browser.set_page_load_timeout(60)
        #self.browser.delete_all_cookies()
        #self.authorize()
        pass
    
    def init_firefox(self):
        gecko = "./geckodriver"
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        return webdriver.Firefox( firefox_profile, executable_path=gecko)

    def init_phantomjs(self):
        desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        desired_capabilities['phantomjs.page.settings.userAgent'] = user_agent
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = user_agent
        desired_capabilities['phantomjs.page.customHeaders.customHeaders'] = \
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Content-type': 'text/html',
             'Accept-Encoding': 'gzip, deflate, sdch',
             'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
             'Cache-Control': 'max-age=0'}
        browser = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
        browser.maximize_window()
        browser.implicitly_wait(40)
        return browser

    def init_chrome(self):
        # Path to chromdriver.
        chromedriver = "/opt/google/chrome/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        # Disable images.
        prefs = { "profile.managed_default_content_settings.images" : 2 }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--lang=en-us')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option( "prefs", prefs )
        browser = webdriver.Chrome( executable_path=chromedriver, chrome_options=chrome_options )
        return browser

    def get(self, url):
        self.browser.get( url )
        time.sleep( self.DELAY )
    
    def html_content(self):
        return self.browser.page_source

    def __del__(self):
        try:
            self.browser.quit()
        except:
            pass

def get_links( text ):
    return [ url.strip() for url in URL_PATTERN.findall( text ) + URL_2_PATTERN.findall( text ) if url.strip() != "" ]

def save_email( body_, from_=None, to_=None ):
    with open( LAST_EMAIL_FILE_NAME, 'w' ) as output_email:
        output_email.write( body_ )

def read_last_email( ):
    with open( LAST_EMAIL_FILE_NAME, 'r' ) as input_email:
        return input_email.read()
