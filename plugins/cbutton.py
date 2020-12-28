""" Create Buttons Through Bots """

# By @Krishna_Singhal

from pyrogram.errors import UserIsBot, BadRequest

from userge import userge, Config, Message
from userge.utils import parse_buttons as pb, get_file_id_of_media


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
    string = msg.input_raw
    replied = msg.reply_to_message
    file_id = None
    if replied:
        if replied.caption:
            string = replied.caption.html
        elif replied.text:
            string = replied.text.html
        file_id = get_file_id_of_media(replied)
    if not string:
        await msg.err("`need an input!`")
        return
    text, markup = pb(string)
    if not text:
        await msg.err("`need text too!`")
        return
    message_id = replied.message_id if replied else None
    client = msg.client if msg.client.is_bot else msg.client.bot
    try:
        if replied and replied.media and file_id:
            await client.send_cached_media(
                chat_id=msg.chat.id,
                file_id=file_id,
                caption=text,
                reply_to_message_id=message_id,
                reply_markup=markup)
        else:
            await client.send_message(
                chat_id=msg.chat.id,
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
