import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📤 Upload Now", callback_data="upload_now"),
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/EL_Pita_Shree")
            ]
        ]
    )
    await bot.send_photo(
        chat_id=m.chat.id,
        photo="https://envs.sh/Lz_.jpg",
        caption = f"""
<blockquote><b>HELLO {m.from_user.mention}</b>

<b>PREMIUM BOT SERVICE</b>  
Designed to <b>extract links</b> from your <code>.TXT</code> files  
and <b>upload them directly</b> to Telegram.

───────────────  
<b>HOW TO USE</b>  
1. Send <code>/upload</code>  
2. Follow the steps  
3. Task will complete automatically  
───────────────  

<b>NOTE:</b> Use <code>/stop</code> anytime to cancel the process.
</blockquote>
""",
        reply_markup=buttons
    )


@bot.on_callback_query()
async def callback_query_handler(bot: Client, query):
    if query.data == "upload_now":
        await query.message.delete()
        await upload(bot, query.message)


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("Stopped🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read().split("\n")
        links = [i.split("://", 1) for i in content]
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    await editable.edit(f"𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤 ғᴏᴜɴᴅ ᴀʀᴇ🔗🔗 {len(links)}\n\n𝕊ᴇɴᴅ 𝔽ʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪ𝕤 1")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("Now Please Send Me Your Batch Name")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("𝔼ɴᴛᴇʀ ʀᴇ𝕤ᴏʟᴜᴛɪᴏɴ📸\n144,240,360,480,720,1080 please choose quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    try:
        res_map = {
            "144": "256x144",
            "240": "426x240",
            "360": "640x360",
            "480": "854x480",
            "720": "1280x720",
            "1080": "1920x1080"
        }
        res = res_map.get(raw_text2, "UN")
    except Exception:
        res = "UN"

    await editable.edit("Now Enter A Caption to add caption on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    MR = f"️ ⁪⁬⁮⁮⁮" if raw_text3 == 'Robin' else raw_text3

    await editable.edit("Now send the Thumb url/nEg » https://envs.sh/Lz_.jpg \n Or if don't want thumbnail send = no")
    input6: Message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    elif thumb == "no":
        thumb = None

    count = int(raw_text) if len(links) > 1 else 1

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=")\
                           .replace("www.youtube-nocookie.com/embed", "youtu.be")\
                           .replace("?modestbranding=1", "")\
                           .replace("/view?usp=sharing", "")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={
                        'User-Agent': 'Mozilla/5.0'
                    }) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(
                    f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                    headers={
                        'x-access-token': 'your-token-here'  # Replace with actual token
                    }).json()['url']

            elif '/master.mpd' in url:
                id = url.split("/")[-2]
                url = f"https://d26g5bnklkwsh4.cloudfront.net/{id}/master.m3u8"

            name1 = re.sub(r'[:/+#|@*."https]', '', links[i][0]).strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"

            cmd = f'yt-dlp -o "{name}.mp4" "{url}"' if "jw-prod" in url else f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}.** {name1}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'

                if "drive" in url:
                    ka = await helper.download(url, name)
                    await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                    os.remove(ka)

                elif ".pdf" in url:
                    os.system(f'yt-dlp -o "{name}.pdf" "{url}" -R 25 --fragment-retries 25')
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                    os.remove(f'{name}.pdf')

                else:
                    Show = f"**⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »**\n\n**📝Name »** `{name}\n❄Quality » {raw_text2}`\n\n**🔗URL »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, res_file, thumb, name, prog)

                count += 1
                time.sleep(1)

            except FloodWait as e:
                await m.reply_text(str(e))
                time.sleep(e.x)
                continue

    except Exception as e:
        await m.reply_text(f"**downloading Interupted**\n{str(e)}")
        return

    await m.reply_text("𝔻ᴏɴᴇ 𝔹ᴏ𝕤𝕤😎")


bot.run()