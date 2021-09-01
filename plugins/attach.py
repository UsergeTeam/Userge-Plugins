# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from userge import userge, Message


@userge.on_cmd("attach", about={
    'header': "Attach any link in a message",
    'usage': "{tr}attach [reply to a message]"})
async def attach(update: Message):
    '''Attach links in message''' 
    if update.reply_to_message is None:
        await update.reply_to_message.reply_text(
            text="Reply to a text for attaching"
        )
        return
    message = update.reply_to_message
    link = message.text.split(" ", 1)[1]
    text = message.reply_to_message.text
    await message.reply_text(text=f"[\u2063]({link}){text}")
