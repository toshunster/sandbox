#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import time

from utils import logger, Requester
NAME_SCRAPING_PRO = 'admin'
PASSWORD_SCRAPING_PRO = '12345'

if __name__ == "__main__":
    logger.info( "Start '{}' script.".format( sys.argv[0] ) )
    
    requester = Requester()
    requester.get( 'http://testing-ground.scraping.pro/login' )

    logger.debug( "Authorizate via account '{}'.".format( NAME_SCRAPING_PRO ) )
    login_element = requester.browser.find_element_by_id( 'usr' )
    password_element = requester.browser.find_element_by_id( 'pwd' )
    login_element.send_keys( NAME_SCRAPING_PRO )
    password_element.send_keys( PASSWORD_SCRAPING_PRO )
    time.sleep(1)

    requester.browser.find_element_by_xpath( '//input[@value="Login"]' ).click()
    time.sleep(15)
    
    logger.info( "Successfully push submit button." )