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

    if len( links_from_message ) == 0:
        logger.error( "There are no links in email body." )
        sys.exit( 1 )
    
    requester = Requester()
    auth_3dhub( requester, NAME_3DHUBS, PASSWORD_3DHUBS )
    time.sleep(5)
    requester.get( links_from_message[0] )
    time.sleep(5)
