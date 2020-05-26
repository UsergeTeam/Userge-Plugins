import os
import asyncio
from userge import userge, Message, Config

S_LOG = userge.getCLogger(__name__)

@userge.on_cmd("spem", about={
    'header': "Spam some Messages",
    'description': "Message Spam module just for fun."
                   "Btw Don't over use this plugin or get"
                   "ready for account ban or flood waits.",
    'usage': "{tr}spem [spam count] [spam message/reply to a media]",
    'example': "{tr}spem 10 Durov will ban me for using this plugin"})
async def spem(message: Message):
    if message.reply_to_message:
        replied = message.reply_to_message
        if not replied.media:
            await message.edit("Bruh! Hands up!! Durov wants to know ur location")
            await message.reply_sticker(sticker="CAADAQADrwAD3RUoRoRNidg0f7S3FgQ")
            await S_LOG.log("Sent your current location to Durov, Good Luck kek")
            return
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
            for spem in range(sc):
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
                for spem in range(sc):
                    await userge.send_video(video=to_spem, chat_id=message.chat.id)
                    await asyncio.sleep(0.1)
            elif replied.photo:
                for spem in range(sc):
                    await userge.send_photo(photo=to_spem, chat_id=message.chat.id)
                    await asyncio.sleep(0.1)
            await S_LOG.log("Spammed Media in Chat» {message.chat.title}, {sc} times")
    elif len(message.input_str.split()) > 1:
        spem_count, spem_text = message.input_str.split()
        try:
            sc = int(spem_count)
        except ValueError as e:
            await message.edit(e)
            await message.reply_sticker(sticker="CAADAQADzAADiO9hRu2b2xyV4IbAFgQ")
            return
        await message.edit(f"Spamming {sc} times")
        for spem in range(sc):
            await userge.send_message(text=spem_text, chat_id=message.chat.id)
            await asyncio.sleep(0.1)
        await S_LOG.log("Spammed Text in Chat» {message.chat.id}, {sc} times")
    else:
        await message.edit("Well it doesn't work that way")
        await message.reply_sticker(sticker="CAADAQAD6gADfAVQRnyVSb3GhGT4FgQ")
