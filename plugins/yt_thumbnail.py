# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import ytthumb
from userge import userge, Message


@userge.on_cmd("ytthumb", about={
    'header': "YouTube Video Thumbnail",
    'description': "get thumbnail of a youtube video",
    'usage': "{tr}ytthumb [link]"})
async def youtube_thumbnail(update: Message):
    if " " not in update.text:
        await update.edit_text("Send with youtube video link or id")
        return
    await update.edit_text("`Processing`")
    thumbnail = ytthumb.thumbnail(update.text.split(" ", 1)[1])
    message = update.reply_to_message if update.reply_to_message else update
    await message.reply_photo(
        photo=thumbnail,
        quote=True
    )
    await update.delete()
