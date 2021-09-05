# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from requests.utils import requote_uri
from userge import userge, Message


@userge.on_cmd("requote", about={
    'header': "Requote Text",
    'description': "get requoted text from a normal text",.
    'usage': "{tr}requote [text]"})
async def requote(update: Message):
    text = requote_uri(update.message.text)
    await update.message.edit_text(
        text=text,
        disable_web_page_preview=True,
    )
