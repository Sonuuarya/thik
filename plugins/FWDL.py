"""
{i}fwdl
"""
import os
import re
import time
import asyncio
from datetime import datetime
from . import *
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from . import LOGS, time_formatter, downloader, random_string

REGEXA = r"^(?:(?:https|tg):\/\/)?(?:www\.)?(?:t\.me\/|openmessage\?)(?:(?:c\/(\d+))|(\w+)|(?:user_id\=(\d+)))(?:\/|&message_id\=)(\d+)(?:\?single)?$"
DL_DIR = "/home/user/app/ok"

def rnd_filename(path):
    if not os.path.exists(path):
        return path
    spl = os.path.splitext(path)
    rnd = "_" + random_string(5).lower() + "_"
    return spl[0] + rnd + spl[1]

@ultroid_cmd(
    pattern="fwdl(?: |$)((?:.|\n)*)",
)
async def fwd_dl(e):
    ghomst = await e.eor("`checking...`")
    args = e.pattern_match.group(1)
    if not args:
        reply = await e.get_reply_message()
        if reply and reply.text:
            args = reply.message
        else:
            return await eod(ghomst, "Give two tg links to download", time=10)
    
    links = args.split()
    if len(links) != 2:
        return await ghomst.edit("`Give two tg links to proceed`")
    
    start_link, end_link = links
    
    remgx_start = re.findall(REGEXA, start_link)
    remgx_end = re.findall(REGEXA, end_link)
    
    if not remgx_start or not remgx_end:
        return await ghomst.edit("`probably invalid Links !?`")

    try:
        chat_start, id_start = [i for i in remgx_start[0] if i]
        chat_end, id_end = [i for i in remgx_end[0] if i]
        
        if chat_start != chat_end:
            return await ghomst.edit("`Links should be from the same chat/channel`")
        
        channel = int(chat_start) if chat_start.isdigit() else chat_start
        start_msg_id = int(id_start)
        end_msg_id = int(id_end)
        
        if start_msg_id > end_msg_id:
            start_msg_id, end_msg_id = end_msg_id, start_msg_id
        
    except Exception as ex:
        return await ghomst.edit("`Give valid tg links to proceed`")

    try:
        msgs = await e.client.get_messages(channel, min_id=start_msg_id-1, max_id=end_msg_id+1)
        
        for msg in msgs:
            start_ = datetime.now()
            if (msg and msg.media) and hasattr(msg.media, "photo"):
                dls = await e.client.download_media(msg, DL_DIR)
            elif (msg and msg.media) and hasattr(msg.media, "document"):
                fn = msg.file.name or f"{channel}_{msg.id}{msg.file.ext}"
                filename = rnd_filename(os.path.join(DL_DIR, fn))
                try:
                    dlx = await downloader(
                        filename,
                        msg.document,
                        ghomst,
                        time.time(),
                        f"Downloading {filename}...",
                    )
                    dls = dlx.name
                except MessageNotModifiedError as err:
                    LOGS.exception(err)
                    return await xx.edit(str(err))
            else:
                continue

            end_ = datetime.now()
            ts = time_formatter(((end_ - start_).seconds) * 1000)

            stream, force_doc, delete, thumb = (
                False,
                True,
                False,
                ULTConfig.thumb,
            )

            file, _ = await e.client.fast_uploader(
                    dls, show_progress=True, event=ghomst, to_delete=delete
                )

            await e.client.send_file(
                    e.chat_id,
                    file,
                    supports_streaming=stream,
                    force_document=force_doc,
                    thumb=thumb,
                    caption=f"`{os.path.basename(dls)}`",
                    reply_to=e.reply_to_msg_id or e,
                )

            os.remove(dls)
            
    except Exception as ex:
        return await ghomst.edit(f"**Error:**  `{ex}`")
