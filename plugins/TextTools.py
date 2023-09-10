"""

**Ignore N Lines from a Text File and Upload the Rest**
**• Examples: **
> `{i}ignore 5`

**Count the Number of Lines in a Text File**
**• Examples: **
> `{i}count`

**Print N Lines from a Text File**
**• Examples: **
> `{i}lines 10`

**Ignore Blank Lines In A Text File**
**• Example: **
> `{i}blank`

**Split a Text File into Smaller Files Based on a Given Value.**

**• Examples: **
> `{i}break 2` 
> `{i}break 4`

"""

import os
from io import BytesIO
from . import ultroid_cmd
from telethon import events
from telethon.tl import functions, types
from . import *
from telethon.tl.types import DocumentAttributeFilename

@ultroid_cmd(pattern="count")
async def count_lines(e):
    reply = await e.get_reply_message()
    if not reply or not reply.media or "text" not in reply.file.mime_type or not reply.file.name.endswith(".txt"):
        return await e.eor("`Please reply to a text file with .txt extension`")
    file = await e.client.download_media(reply)
    with open(file, "r") as f:
        lines = f.readlines()
    output = f"`The file has {len(lines)} lines`"
    await e.reply(output)
    os.remove(file) 

@ultroid_cmd(pattern="ignore (\d+)")
async def ignore_lines(e):
    amount = int(e.pattern_match.group(1))
    reply = await e.get_reply_message()
    if not reply or not reply.media or "text" not in reply.file.mime_type or not reply.file.name.endswith(".txt"):
        return await e.eor("`Please reply to a text file with .txt extension`")
    file = await e.client.download_media(reply)
    with open(file, "r") as f:
        lines = f.readlines()
    if amount > len(lines):
        return await e.eor("`The file does not have that many lines`")
    output = "".join(lines[amount:])
    with BytesIO(output.encode()) as new_file:
        new_file.name = "output.txt"
        await e.client.send_file(
            e.chat_id, new_file, caption=f"`Ignored {amount} lines from the file`", reply_to=e.reply_to_msg_id
        )
    os.remove(file) 

@ultroid_cmd(pattern="lines (\d+)")
async def print_lines(e):
    amount = int(e.pattern_match.group(1))
    reply = await e.get_reply_message()
    if not reply or not reply.media or "text" not in reply.file.mime_type or not reply.file.name.endswith(".txt"):
        return await e.eor("`Please reply to a text file with .txt extension`")
    file = await e.client.download_media(reply)
    with open(file, "r") as f:
        lines = f.readlines()
    if amount > len(lines):
        return await e.eor("`The file does not have that many lines`")
    output = "".join(lines[:amount])
    await e.reply(f"`{output}`")
    os.remove(file) 

@ultroid_cmd(pattern="blank")
async def blank(e):
    reply = await e.get_reply_message()
    if not reply or not reply.file or reply.file.mime_type != "text/plain":
        return await eor(e, "Please reply to a text file.")
    message = await eor(e, "Downloading...")
    file = await reply.download_media()
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as f:
        for line in lines:
            if line.strip():
                f.write(line)
    await message.edit("Uploading...")
    await e.reply(file=file)
    await message.edit("⚡Done")
    os.remove(file)

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
