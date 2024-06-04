from twilio.rest import Client
from os import getenv
from os.path import exists
import requests
from datetime import datetime, timezone, timedelta
import pdb


def clear_conversation():
  account_sid = getenv('TWILIO_ACCOUNT_SID')
  auth_token = getenv('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  messages = client.messages.list()
  for msg in messages:
    client.messages(msg.sid).delete()
    print(f"Deleted message {msg.sid}")

def fetch_voicenotes(save_path:str):
  tz = timezone(timedelta(hours=-6))

  account_sid = getenv('TWILIO_ACCOUNT_SID')
  auth_token = getenv('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)
  messages = client.messages.list()
  print("Fetching voicenotes...")
  for msg in messages:
    if msg.num_media != "0":
      timestamp = msg.date_sent.astimezone(tz).strftime("%Y-%m-%d_%H-%M")
      media_item = client.messages(msg.sid).media.list()[0]

      media_url = f'https://api.twilio.com{media_item.uri}'.replace('.json', '')
      response = requests.get(media_url, auth=(account_sid, auth_token))
      
      if response.headers['Content-Type'].startswith('audio/'):  
        file_extension = response.headers['Content-Type'].split('/')[1]  
        
        if exists(file_path := save_path + f'{timestamp}_{media_item.sid[:5]}.{file_extension}'):
          continue

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f'File saved: {file_path}')
        print('Length: ', response.headers['Content-Length'])
        #print('Date: ', response.headers['Date'])
        #print('Last-Modified: ', response.headers['Last-Modified'], '\n')
