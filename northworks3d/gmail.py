# -*- coding: utf-8 -*-

import os
import sys

import email
import logging
import imaplib

from config import GMAIL_LOGIN, GMAIL_PASSWORD

FORMAT = '[%(asctime)s] [%(levelname)s] - %(message)s'
logger = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter( FORMAT ))
out_hdlr.setLevel(logging.DEBUG)
logger.addHandler(out_hdlr)
logger.setLevel(logging.DEBUG)

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = '993'
IMAP_USE_SSL = True

class GmailBox:

    def __init__( self, username, password ):
        self.username = username
        self.password = password
        self.imap = imaplib.IMAP4_SSL( IMAP_SERVER )
    
    def __enter__( self ):
        self.imap.login( self.username, self.password )
        return self
    
    def __exit__(self, type, value, traceback):
        self.imap.close()
        self.imap.logout()
    
    def get_latest_message( self ):
        self.imap.select( "inbox" )
        result, data = self.imap.search( None, 'ALL' )

        #retrieves the latest (newest) email by sequential ID
        ids = data[0]
        id_list = ids.split()
        print( ids )
        latest_email_id = id_list[-1]

        # Fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc.
        resp, data = self.imap.fetch(latest_email_id, "(RFC822)")
        logger.info( "UID: [{}]".format( latest_email_id ) )
        # Getting the mail content.
        email_body = data[0][1]
        # Parsing the mail content to get a mail object.
        email_message = email.message_from_string( email_body.decode('utf-8') )
        return email_message
    
    # New mail generator --> yield after each mail to save resources.
    def get_messages_by_uid( self, uid ):
        # Issue the search command of the form "SEARCH UID 42:*" or "ALL".
        command = "UID {}:*".format( uid ) if uid is not None else "ALL"
        self.imap.select( "inbox" )
        result, data = self.imap.search( None, command )
        messages = data[0].split()
        # Yield emails.
        for message_uid in messages:
            # SEARCH command *always* returns at least the most
            # recent message, even if it has already been synced
            if uid is None or int(message_uid) > uid:
                result, data = self.imap.uid('fetch', message_uid, '(RFC822)')
                # Getting the mail content.
                email_body = data[0][1]
                # yield raw mail body.
                yield message_uid, email.message_from_string( email_body.decode('utf-8') )
        return dict()

LAST_UID_FILE_NAME = 'last_uid.txt'

if __name__ == "__main__":
    if len( sys.argv ) != 2:
        print( "Usage: {0} <rules file>".format( sys.argv[0] ) )
        sys.exit(1)
    rule_file_name = sys.argv[1]
    rules = list()
    with open( rule_file_name, 'r' ) as rule_file:
        for rule_line in rule_file:
            rule, script_file = rule_line.strip().split('\t')
            rules.append( ( rule, script_file ) )
        logger.info('Read {} rules.'.format( len(rules) ))
    logger.info( "Success!" )
    uid = None
    if os.path.isfile( LAST_UID_FILE_NAME ):
        try:
            uid = int( open( LAST_UID_FILE_NAME, 'r' ).read().strip() )
        except:
            logger.warning( "Can't open {} file. Start read email from begin.".format( LAST_UID_FILE_NAME ) )
    # Logs in to the desired account and navigates to the inbox.
    try:
        with GmailBox( GMAIL_LOGIN, GMAIL_PASSWORD ) as gmail:
            #message = gmail.get_latest_message()
            #uid = None
            #uid = 5
            for message_uid, message in gmail.get_messages_by_uid( uid ):
                print( message_uid, message.get('Subject', None) )
                uid = message_uid
    except imaplib.IMAP4.error as e:
        logger.error( "imaplib.IMAP4.error: {}".format( str(e) ) )
        sys.exit(1)
    except Exception as e: 
        logger.error( "Unknown exception: {}".format( str(e) ) )
        sys.exit(1)
    
    with open( LAST_UID_FILE_NAME, 'w' ) as output:
        output.write( str(int(uid)) )
    #print( email_message['To'] )
    #print( email_message['From'] )
