# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from requests.utils import requote_uri
from userge import userge, Message


@userge.on_cmd("requote", about={
    'header': "Requote Text",
    'description': "get requoted text from a normal text",
    'usage': "{tr}requote [text]"})
async def requote(update: Message):
    if len(update.text.split()) <= 1:
        text = "Add requote text too."
    else:
        text = requote_uri(update.text.split(" ", 1)[1])
    await update.edit_text(
        text=text,
        disable_web_page_preview=True
    )
