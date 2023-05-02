import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage


""" Environment variable used"""
load_dotenv()
email_address = os.environ['EMAIL']
email_password = os.environ['EMAIL_PASSWORD']
email_server = os.environ['GMAIL']



""" Function to send email for a temporary passcode login option """


def mail_sender(email, tempcode):
    gmail_server = email_server
    sender_email = email_address
    port = 465
    password = email_password
    receiver_email = email
    msg = EmailMessage()
    msg['Subject'] = "Temporary passcode  "
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Your Temporary passcode is   " + str(tempcode))
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(gmail_server, port, context=context)
    server.login(sender_email, password)
    server.send_message(msg)


