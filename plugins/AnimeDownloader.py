# Anime Downloader And Uploader Plugin For Ultroid
# Using Animeout.xyz As Base For Downloading And Uploading Animes
# Using AnimeX CLI Tool To Download Animes
# Ported Into Ultroid By @ItzAditya_xD
"""
**Download Any Anime From Animeout.xyz**
**Download Both Sub And Dub Animes**
**Make Sure To Add Anime Name Within Double Quotes**

** •Usage **
{i}animeX <from_episode> <to_episode> "<anime_name>"
** •Example **
`{i}animeX 1 10 "Boruto"`
"""

from telethon import events
from . import *
import os
import sys
import time
import urllib3
import requests
from bs4 import BeautifulSoup

def get_search_result(search_item):
    search_url = "https://www.animeout.xyz/wp-json/wp/v2/posts"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    params = {
        "search": search_item
    }

    search_result = []
    r = requests.get(search_url, params=params, headers=headers).json()

    for post in r:
        post_title = post['title']['rendered']
        if search_item.split(' ', 1)[0].lower() in post_title.lower():
            print(post_title)
            search_result.append({
                'name': post_title,
                'raw-content': post['content']['rendered']
            })

    return search_result    

def get_anime_episodes(anime_content):
    anime_result = BeautifulSoup(anime_content, "html.parser")

    episodes = []
    for i in anime_result.findAll("a"):
        try:
            if i["href"][-3:] in ["mkv", "mp4]"]:
                episodes.append(i["href"])
        except:
            pass
    return episodes

def make_directory(anime_name):
    if not os.path.exists(anime_name):
        os.mkdir(anime_name)

def get_download_url(anime_url):
    r = requests.get(anime_url)
    pre_download_page = BeautifulSoup(r.text, "html.parser")
    pre_download_url = pre_download_page.find("a", {"class": "btn"})["href"]
    r = requests.get(pre_download_url)
    download_page = BeautifulSoup(r.text, "html.parser")
    try:
        download_url = download_page.find("script", {"src": None}).text.split('"')[1]
    except:
        download_url = download_page.find("script", {"src": None}).contents[0].split('"')[1]
    return download_url

def download_episode(anime_name, download_url, i=1):
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    filename = os.path.basename(download_url)
    download_path = os.path.join(anime_name, filename)
    if not os.path.exists(download_path):
        _url = download_url.replace(" ", "%20")
        _url = "https://pub" + str(i) + ".animeout.com" + \
            _url[_url.find('/series'):]
        print("\nTrying " + _url + " ...")
        try:
            r = http.request('GET', _url, preload_content=False)
            if r.status == 404:
                raise BadLinkException('bad link')
            print('Gotten Verified Download link!')
            print("Downloading", name_parser(filename))
            with open(download_path, 'wb') as out:
                while True:
                    data = r.read()
                    if not data:
                        break
                    out.write(data)
            r.release_conn()
            clear_tmp(anime_name)
        except BadLinkException as e:
            print(e)
            n = i + 1
            download_episode(anime_name, download_url, n)

class BadLinkException(Exception):
    def __init__(self, ok):
        self.ok = ok

def name_parser(name):
    new_name = ("]".join(name.split("]")[1:2]) + "]").strip()
    if new_name in ["[RapidBot]", "[]"]:
        new_name = os.path.basename(name)
    return new_name

def clear_tmp(directory):
    for i in os.listdir(directory):
        if i[-3:] == "tmp":
            os.remove(os.path.join(directory, i))

@ultroid_cmd(pattern="animeX(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+\"(.+)\")?")
async def animeX(event):
    from_episode = event.pattern_match.group(1)
    to_episode = event.pattern_match.group(2)
    anime_name = event.pattern_match.group(3)
    if not from_episode or not to_episode:
        await event.reply("⚠️ Specific Number Of Episode To Download")
        return
    await event.message.edit("🔍Searching for links...")
    search_result = get_search_result(anime_name)
    if len(search_result) == 0:
        await event.reply("❌ We couldn't find the anime you searched for, check the spelling and try again")
        return
    anime = search_result[0]
    anime["name"] = "".join(
        [i if i.isalnum() or i in [")", "(", " "] else "-" for i in anime["name"]])
    episodes = get_anime_episodes(anime["raw-content"])
    episodes = episodes[int(from_episode) - 1:int(to_episode)]
    make_directory(anime["name"])    
    for i in episodes:
        await event.message.edit(f"⚡Downloading episode `{i}`...")       
        download_url = get_download_url(i)
        download_episode(anime["name"], download_url)
        filename = os.path.basename(download_url)
        download_path = os.path.join(anime["name"], filename)
        file, _ = await event.client.fast_uploader(
            download_path, show_progress=True, event=event
        )
        await event.client.send_file(
            event.chat_id,
            file,
            force_document=True,
            caption=f"{filename}",
            reply_to=event.reply_to_msg_id or event,
        )
        os.remove(download_path)
    await event.message.delete()
    msg = await event.reply(f"🔥Finished downloading episodes {from_episode} to {to_episode} of {anime_name}")
    await asyncio.sleep(10)
    await msg.delete()
