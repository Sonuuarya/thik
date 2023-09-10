# Made By - ⚡️Λ∂ιтуα
# Ported Into Ultroid By ⚡️Λ∂ιтуα (@itzAditya_xD)
"""
**Merge Text Files Plugin**

> This plugin allows you to merge up to 50 text files into one file.

**• Examples: **
> `{i}m` : Reply to a text file to download it and add it to the merge list.
> `{i}merge <filename>.txt` : Merge all the downloaded text files and upload the result with the given filename.
"""

import os
from . import LOGS, ultroid_cmd
from io import BytesIO
from . import async_searcher


@ultroid_cmd(pattern="m$")
async def download_text(e):
    reply = await e.get_reply_message()
    if not reply or not reply.media or not reply.file.ext == ".txt":
        return await e.eor("`Please reply to a text file.`")
    file = await e.client.download_media(reply)
    if os.path.exists("merge_list.txt"):
        with open("merge_list.txt", "a") as f:
            f.write(file + "\n")
    else:
        with open("merge_list.txt", "w") as f:
            f.write(file + "\n")
    await e.eor(f"`{file}` added to the merge list.")


@ultroid_cmd(pattern="merge (.*)")
async def merge_text(e):
    filename = e.pattern_match.group(1)
    if not filename.endswith(".txt"):
        return await e.eor("`Please provide a valid filename ending with .txt`")
    if not os.path.exists("merge_list.txt"):
        return await e.eor("`No text files downloaded. Please use {i}m command first.`")
    with open("merge_list.txt", "r") as f:
        files = f.read().splitlines()
    if len(files) > 50:
        return await e.eor("`Cannot merge more than 50 text files. Please reduce the number of files in the merge list.`")
    eris = await e.eor("`Merging text files...`")
    line_count = 0
    with open(filename, "w") as f:
        for file in files:
            with open(file, "r") as g:
                content = g.read()
                f.write(content + "\n")
                line_count += len(content.splitlines())
            os.remove(file)
    os.remove("merge_list.txt")
    caption = f"`{filename}` merged from {len(files)} text files.\n"
    caption += f"Number of Lines: {line_count}"
    await e.client.send_file(e.chat_id, filename, caption=caption, reply_to=e.reply_to_msg_id)
    await eris.try_delete()
