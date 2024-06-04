from os import getenv, listdir, remove as remove_file
from os.path import join as path_join
from twilio.rest import Client
import sqlite3

def clear_conversation():
  account_sid = getenv('TWILIO_ACCOUNT_SID')
  auth_token = getenv('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  messages = client.messages.list()
  for msg in messages:
    client.messages(msg.sid).delete()
    print(f"Deleted message {msg.sid}")


def delete_last_n_messages(n):
  account_sid = getenv('TWILIO_ACCOUNT_SID')
  auth_token = getenv('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  messages = client.messages.list()
  for msg in messages[-n:]:
    client.messages(msg.sid).delete()
    print(f"Deleted message {msg.sid}")


def drop_log():
    query =  "DROP TABLE food_idxs"
    with sqlite3.connect('/mnt/local/food_log.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)


def clear_vn_cache():
    dir = "audio_input/voicenotes"
    for filename in listdir(dir):
        remove_file(path_join(dir, filename))