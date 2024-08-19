from os import getenv, listdir, remove as remove_file
from os.path import exists, join as path_join, dirname

from datetime import timezone, timedelta

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

from requests import get as requests_get

from aiohttp import BasicAuth, ClientSession
from asyncio import run as run_async, ensure_future, gather as gather_futures

from typing import List, Coroutine, Dict


CACHE_DIR = path_join(dirname(__file__), 'vn_cache')


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


def clear_cache(cache_dir:str=CACHE_DIR) -> List[str]:
   logs = []
   for filename in listdir(cache_dir):
      try:
         remove_file(path_join(cache_dir, filename))
         logs.append(f'Successfully removed {filename}')
      except:
         logs.append(f'Unable to remove {filename}')
   return logs


### ASYNC ###
async def extract_audio(session:ClientSession,
                        message:MessageInstance, 
                        auth:BasicAuth,
                        cache_dir:str=CACHE_DIR):

   if message.num_media == '0':
      return f"Message {message.sid} contains no media."

   media_url = f'https://api.twilio.com{message.media.list()[0].uri}'.replace('.json', '')
   
   async with session.get(media_url, auth=auth) as response:
      if (status:= response.status) != 200:
         return f"Status code: {status}"

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
   

async def fetch(ids: Dict[str, str] | None = None)->Coroutine[None,None,List[str]]:
   client, auth = get_client(ids, return_auth=True)
   async with ClientSession() as session:
      tasks = []
      for message in client.messages.stream():
         tasks.append(ensure_future(extract_audio(session, message, auth)))
      logs = await gather_futures(*tasks)
      return logs


def run_fetch() -> List[str]:
   logs = run_async(fetch())
   return logs