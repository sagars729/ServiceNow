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

def runtests():
    os.system("winpty -Xallow-non-tty ~/Downloads/python-3.8.2-embed-amd64/Scripts/pytest.exe > log")
    os.system("sed 's/\\?//g' log > log.txt")
    os.system("sed 's/\\x1b\\[[0-9;]*[a-zA-Z]//g' log.txt > log2.txt")
    os.system("mv log2.txt log.txt")

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

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw' : raw}

def send_message(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message)
           .execute())
    print('Message Id: %s' % message['id'])
    return message

service = get_service()
message = create_message("sagardsaxena@gmail.com", "ssaxena1@terpmail.umd.edu", "Test", "Test")
send_message(service, "me", message)


#every = 3600 * 3
#while True:
#    dt = time.time()
#    runtests()
#    dt = time.time() - dt
#    time.sleep(every - dt)

