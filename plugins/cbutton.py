""" Create Buttons Through Bots """

# By @Krishna_Singhal

from pyrogram import InlineKeyboardMarkup as keyboard
from pyrogram.errors.exceptions.bad_request_400 import (
    UserIsBot, BadRequest, MessageEmpty)

from userge import userge, Config, Message, _parse_buttons as pb


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
    replied = msg.reply_to_message
    if not (replied and replied.text):
        await msg.err("Reply a text Msg")
        return
    text, buttons = pb(replied.text)
    try:
        await userge.bot.send_message(
            msg.chat.id, text=text,
            reply_to_message_id=replied.message_id,
            reply_markup=keyboard(buttons))
    except UserIsBot:
        await msg.err(
            "oops, your Bot is not here to send Msg!")
    except BadRequest:
        await msg.err(
            "Check Syntax of Your Message for making buttons!")
    except MessageEmpty:
        await msg.err(
            "Message Object is Empty!")
    except Exception as error:
        await msg.edit(
            f"`Something went Wrong! 😁`\n\n**ERROR:** `{error}`")
    else:
        await msg.delete()
