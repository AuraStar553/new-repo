from bs4 import BeautifulSoup as bs
import aiohttp
import feedparser
import zipfile as zippy
import glob


async def get_suke_info(code):
  r = aiohttp.ClientSession()
  suke = await r.get(f"https://sukebei.nyaa.si/view/{code}")
  suke = await suke.text()
  await r.close()
  s = bs(suke, "html.parser")
  title = s.find_all("h3", attrs={"class":"panel-title"})[0]
  link = s.find_all("a", attrs={"class": "card-footer-item"})[0].get("href")
  d1 = s.find_all("div", attrs={"class":"col-md-1"})
  d2 = s.find_all("div", attrs={"class":"col-md-5"})
  title = str(title.string)
  title = title[4:]
  inf = []
  for t in d1:
    num = d1.index(t)
    t = t.string
    t = t[:-1]
    y = d2[num]
    if y.span:
      y = y.span.string
    elif y.a:
      y = y.a.string
    else:
      y = y.string
    sq = [t, y]
    inf.append(sq)
    try:
      if "Information" in t:
        inf.remove([t, y])
      else:
        pass
    except:
      pass
  graph = {}
  graph['title'] = title
  for a in inf:
    graph[f'{a[0]}'] = a[1]
  graph['magnet'] = link 
  return graph



async def feed():
  x = feedparser.parse("https://sukebei.nyaa.si/?page=rss")
  x = x['entries'][0]
  rus = {}
  dic = {}
  code = str(x['link'])
  code = code.replace(".torrent", "")
  code = code.split('/')[-1]
  magnet = await get_suke_info(code)
  magnet = magnet['magnet']
  dic['title'] = x['title']
  dic['code'] =  code
  dic['magnet'] = magnet
  dic['seeders'] = x['nyaa_seeders']
  dic['leechers'] = x['nyaa_leechers']
  dic['downloads'] = x['nyaa_downloads']
  dic['infohash'] = x['nyaa_infohash']
  dic['category'] = x['nyaa_category']
  dic['size'] = x['nyaa_size']
  return dic

def mag_parser(xm):
  tt = ""
  for x in xm:
    y = x
    x = x.replace("_", " ")
    tt += f"<b>{x.capitalize()}:</b> <code>{xm[y]}</code>\n\n"
  return tt

async def get_by_id(id, name):
  e = aiohttp.ClientSession()
  s = await e.get(f"https://sukebei.nyaa.si/?c={id}")
  s = await s.text()
  await e.close()
  soup = bs(s, 'html.parser')
  soup = soup.find_all("td", attrs={"colspan":"2"})
  hrefs = []
  for h in soup:
    href = h.a.get("href")
    href = href.split("/")[-1]
    href = href.replace("#comments", "")
    rut = str(h.a.get("title"))
    hrefs.append({'name':rut[:15], 'data': href})
  return hrefs



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


def is_file(file):
  file = glob.glob(f"{file}/*)
  file = len(file)
  if file == 0:
    return True
  else:
    return False
