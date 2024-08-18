from os import getenv, listdir, remove as remove_file
from os.path import exists, join as path_join

from datetime import timezone, timedelta

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

from requests import get as requests_get

from aiohttp import BasicAuth, ClientSession
from asyncio import run as run_async, ensure_future, gather as gather_futures

from typing import List, Coroutine, Dict


def extract_audio_sync(message:MessageInstance, client:Client, cache_dir:str='voicenotes/vn_cache') -> str:
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


def fetch_voicenotes_sync(client:Client=None)->List[str]:
   if client is None:
      client = get_client()

   messages = fetch_media_messages(client)
   log = []
   for msg in messages:
      ret = extract_audio(msg, client)
      log.append(ret)
   return log


def get_client(ids=None, return_auth:bool=False)->Client:
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
   if return_auth:
      auth = BasicAuth(*ids.values())
      return client, auth
   else:
      return client


def is_valid_int_string(s:str)->bool:
   try:
      int(s)
      return True
   except:
      return False


def get_timestamp(message:MessageInstance, tz: timezone | str | None = None) -> str:
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


def clear_cache(cache_dir:str='voicenotes/vn_cache') -> List[str]:
   log = []
   for filename in listdir(cache_dir):
      try:
         remove_file(path_join(cache_dir, filename))
         log.append(f'Successfully removed {filename}')
      except:
         log.append(f'Unable to remove {filename}')
   return log


### ASYNC ###
async def extract_audio(session:ClientSession,
                        message:MessageInstance, 
                        auth:BasicAuth,
                        cache_dir:str='voicenotes/vn_cache'):

   if message.num_media == '0':
      return f"Message {message.sid} contains no media."

   media_url = f'https://api.twilio.com{message.media.list()[0].uri}'.replace('.json', '')
   
   async with session.get(media_url, auth=auth) as response:
      #if status_code:= response.status_code != 200:
      #   return f"Status code: {status_code}"

      if content_type:= response.headers['Content-Type'].startswith('audio/'):
         file_extension = response.headers['Content-Type'].split('/')[1] 
         timestamp = get_timestamp(message)      
         filename = f'{timestamp}_{message.sid}.{file_extension}'

         if not exists(file_path := path_join(cache_dir, filename)):
            audio_file = await response.read()
            with open(file_path, 'wb') as f:
               f.write(audio_file)

            return f'File saved: {filename}'
         
         else:
            return f"File {filename} found in cache. Skipping download."
         
      else:
         return f"Message does not contain an audio file. Content-type header: {content_type}"
   

async def fetch_voicenotes(ids: Dict[str, str] | None = None)->Coroutine[None,None,List[str]]:
   client, auth = get_client(ids, return_auth=True)
   async with ClientSession() as session:
      tasks = []
      for message in client.messages.stream():
         tasks.append(ensure_future(extract_audio(session, message, auth)))
      log = await gather_futures(*tasks)
      return log


def fetch() -> List[str]:
   log = run_async(fetch_voicenotes())
   return log