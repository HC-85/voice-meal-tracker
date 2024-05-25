from twilio.rest import Client
from os import getenv, exists
import requests


def fetch_voicenotes(save_path:str):
  account_sid = getenv('TWILIO_ACCOUNT_SID')
  auth_token = getenv('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  messages = client.messages.list()

  for msg in messages:
    if msg.num_media != "0":
      media_item = client.messages(msg.sid).media.list()[0]
      media_item.sid

      media_url = f'https://api.twilio.com{media_item.uri}'.replace('.json', '')
      response = requests.get(media_url, auth=(account_sid, auth_token))
      
      if response.headers['Content-Type'].startswith('audio/'):  
        file_extension = response.headers['Content-Type'].split('/')[1]  
        
        if exists(file_path := save_path + f'{media_item.sid}.{file_extension}'):
          continue

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f'File saved: {media_item.sid}.{file_extension}')
        print('Length: ', response.headers['Content-Length'])
        #print('Date: ', response.headers['Date'])
        #print('Last-Modified: ', response.headers['Last-Modified'], '\n')
