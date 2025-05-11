import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

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
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
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
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        msg = await event.get_reply_message()
        if msg is None:
            return await event.respond(
                "ɪ ᴄᴀɴ'ᴛ ᴍᴇɴᴛɪᴏɴ ᴍᴇᴍʙᴇʀs ꜰᴏʀ ᴏʟᴅᴇʀ ᴍᴇssᴀɢᴇs! (ᴍᴇssᴀɢᴇs ᴡʜɪᴄʜ ᴀʀᴇ sᴇɴᴛ ʙᴇꜰᴏʀᴇ ɪ'ᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ)"
            )
    else:
        return await event.respond(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴏᴛʜᴇʀs"
        )

    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(chat_id):
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
        
        # Kirim pesan setiap 5 pengguna
        if usrnum % 5 == 0:
            if event.is_reply:
                await msg.reply(usrtxt)
            else:
                await client.send_message(chat_id, usrtxt)
            await asyncio.sleep(2)  # Delay untuk menghindari spam
            usrtxt = ""  # Reset teks setelah mengirim

    # Kirim sisa pengguna yang belum dikirim
    if usrtxt:
        if event.is_reply:
            await msg.reply(usrtxt)
        else:
            await client.send_message(chat_id, usrtxt)


        
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
