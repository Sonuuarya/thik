# Mirror Bot Hosted By @ItzAditya_xD
# Plugin Made By @ItzAditya_xD
# Ported Into Ultroid By @ItzAditya_xD
"""
**Lᴇᴇᴄʜ Aɴʏ Fɪʟᴇs Fʀᴏᴍ Lɪɴᴋs.**
**Mᴜsᴛ Usᴇ Tᴏʀʀᴇɴᴛ Oʀ Cᴅɴ Lɪɴᴋs Oʀ Eʟsᴇ Wᴏɴᴛ Wᴏʀᴋ**
**Nᴇᴇᴅ Aᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ Fʀᴏᴍ @ItzAditya_xD Oʀ Eʟsᴇ Wᴏɴᴛ Wᴏʀᴋ.**
**Tʜɪs Pʟᴜɢɪɴ Cᴀɴ Aʟsᴏ Lᴇᴇᴄʜ Fɪʟᴇs Fʀᴏᴍ A Tᴇxᴛ Fɪʟᴇ**

** •Usᴀɢᴇ **
{i}leech <link>
{i}leech (Reply To Text File)

** •Exᴀᴍᴘʟᴇ **
{i}leech `https://thothub.to/get_file/18/9f2491a6f6e4bd8bf2fb85c91a674cc7/361000/361790/361790.mp4`
"""

from telethon import events
from asyncio import TimeoutError
from . import *

@ultroid_cmd(pattern="leech ?(.*)")
async def leech(ult):
    url = ult.pattern_match.group(1)
    if not url:
        if not ult.is_reply:
            await ult.edit("Please reply to a text file containing URLs or specify a URL after the .leech command.")
            return
        reply = await ult.get_reply_message()
        if not reply.document:
            await ult.edit("Please reply to a text file containing URLs or specify a URL after the .leech command.")
            return
        file = await ult.client.download_media(reply)
        with open(file, "r") as f:
            urls = f.read().splitlines()
    else:
        urls = [url]
    bot = "@RevyMirror_Bot"
    await ult.edit("Downloading...")
    for url in urls:
        sent_message = await ult.client.send_message(bot, f"/l {url}")
        try:
            while True:
                async with ult.client.conversation(bot, timeout=86400) as conv:
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=bot))
                    response = await response
                    if response.media and (response.photo or response.video):
                        await ult.client.forward_messages(ult.chat_id, response.message)
                        break
                    else:
                        print(response.message.text)
        except TimeoutError:
            await ult.edit(f"Timeout while processing URL: {url}")
            return
    await ult.edit("Files Uploaded.")
