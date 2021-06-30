# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from userge import userge, Message


@userge.on_cmd("attach", about={
    'header': "Attach any link in a message",
    'usage': "{tr}attach [reply to a message]"})
async def attach(message: Message):
    '''Attach links in message'''
    link = message.text.split(" ", -1)
    text = message.reply_to_message.text
    await message.reply_text(text=f"[\u2063]({link}){text}")
