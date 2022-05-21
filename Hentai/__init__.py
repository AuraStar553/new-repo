from config import *
from pyrogram import Client
import os
import time
import libtorrent as lt


mio = Client(
  "MIO HENTAI",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=TOKEN
)
print("[INFO]: STARTING MIO NARUSE...")

mio.start()
START_TIME = time.time()

print("[INFO]: GETTING INFO FOR MIO")
m = mio.get_me()

MIO_NAME = m.first_name + (m.last_name or "")
MIO_USERNAME = m.username
MIO_ID = m.id

print("[INFO]: STARTING LIB TORRENT CLIENT")
ses = lt.session()
ses.listen_on(6881, 6891)