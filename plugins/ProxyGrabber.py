"""
**Grab Proxy From Any Proxy Source URL**
**Warning ⚠️**
**Please Use A Small Source List Or Your Whole Bot May Get Fucked Up**

**• Example**
`{i}grab`
Make Sure Reply To A Text File Or Else Wont Work
"""

from telethon import events
from . import *
import requests
import re
from concurrent.futures import ThreadPoolExecutor

proxy_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\b"
num_threads = 1000
urls_per_thread = 100

def scrape_url(url):
    proxies = []
    try:
        res = requests.get(url.strip())
        proxies.extend(re.findall(proxy_regex, res.text))
    except:
        pass
    return proxies

@ultroid_cmd(pattern="grab")
async def grab_proxies(event):
    if not event.is_reply:
        await event.edit("Please reply to a text file containing the URLs.")
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith(".txt"):
        await event.edit("Please reply to a text file containing the URLs.")
        return
    urls = (await reply.download_media(bytes)).decode().split("\n")
    proxies = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(0, len(urls), urls_per_thread*num_threads):
            batch_urls = urls[i:i+urls_per_thread*num_threads]
            results = executor.map(scrape_url, batch_urls)
            for result in results:
                proxies.extend(result)
            await event.edit(f"Scraping from line {i+1}/{len(urls)}. Total proxies found: {len(proxies)}")
    if proxies:
        with open("proxies.txt", "w") as f:
            f.write("\n".join(proxies))
        await event.edit(f"Found {len(proxies)} proxies. Saved to `proxies.txt`.")
    else:
        await event.edit("No proxies found.")
