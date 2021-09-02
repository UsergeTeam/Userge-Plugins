# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from userge import userge, Message


@userge.on_cmd("attach", about={
    'header': "Attach any link's preview in a message",
    'usage': "{tr}attach [link] [reply to a message]"})
async def attach(update: Message):
    '''Attach links in message'''
    link = update.text.split()[1]
    replied = update.reply_to_message
    if replied is None or not link:
        await update.reply_text(
            text="`Reply to a text for attachment and provide link as input...`"
        )
        return
    text = replied.text
    await replied.reply_text(text=f"[\u2063]({link}){text}")
