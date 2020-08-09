""" Create Buttons Through Bots """

# By @Krishna_Singhal

from pyrogram.errors.exceptions.bad_request_400 import UserIsBot, BadRequest

from userge import userge, Config, Message
from userge.utils import parse_buttons as pb


@userge.on_cmd("cbutton", about={
    'header': "Create buttons Using bot",
    'description': "First Create a Bot via @Botfather and "
                   "Add bot token To Config Vars",
    'usage': "{tr}cbutton [reply to button msg]",
    'buttons': "<code>[name][buttonurl:link]</code> - <b>add a url button</b>\n"
               "<code>[name][buttonurl:link:same]</code> - "
               "<b>add a url button to same row</b>"})
async def create_button(msg: Message):
    """ Create Buttons Using Bot """
    if Config.BOT_TOKEN is None:
        await msg.err("First Create a Bot via @Botfather to Create Buttons...")
        return
    string = msg.input_or_reply_raw
    if not string:
        await msg.err("`need an input!`")
        return
    text, markup = pb(string)
    if not text:
        await msg.err("`need text too!`")
        return
    replied = msg.reply_to_message
    message_id = replied.message_id if replied else msg.message_id
    client = msg.client if msg.client.is_bot else msg.client.bot
    try:
        await client.send_message(chat_id=msg.chat.id,
                                  text=text,
                                  reply_to_message_id=message_id,
                                  reply_markup=markup)
    except UserIsBot:
        await msg.err("oops, your Bot is not here to send Msg!")
    except BadRequest:
        await msg.err("Check Syntax of Your Message for making buttons!")
    except Exception as error:
        await msg.edit(f"`Something went Wrong! 😁`\n\n**ERROR:** `{error}`")
    else:
        await msg.delete()
