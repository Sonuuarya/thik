#Ported Into Ultroid By @ItzAditya_xD
"""

**Fᴀᴘᴇʟʟᴏ Dᴏᴡɴʟᴏᴀᴅᴇʀ**

»Sᴄʀᴀᴘᴇ Iᴍᴀɢᴇ Aɴᴅ Vɪᴅᴇᴏ Fʀᴏᴍ Fapello.com

»𝙐sᴀɢᴇ
> {i}fp https://fapello.com/tanababyxo-12/

"""

import requests, os
from bs4 import BeautifulSoup
from . import ultroid_cmd

@ultroid_cmd(pattern="fp( ([\s\S]*)|$)")
async def fapello(event):
    url = event.pattern_match.group(1)
    profile = url.split("/")[-2]
    r = requests.get(url)
    await event.reply(f"STATUS => {r.status_code}")
    soup = BeautifulSoup(r.text, "lxml")
    for img in soup.find_all("img"):
        if str(profile) in str(img.get("src")):
            media_url = (img.get("src").replace("_300px", ""))
            madia_name = media_url.split("/")[-1]
            if(not os.path.isfile(madia_name)):
                r = requests.get(media_url)
                open(madia_name, 'wb').write(r.content)
                await event.client.send_file(event.chat_id, madia_name)
