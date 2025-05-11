import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    UserNotParticipantError
)

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**I'm MentionAll Bot**, I will help you to mention near about all members in your group and channel 👻\nClick **/help** for more information__\n\n Follow [@aseppppv](https://t.me/aseppppv) on my channel",
    link_preview=False,
    buttons=(
      [
        Button.url('Grup Chat', 'https://t.me/death_star_area'),
        Button.url('Ch Film', 'https://t.me/awdfilm')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of MentionAll_Bot**\n\nCommand: /utag\n__You can use this command with text what you want to say to others.__\n`Example: /utag ketik pesan nya atuhh`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nFollow [@aseppppv](https://t.me/aseppppv) on my channel"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('Grup Chat', 'https://t.me/death_star_area'),
        Button.url('Ch Film', 'https://t.me/awdfilm')
      ]
    )
  )
  
 
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond(
            "ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs"
        )

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴍᴇɴᴛɪᴏɴ ᴀʟʟ")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("ɢɪᴠᴇ ᴍᴇ ᴏɴᴇ ᴀʀɢᴜᴍᴇɴᴛ")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg_text = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg_obj = await event.get_reply_message()
        if msg_obj is None:
            return await event.respond(
                "ɪ ᴄᴀɴ'ᴛ ᴍᴇɴᴛɪᴏɴ ᴍᴇᴍʙᴇʀs ꜰᴏʀ ᴏʟᴅᴇʀ ᴍᴇssᴀɢᴇs! (ᴍᴇssᴀɢᴇs ᴡʜɪᴄʜ ᴀʀᴇ sᴇɴᴛ ʙᴇꜰᴏʀᴇ ɪ'ᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ)"
            )
        msg_text = getattr(msg_obj, 'raw_text', '') or getattr(msg_obj, 'message', '') or ''
    else:
        return await event.respond(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴏᴛʜᴇʀs"
        )

    # Step 1: Mention anggota dalam beberapa batch tanpa teks
    usrnum = 0
    usrtxt = ""
    batch_size = 5
    async for usr in client.iter_participants(chat_id):
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
        if usrnum % batch_size == 0:
            await client.send_message(chat_id, usrtxt)
            await asyncio.sleep(2)
            usrtxt = ""

    # Kirim batch mention tersisa jika ada
    if usrtxt:
        await client.send_message(chat_id, usrtxt)

    # Step 2: Kirim teks lengkap (multiline) sebagai pesan terpisah supaya semua paragraf terbaca
    if mode == "text_on_cmd":
        await client.send_message(chat_id, msg_text)
    elif mode == "text_on_reply":
        await msg_obj.reply(msg_text)


@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> BOT STARTED <<")
client.run_until_disconnected()
