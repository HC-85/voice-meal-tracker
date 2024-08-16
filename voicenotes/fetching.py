from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from os import getenv, listdir, remove as remove_file
from os.path import exists, join as path_join
from requests import get as requests_get
from datetime import timezone, timedelta
from typing import List, Union
import aiohttp
import asyncio


def get_client(ids=None)->Client:
   match ids:   
      case {'username': str(_), 'password': str(_)}:
          pass
      case None:
        ids = {
           'username': getenv('TWILIO_ACCOUNT_SID'),
           'password': getenv('TWILIO_AUTH_TOKEN')
           }
      case _:
          raise ValueError(f"Unexpected format: {ids}")
   client = Client(**ids)
   return client


def fetch_media_messages(client:Client, mode:str='list')->List[MessageInstance]:
   messages = client.messages
   match mode:
      case 'stream':
         msgs = messages.stream()
         messages_with_media = (msg for msg in msgs if msg.num_media != "0")
      case 'list':
         msgs = messages.list()
         messages_with_media = [msg for msg in msgs if msg.num_media != "0"]
      case _:
         raise ValueError(f'Invalid mode {mode}')
   return messages_with_media


def is_valid_int_string(s:str)->bool:
   try:
      int(s)
      return True
   except:
      return False


def get_timestamp(message:MessageInstance, tz:Union[timezone, str]=None)->str:
   match tz:
      case timezone(_):
         pass
      case str() as s if is_valid_int_string(''.join(offset:=s[-2:])) and s.startswith('UTC'):
        tz = timezone(timedelta(hours=int(offset)))
      case None:
         tz = timezone(timedelta(hours=-6))
      case _:
         raise ValueError(f"Invalid timezone: {tz}")
   timestamp = message.date_sent.astimezone(tz).strftime("%Y-%m-%d_%H-%M")
   return timestamp  


def extract_audio(message:MessageInstance, client:Client, cache_dir:str='voicenotes/fetched') -> str:
   media_item = client.messages(message.sid).media.list()[0]
   media_url = f'https://api.twilio.com{media_item.uri}'.replace('.json', '')
   response = requests_get(media_url, auth=(client.account_sid, client.password))
   
   if status_code:= response.status_code != 200:
      return f"Status code: {status_code}"

   if content_type:= response.headers['Content-Type'].startswith('audio/'):
      file_extension = response.headers['Content-Type'].split('/')[1] 
      timestamp = get_timestamp(message)      
      filename = f'{timestamp}_{media_item.sid[:5]}.{file_extension}'

      if not exists(file_path := path_join(cache_dir, filename)):
         with open(file_path, 'wb') as f:
            f.write(response.content)

         return f'File saved: {filename}'
      
      else:
         return f"File {filename} found in cache. Skipping download."
      
   else:
      return f"Message does not contain an audio file. Content-type header: {content_type}"


def fetch_voicenotes(client:Client=None):
   if client is None:
      client = get_client()

   messages = fetch_media_messages(client)
   log = []
   for msg in messages:
      ret = extract_audio(msg, client)
      log.append(ret)
   return log


def clear_cache(cache_dir:str='voicenotes/fetched') -> str:
   log = []
   for filename in listdir(cache_dir):
      try:
         remove_file(path_join(cache_dir, filename))
         log.append(f'Successfully removed {filename}')
      except:
         log.append(f'Unable to remove {filename}')
   return log


### ASYNC ###
async def extract_audio_async(session, message:MessageInstance, client:Client, cache_dir:str='voicenotes/fetched') -> str:
   media_item = client.messages(message.sid).media.list()[0]
   media_url = f'https://api.twilio.com{media_item.uri}'.replace('.json', '')
   auth = aiohttp.BasicAuth(client.account_sid, client.password)

   async with session.get(media_url, auth=auth) as response:
      #if status_code:= response.status_code != 200:
      #   return f"Status code: {status_code}"

      if content_type:= response.headers['Content-Type'].startswith('audio/'):
         file_extension = response.headers['Content-Type'].split('/')[1] 
         timestamp = get_timestamp(message)      
         filename = f'{timestamp}_{media_item.sid[:5]}.{file_extension}'

         if not exists(file_path := path_join(cache_dir, filename)):
            audio_file = await response.read()
            with open(file_path, 'wb') as f:
               f.write(audio_file)

            return f'File saved: {filename}'
         
         else:
            return f"File {filename} found in cache. Skipping download."
         
      else:
         return f"Message does not contain an audio file. Content-type header: {content_type}"
   

async def fetch_voicenotes_async(client:Client=None):
   if client is None:
      client = get_client()
   messages = fetch_media_messages(client)
   async with aiohttp.ClientSession() as session:
      tasks = []
      for msg in messages:
         tasks.append(asyncio.ensure_future(extract_audio_async(session, msg, client)))
      log = await asyncio.gather(*tasks)
      return log

def async_fetch():
   log = asyncio.run(fetch_voicenotes_async())
   return log