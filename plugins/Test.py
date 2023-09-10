"""
✘ Commands Available -

• `{i}r34py <tags>`
    Download and send up to 100 images from rule34.xxx
    using rule34Py API wrapper.

"""

import os
import requests
from . import *
from rule34Py import rule34Py
from PIL import Image

@ultroid_cmd(pattern="r34py ?(.*)")
async def r34py(event):
    ult = await eor(event, "`Processing...`")
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await ult.edit("`Please enter some tags.`")
    tags = input_str.split()
    r34 = rule34Py()
    result = r34.search(tags, limit=100)
    if not result:
        return await ult.edit("`No images found with those tags.`")
    await ult.edit(f"`Found {len(result)} images. Downloading and sending...`")
    count = 1
    for post in result:
        img_url = post.image
        file_name = os.path.basename(img_url)
        file_path = "resources/downloads/" + file_name
        await download_file(img_url, file_path)
        image = Image.open(file_path)
        width, height = image.size
        max_size = 10 * 1024 * 1024 
        file_size = os.path.getsize(file_path)
        while file_size > max_size:
            width = int(width * 0.9)
            height = int(height * 0.9)
            image = image.resize((width, height), Image.LANCZOS)
            image.save(file_path)
            file_size = os.path.getsize(file_path)
        await event.client.send_file(event.chat_id, file_path, caption=f"Image {count} of {len(result)}")
        os.remove(file_path)
        count += 1
    await ult.delete()
