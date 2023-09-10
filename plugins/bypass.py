# Made By @ItzAditya_xD
# Bot Credits To The Owner 
"""
Link Bypasser Plugin

Supported Links : https://spaceb.in/GPWMTZFJ

{i}bypass <link>


"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from . import *

@ultroid_cmd(pattern="bypass (.*)")
async def bypass(ult):
    chat = "@BypassLinkBot"
    link = ult.pattern_match.group(1)
    await ult.edit("⚡ Bypassing the link...")
    async with ult.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(incoming=True, from_users=5746507003))
            await ult.client.send_message(chat, link)
            response = await response
        except YouBlockedUserError:
            await ult.reply("Boss! Please Unblock @BypassLinkBot ")
            return
        generating_message = response.message.text
        response = conv.wait_event(events.NewMessage(incoming=True, from_users=5746507003))
        response = await response
        direct_link = response.message.text
        await ult.edit(f"»Hᴇʀᴇ Is Yᴏᴜʀ Bʏᴘᴀssᴇᴅ Lɪɴᴋ `{direct_link}`")        
