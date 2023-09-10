"""
**Get Download URLS From First 100 Posts Of A Modle From Thothub.to**

**• Example**
{i}p1 <link>
{i}p1 `https://thothub.to/models/laurenbrite/`
"""

from telethon import events
import re
import time
import requests
import os
from . import *

@ultroid_cmd(pattern="p1 (.*)")
async def p1(event):
    link = event.pattern_match.group(1)
    if not link.startswith("https://thothub.to/models/"):
        await event.reply("Please enter a valid link to a Thothub model page.")
        return
    
    await event.edit("🍂 Getting URL")
    
    class ThothubTO:
        def __get_video_page(self, page_url: str):
            page = requests.get(page_url)
            if page.status_code == 404:
                return []
            return re.findall(r"\"(https:\/\/thothub.to\/videos\/\d+\/.*\/)\"", page.text)

        def __model_page(self, model: str):
            url = "https://thothub.to/models/{}/?".format(model)
            params = {
                "mode": "async",
                "function": "get_block",
                "block_id": "list_videos_common_videos_list",
                "sort_by": "post_date",
                "_": str(int(time.time()))
            }
            for k, v in params.items():
                url += k + "=" + v + "&"
            return url[:-1]

        def __get_video_pages(self, model_page: str):
            i = 1
            while True:
                url = model_page + "&form=" + str(i)
                captured_video_links = self.__get_video_page(url)
                if len(captured_video_links) == 0:
                    break
                for l in captured_video_links:
                    yield l
                i += 1

        def get_video_from_page(self, page_url: str):
            match = re.search(r"https:\/\/thothub.to\/get_file\/\d+\/[a-f0-9]+\/\d+\/\d+\/\d+.mp4", requests.get(page_url).text)
            return None if match is None else match[0]

        def export(self, model: str):
            video_pages = self.__get_video_pages(self.__model_page(model))
            for page_url in video_pages:
                video_url = self.get_video_from_page(page_url)
                if video_url is not None:
                    yield video_url
    
    thothub = ThothubTO()
    
    model = link.split("/")[-2]
    
    video_urls = thothub.export(model)
    
    file_name = f"{model}.txt"
    
    with open(file_name, "w") as f:
        count = 0
        while True:
            if count >= 10: 
                break
            try:
                video_url = next(video_urls)
                f.write(video_url + "\n")
                count += 1
                await event.edit(f"🍂 Getting URL \n URL's Scrapped : {count}")
            except StopIteration:
                break
    await event.respond(file=file_name)
