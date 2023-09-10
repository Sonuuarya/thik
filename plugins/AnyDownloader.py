#Ported Into Ultroid By @ItzAditya_xD

"""
**Aɴʏ Dᴏᴡɴʟᴏᴀᴅᴇʀ**

Gᴇᴛ Cᴅɴ Lɪɴᴋs Oғ Aɴʏ Yᴛᴅʟ Sᴜᴘᴘᴏʀᴛᴇᴅ 
Sɪᴛᴇ Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Iᴛ Aᴛ HD

»Usᴀɢᴇ
`{i}ok <link>`

"""

import os
import subprocess
import time
from . import ultroid_cmd
import yt_dlp

@ultroid_cmd(pattern=".ok(?: |$)(.*)")
async def download_youtube_video(event):
    input_url = event.pattern_match.group(1).strip()

    if not input_url:
        await event.edit("Please provide a valid YouTube video link.")
        return

    try:
        ydl_opts = {
            'format': 'best[ext=mp4][height<=720]',
            'progress_hooks': [lambda d: progress_hook(d, event)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(input_url, download=True)
            filename = ydl.prepare_filename(info)

        await event.edit(f"Downloaded: {filename}")

    except Exception as e:
        await event.edit(f"An error occurred: {str(e)}")

def progress_hook(d, event):
    if d['status'] == 'downloading':
        progress = d['_percent_str']
        event.edit(f"Downloading: {progress} ▰▰▰▰▰▰▰▰▰▰▰▱")
    if d['status'] == 'finished':
        event.edit(f"Downloaded: {d['filename']} ▰▰▰▰▰▰▰▰▰▰▰▰")
    if d['status'] == 'error':
        event.edit(f"An error occurred while downloading: {d['filename']}")
