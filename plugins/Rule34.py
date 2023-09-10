"""
{i}rule34 <keyword>
"""
from telethon import events
import math
import requests
import xml.etree.ElementTree as XML_ET
from plugins.http import http_download
from . import *

class Rule34:
    def __init__(self, tags: list):
        self.__tags = tags

    @property
    def tags(self):
        return self.__tags

    def api_url_builder(self, pid: int = 0, limit: int = 100):
        return "https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}&pid={}&limit={}".format(",".join(self.tags), pid, limit)

    def export(self):
        pid = 0
        limit = 100
        while True:
            url = self.api_url_builder(pid=pid)
            data = requests.get(url).text
            data = XML_ET.fromstringlist([data])
            total_posts = int(data.get("count"))
            posts = data.iter("post")
            for post in posts:
                yield post.get("file_url")
            pid_limit = math.ceil(total_posts / limit)
            if pid_limit == pid:
                break
            pid += 1

    def download_file(self, url: str, output: str):
        http_download(url, output, custom_headers={
            "Accept": "gzip, deflate, br"
        })

@ultroid_cmd(pattern="r34 (.*)")
async def r34(event):
    tags = event.pattern_match.group(1).split()
    if len(tags) > 6:
        await event.reply("Please enter up to 6 tags.")
        return
    
    await event.edit("🔞 Searching for posts with tags: {}".format(", ".join(tags)))
    
    r34 = Rule34(tags)
    
    posts = r34.export()
    
    count = 0
    while True:
        if count >= 10: 
            break
        try:
            post_url = next(posts)
            await event.reply(file=post_url)
            count += 1
            await event.edit(f"🔞 Searching for posts with tags: {', '.join(tags)} \n Posts sent: {count}")
        except StopIteration:
            break
    
    await event.edit(f"🔞 Done. Sent {count} posts with tags: {', '.join(tags)}")
    
