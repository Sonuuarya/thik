"""
**Split a Text File into Smaller Files Based on a Given Value.**

**• Examples: **
`{i}break 2` 
`{i}break 4`
"""

from telethon import events
from telethon.tl.types import DocumentAttributeFilename
import os
from . import *

@ultroid_cmd(pattern="break (\\d+)")
async def break_file(event):
    value = event.pattern_match.group(1)
    try:
        value = int(value)
        if value < 2:
            raise ValueError
    except ValueError:
        await event.reply("Please enter a valid integer greater than 1.")
        return    
    reply = await event.get_reply_message()
    if not reply or not reply.media or not isinstance(reply.media.document.attributes[0], DocumentAttributeFilename) or not reply.media.document.attributes[0].file_name.endswith(".txt"):
        await event.reply("Please reply to a text file.")
        return
    file_name = reply.media.document.attributes[0].file_name
    await ultroid_bot.download_media(reply, file_name)
    with open(file_name, "r") as f:
        lines = f.readlines()
        n = len(lines) // value
        for i in range(value):
            new_file_name = file_name[:-4] + f"_{i+1}.txt"
            with open(new_file_name, "w") as g:
                g.writelines(lines[i*n:(i+1)*n])
            await event.reply(file=new_file_name)
            os.remove(new_file_name)
    os.remove(file_name)
