import asyncio
import time
import os
import glob
from Hentai import ses
import libtorrent as lt
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .progress import *
from .parser import *

async def downloader(m=None, ab=None):
  link = ab
  params = {
  'save_path': './',
  'storage_mode': lt.storage_mode_t(2),}

  handle = lt.add_magnet_uri(ses, link, params)
  ses.start_dht()

  r = await m.reply_text('Downloading Metadata...')
    
  while (not handle.has_metadata()):
    
    await asyncio.sleep(1)
    
  await r.edit('Got Metadata, Starting Torrent Download...')

  await r.edit(f"Starting   **{str(handle.name())}**")
  trgt = str(handle.name())

  while (handle.status().state != lt.torrent_status.seeding):
    
    s = handle.status()
    
    state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
    
    try:
      
      await r.edit(
        text="**Name**: **{}**\n\n**Status**: `{}`\n**Completed** : `{}%` \n\n**Down**: `{} KiB/s` | **Up**: `{} KiB/s` \n**Peers**: `{}`".format(
          trgt, 
          str(state_str[s.state]).capitalize(), 
          round(s.progress * 100, 2),
          round(s.download_rate / 1000, 1),
          round(s.upload_rate / 1000, 1),
          s.num_peers
        )
      )
    except:
      pass
    print(str(s))
        #print(s.state)
    await asyncio.sleep(5)
  fuk = is_file(trgt)
  if fuk:
    c_time = time.time()
    z = await r.reply_document(
      document=trgt,
      caption=os.path.basename(trgt),
      progress=progress_for_pyrogram,
      progress_args=(
        f"STARTING TO UPLOAD {os.path.basename(trgt)}...",
        r,
        c_time
      )
    )
    os.remove(trgt)
  else:
    trg = f"{trgt}/*"
    x = glob.glob(trg)
    for tr in x:
      c_time = time.time()
      z = await r.reply_document(
        document=tr,
        caption=os.path.basename(tr),
        progress=progress_for_pyrogram,
        progress_args=(
          f"STARTING TO UPLOAD {os.path.basename(tr)}...",
          r,
          c_time
        )
      )
      os.remove(tr)
      await asyncio.sleep(2)
    os.rmdir(trgt)
  await z.reply_text(f"**Your Porno Has Been uploaded @{m.from_user.username}**")
  try:
    await r.delete()
    os.remove(trgt)
  except:
    return
  return
