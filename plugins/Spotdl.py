"""
**𝙎𝙋𝙊𝙏𝙄𝙁𝙔 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿𝙀𝙍**
**Dᴏᴡɴʟᴏᴀᴅ Aʟʟ Sᴏɴɢs Fᴏʀ Aɴ Aʀᴛɪsᴛ**
**Dᴏᴡɴʟᴏᴀᴅ Aʟʟ Sᴏɴɢs Fʀᴏᴍ A Pʟᴀʏʟɪsᴛ**
**Dᴏᴡɴʟᴏᴀᴅ Sɪɴɢʟᴇ Sᴏɴɢ**

** •Example **
`{i}sp <url>`
`{i}sp https://open.spotify.com/track/6Rdp4sAeb38xf8DByVG3Xs?si=f3UzJaS8Q3K2HMC375v2Rg&utm_source=copy-link`
"""
import os
import glob
from . import ultroid_cmd
from . import *

@ultroid_cmd(pattern="sp (.*)")
async def spotdl(event):
    delete=1
    query = event.pattern_match.group(1)
    if not query:
        return await event.reply("Please provide a valid Spotify URL or search query.")
    try:
        os.system(f"spotdl {query}")
        await event.reply("Download complete!")
        for file in glob.glob("*.mp3"):
            await event.client.send_file(event.chat_id, file)
            if (delete==1):
                os.remove(file)
    except Exception as e:
        await event.reply(f"An error occurred: {e}")
