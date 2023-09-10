"""
{i}getlimk
"""
import os
from . import *

@ultroid_cmd(pattern="getlimk -c \"(.*)\" -s (.*) -e (.*)")
async def getlink(event):
    chat_id = event.pattern_match.group(1)
    if not chat_id.startswith("-100"):
        return await event.eor("Error: Invalid chat ID")
    start_msg_id = int(event.pattern_match.group(2))
    end_msg_id = int(event.pattern_match.group(3))
    thumb = ULTConfig.thumb
    msg = await event.eor("Processing...")
    for msg_id in range(start_msg_id, end_msg_id + 1):
        try:
            message = await event.client.get_messages(chat_id, ids=msg_id)
            if message and message.media:
                file_name = message.file.name
                file_path, _ = await downloader(message, file_name)
                attributes = await set_attributes(file_path)
                await event.client.send_file(
                    event.chat_id,
                    file_path,
                    thumb=thumb,
                    caption=f"Uploaded {file_name}",
                    attributes=attributes,
                    force_document=True,
                )
                os.remove(file_path)  # Remove the downloaded file from disk
                await msg.edit(f"Downloaded and uploaded {file_name}")
        except Exception as e:
            LOGS.exception(e)
            continue
    await msg.edit("Uploaded Everything")
