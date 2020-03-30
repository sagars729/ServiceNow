from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os 
import time

from email.mime.text import MIMEText
import base64
from datetime import datetime

from ansi2html import Ansi2HTMLConverter as a2h
import argparse

import re
from pandas import DataFrame as df

conv = a2h()

def analyze(text):
    passed = re.compile(r"passed.*::(test.*)\x1b", re.IGNORECASE)
    failed = re.compile(r"failed.*::(test.*) - (.*)\x1b", re.IGNORECASE)
    passed = passed.findall(text)
    failed = failed.findall(text)

    failed = [(i[0], ("\033[33mWARNING\033[0m","\033[31mFAILED\033[0m")["assert" in i[1].lower()], i[1]) for i in failed]
    passed = [(i, "\033[32mPASSED\033[0m", "") for i in passed]

    frame = df(data=passed+failed, columns=["Test", "\033[37mStatus\033[0m", "Message"])

    return frame.to_string()

def runtests():
    dt = time.time()
    os.system("winpty -Xallow-non-tty ~/Downloads/python-3.8.2-embed-amd64/Scripts/pytest.exe -rA > log")
    #os.system("sed 's/\\?//g' log > log.txt")
    #os.system("sed 's/\\x1b\\[[0-9;]*[a-zA-Z]//g' log.txt > log2.txt")
    #os.system("mv log2.txt log.txt")
    return time.time() - dt

def get_service():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(subject, message_text, typ="plain"):
  message = MIMEText(message_text, typ)
  message['to'] = args.to
  message['from'] = args.sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw' : raw}

def send_message(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message)
           .execute())
    print('Message Id: %s' % message['id'])
    return message

def cycle(t, email=False):
    while True:
        dt = runtests()
        
        if email:
            service = get_service()
            with open("log", "r") as infile:
                ansi = "".join(infile.readlines())
                ansi = analyze(ansi) + "\n" + ansi 
                html = conv.convert(ansi)
                infile.close()

            message = create_message("Automated Pytest Report %s" % (datetime.now().strftime("%H:%M:%S")), html, "html") 
            send_message(service, "me", message)
        
        time.sleep(t - dt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program allows you to run automated tests and email logs at set intervals.')
    parser.add_argument('--sender', type=str, default="sender@gmail.com", help="Email that sends the logs")
    parser.add_argument('--to', type=str, default="receiver@gmail.com", help="Email that receives the logs")
    parser.add_argument('--interval', type=float, default=3, help="Interval In Hours")
    args = parser.parse_args()
    
    cycle(3600*args.interval, True)
