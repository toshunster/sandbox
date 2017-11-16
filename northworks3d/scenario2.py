#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import time

from utils import read_last_email, get_links, logger, Requester, auth_3dhub
from config import NAME_3DHUBS, PASSWORD_3DHUBS

if __name__ == "__main__":
    logger.info( "Start '{}' script.".format( sys.argv[0] ) )
    logger.debug( "Read last email." )
    message_body = read_last_email()
    links_from_message = get_links( message_body )

    ignore_links_from_message = True
    if ignore_links_from_message and len( links_from_message ) == 0:
        logger.error( "There are no links in email body." )
        sys.exit( 1 )
    
    requester = Requester()
    logger.debug( "Authorizate via account '{}'.".format( NAME_3DHUBS ) )
    auth_3dhub( requester, NAME_3DHUBS, PASSWORD_3DHUBS )
    time.sleep(1)
    if not ignore_links_from_message:
        link = links_from_message[0]
        logger.debug( "Go to link [{}].".format( link ) )
        requester.get( link )
        sys.exit( 0 )
    logger.debug( "Go to 'My orders'." )
    requester.browser.find_element_by_xpath("//a[contains(text(), 'My orders')]").click()
    time.sleep(1)
    logger.debug( "Go to 'View profile'." )
    requester.browser.find_element_by_xpath("//div/a[contains(text(), 'View profile')]").click()
    time.sleep(1)
    
    # Switch to first tab and close it
    logger.debug( "Switch to first tab and close it." )
    window_before = requester.browser.window_handles[0]
    requester.browser.switch_to_window(window_before)
    requester.browser.close()

    time.sleep(1)
    # Switch to new tab.
    logger.debug( "Switch to new tab." )
    requester.browser.switch_to_window( requester.browser.window_handles[0] )
    
    logger.debug( "Click on 'Contact' button." )
    requester.browser.find_element_by_xpath("//div/button[contains(text(), 'Contact')]").click()
    
    message = 'This is a test message using the automated rules-based python script. This is not a real inquiry.'
    logger.debug( "Send message '{}'.".format( message ) )
    requester.browser.find_element_by_class_name("h3d-form-group__input").send_keys( message )
    time.sleep(0.5)
    # TODO: Uncomment when you will be ready.
    #requester.browser.find_element_by_xpath("//form[@name='vm.enquiryForm']/div/button").click()
    
    logger.info( "Successfully send test message via login." )