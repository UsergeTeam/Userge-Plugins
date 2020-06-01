import os
import asyncio

from userge import userge, Message, Config

S_LOG = userge.getCLogger(__name__)


@userge.on_cmd("spem", about={
    'header': "Spam some Messages",
    'description': "Message Spam module just for fun."
                   "Btw Don't over use this plugin or get"
                   "ready for account ban or flood waits. "
                   "For spamming text use '|' to separate count and text.",
    'usage': "{tr}spem [spam count] | [spam message/reply to a media]",
    'examples': "**For Text:** `{tr}spem 2 | Durov will ban me for using this plugin`"})
async def spem(message: Message):
    replied = message.reply_to_message
    is_str = "|" in message.input_str
    if (replied and replied.media and not is_str):
        if not os.path.isdir(Config.DOWN_PATH):
            os.makedirs(Config.DOWN_PATH)
        if replied.sticker:
            to_spem = replied.sticker.file_id
            try:
                sc = int(message.input_str)
            except ValueError as e:
                await message.edit(e)
                await message.reply_sticker(sticker="CAADAQADzAADiO9hRu2b2xyV4IbAFgQ")
                return
            await message.edit(f"Spamming {sc} Time")
            for _ in range(sc):
                await userge.send_sticker(sticker=to_spem, chat_id=message.chat.id)
                await asyncio.sleep(0.1)
            await S_LOG.log(f"Spammed Sticker in Chat» {message.chat.title}, {sc} times")
        elif (replied.animation or replied.video or replied.photo):
            dls = await userge.download_media(
                message=message.reply_to_message,
                file_name=Config.DOWN_PATH
            )
            to_spem = os.path.join(Config.DOWN_PATH, os.path.basename(dls))
            try:
                sc = int(message.input_str)
            except ValueError as e:
                await message.edit(e)
                await message.reply_sticker(sticker="CAADAQADzAADiO9hRu2b2xyV4IbAFgQ")
                return
            await message.edit(f"Spamming {sc} times")
            if (replied.video or replied.animation):
                for _ in range(sc):
                    await userge.send_video(video=to_spem, chat_id=message.chat.id)
                    await asyncio.sleep(0.1)
            elif replied.photo:
                for _ in range(sc):
                    await userge.send_photo(photo=to_spem, chat_id=message.chat.id)
                    await asyncio.sleep(0.1)
            await S_LOG.log(f"Spammed Media in Chat» {message.chat.title}, {sc} times")
    elif is_str:
        spem_count, spem_text = message.input_str.split("|")
        try:
            sc = int(spem_count)
        except ValueError as e:
            await message.edit(e)
            await message.reply_sticker(sticker="CAADAQADzAADiO9hRu2b2xyV4IbAFgQ")
            return
        await message.edit(f"Spamming {sc} times")
        for _ in range(sc):
            await userge.send_message(text=spem_text, chat_id=message.chat.id)
            await asyncio.sleep(0.1)
        await S_LOG.log(f"Spammed Text in Chat» {message.chat.title}, {sc} times")
    else:
        await message.edit("Well it doesn't work that way")
        await message.reply_sticker(sticker="CAADAQAD6gADfAVQRnyVSb3GhGT4FgQ")
