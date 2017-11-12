#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

from config import GMAIL_LOGIN, GMAIL_PASSWORD
from utils import logger

TO_EMAIL = 'webmaster@northworks3d.com'

def create_message( subject, to, body ):
    msg = EmailMessage()
    msg.set_content( body )

    msg['Subject'] = subject
    msg['From'] = GMAIL_LOGIN
    msg['To'] = to
    return msg

if __name__ == "__main__":
    logger.info( "Start '{}' script.".format( sys.argv[0] ) )
    # Create a text/plain message
    mail_subject = 'New Congrats email'
    mail_body = 'sample text'
    to_mail = 'toshun@mail.ru'
    msg = create_message( mail_subject, to_mail, mail_body )

    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL( 'smtp.gmail.com', 465 ) as smtp_server:
        smtp_server.login( user=GMAIL_LOGIN, password=GMAIL_PASSWORD )
        smtp_server.send_message( msg )
    