from Hentai import mio, START_TIME, MIO_NAME, MIO_USERNAME, MIO_ID, SUDO_CHATS
from config import SUDOERS
from pyrogram import __version__ as pyrover
from platform import python_version as pyver
from Hentai.strings import *
from Hentai.helpers.progress import TimeFormatter
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import time
import os
import random
from Hentai.helpers import *


TYPES = [
  {
    'key': '1_1',
    'name': 'Art - Anime'
  }, 
  {
    'key': '1_2',
    'name': 'Art - Doujinshi'
  },
  {
    'key': '1_3',
    'name': 'Art - Games'
  },
  {
    'key': '1_4',
    'name': 'Art - Manga'
  },
  {
    'key': '1_5',
    'name': 'Art - Pictures'
  },
  {
    'key': '2_1',
    'name': 'Real Life - Pictures'
  },
  {
    'key': '2_2',
    'name': 'Real Life - Videos'
  }
]






@mio.on_message(filters.command(["start", f"start@{MIO_USERNAME}"]) & filters.chat(SUDO_CHATS))
async def _starr(_, message):
  await message.reply_text(
    text=START_MSG.format(MIO_NAME),
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="HELP",
            callback_data="helpcall"
          ),
          InlineKeyboardButton(
            text="ABOUT",
            callback_data="aboutcall"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )



@mio.on_callback_query(filters.regex("helpcall"))
async def _halp(_, query):
  await query.message.edit(
    text=HELP_MSG,
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="Close",
            callback_data="closecall"
          ),
          InlineKeyboardButton(
            text="ABOUT",
            callback_data="aboutcall"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )


@mio.on_message(filters.command(["help", f"help@{MIO_USERNAME}"]) & filters.chat(SUDO_CHATS))
async def h_halp(_, message):
  await message.reply_text(
    text=HELP_MSG,
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="Close",
            callback_data="closecall"
          ),
          InlineKeyboardButton(
            text="ABOUT",
            callback_data="aboutcall"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )



@mio.on_callback_query(filters.regex("aboutcall"))
async def abot(_, query):
  nt = time.time() - START_TIME
  nt = nt*1000
  nt = TimeFormatter(milliseconds=nt)
  await query.message.edit(
    text=ABOUT_MSG.format(
      pyver,
      pyrover,
      nt
    ),
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="Close",
            callback_data="closecall"
          ),
          InlineKeyboardButton(
            text="HELP",
            callback_data="helpcall"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )


@mio.on_callback_query(filters.regex("closecall"))
async def _close(_, query):
  await query.message.delete()

@mio.on_message(filters.command(["random", f"random@{MIO_USERNAME}"]) & filters.chat(SUDO_CHATS))
async def random_sauce(bot, message):
  x = await feed()
  sauce = random.randint(3381878, int(x["code"]))
  sauce = await get_suke_info(sauce)
  link = sauce['magnet']
  info = mag_parser(sauce)
  print(info)
  return await downloader(m=message, ab=link)

@mio.on_message(filters.command(["latest", f"latest@{MIO_USERNAME}"]) & filters.chat(SUDO_CHATS))
async def random_sauce(bot, message):
  x = await feed()
  sauce = int(x["code"])
  sauce = await get_suke_info(sauce)
  link = sauce['magnet']
  info = mag_parser(sauce)
  print(info)
  return await downloader(m=message, ab=link)



@mio.on_message(filters.command(["send", f"send@{MIO_USERNAME}"]) & filters.chat(SUDO_CHATS))
async def randomsauce(bot, message):
  try:
    msg = message.text.split(" ", maxsplit=1)[1]
  except:
    return await message.reply_text("Usage: \n× /send 10 -> Sends 10 pornos")
  try:
    for z in range(int(msg)):
      x = await feed()
      sauce = random.randint(3381878, int(x["code"]))
      sauce = await get_suke_info(sauce)
      link = sauce['magnet']
      info = mag_parser(sauce)
      print(info)
      await downloader(m=message, ab=link)
      await asyncio.sleep(4)
  except:
    pass
  finally:
    return await message.reply_text(f"Sent {int(msg)} pornos")



@mio.on_message(filters.command(["get", f"get@{MIO_USERNAME}"]) & filters.chat(SUDO_CHATS))
async def send_from_sauce(bot, message):
  try:
    x = message.text.split(" ", maxsplit=1)[1]
  except:
    return await message.reply_text("Usage: \n× /get https://sukebei.nyaa.si/view/3381878 -> Sends porno at the link \n**OR**\n× /send 3381878")
  try:
    if "/" in x:
      sauce = int(x.split("/")[-1])
    else:
      sauce = int(x)
    sauce = await get_suke_info(sauce)
    link = sauce['magnet']
    info = mag_parser(sauce)
    print(info)
    return await downloader(m=message, ab=link)
  except Exception as e:
    return await message.reply_text(text=f"**An Error Occurred**\n\n`{str(e)}`")




@mio.on_message(filters.command(['browse', f'browse@{MIO_USERNAME}']) & filters.chat(SUDO_CHATS))
async def browse(_, message):
  caption = "Please Choose A Category From Below To Browse"
  btns = []
  for a in range(int(len(TYPES))):
    type1 = TYPES[int(a)]
    btn = [
      InlineKeyboardButton(
        text=type1['name'],
        callback_data=f"browser {type1['key']}"
      )
      ]
    btns.append(btn)
  markup=InlineKeyboardMarkup(btns)
  return await message.reply_text(text=caption, reply_markup=markup)


@mio.on_callback_query(filters.regex("browser"))
async def beowc(_, query):
  data = query.data.replace("browser", "")
  for typ in TYPES:
    if data[-3:] in typ['key']:
      opt = typ
    else:
      pass
  opts = await get_by_id(opt['key'], opt['name'])
  se = []
  for a in range(10):
    se.append(random.choice(opts))
  btns = []
  for s in range(int(len(se))):
    in1 = se[int(s)]
    btn = [
      InlineKeyboardButton(
        text=in1['name'],
        callback_data=f"brew{in1['data']}"
      )
    ]
    btns.append(btn)
  return await query.message.edit(text=f"SHOWING RESULTS FOR {opt['name']}", reply_markup=InlineKeyboardMarkup(btns))


@mio.on_callback_query(filters.regex('brew'))
async def brewww(_, query):
  href = query.data.replace("brew", "")
  name = query.message.text.split("FOR ", maxsplit=1)[1]
  data = await get_suke_info(int(href))
  dat = {}
  dat['title'] = data['title']
  dat['size'] = data['File size']
  dat['category'] = name
  dat['get_this_porno'] = f"/get https://sukebei.nyaa.si/view/{href}"
  data = mag_parser(dat)
  return await query.message.edit(data)



@mio.on_message(filters.command("update", f"update@{MIO_USERNAME}") & filters.user("SUDOERS") & filters.chat(SUDO_CHATS))
async def update(_, message):
  await message.reply_text("Trying To Update Please Wait")
  os.system("pkill -9 python3 && git pull && python3 -m Hentai")


if __name__ == '__main__':
  print("=====================================================================\n")
  print("[INFO]: BOT STARTED SUCCESSFULLY")
  print("\n===================== JOIN @VILLAINEVIL_UPDATES =====================")
  for SUDO_CHAT in SUDO_CHATS:
    mio.send_message(SUDO_CHAT, text="I'm Alive Nyaa~")
  idle()
