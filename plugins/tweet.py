""" Fun Stickers for Tweet """

# By @Krishna_Singhal

import os
import re
import requests

from PIL import Image
from validators.url import url

from userge import userge, Config, Message

CONVERTED_IMG = Config.DOWN_PATH + "img.png"
CONVERTED_STIKR = Config.DOWN_PATH + "sticker.webp"

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")


@userge.on_cmd("trump", about={
    'header': "Custom Sticker of Trump Tweet",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}trump [text | reply to text]"})
async def trump_tweet(msg: Message):
    """ Fun sticker of Trump Tweet """
    replied = msg.reply_to_message
    if replied and not msg.filtered_input_str:
        text = replied.text
    else:
        text = msg.filtered_input_str
    if not text:
        await msg.err("```Trump Need some Text for Tweet 🙄```", del_in=3)
        return
    await msg.edit("```Requesting trump to tweet... 😃```")
    text_ = _deEmojify(text)
    await _tweets(text_, "trumptweet")
    await _finalize(msg)


@userge.on_cmd("modi", about={
    'header': "Custom Sticker of Modi Tweet",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}trump [text | reply to text]"})
async def modi_tweet(msg: Message):
    """ Fun Sticker of Modi Tweet """
    replied = msg.reply_to_message
    if replied and not msg.filtered_input_str:
        text = replied.text
    else:
        text = msg.filtered_input_str
    if not text:
        await msg.err("```Modi Need some Text for Tweet 😗```", del_in=3)
        return
    await msg.edit("```Requesting Modi to tweet... 😉```")
    text_ = _deEmojify(text)
    await _tweets(text_, "narendramodi")
    await _finalize(msg)


@userge.on_cmd("cmm", about={
    'header': "Custom Sticker of Change My Mind",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}cmm [text | reply to text]"})
async def Change_My_Mind(msg: Message):
    """ Custom Sticker or Banner of Change My Mind """
    replied = msg.reply_to_message
    if replied and not msg.filtered_input_str:
        text = replied.text
    else:
        text = msg.filtered_input_str
    if not text:
        await msg.err("```Need some Text to Change My Mind 🙂```", del_in=3)
        return
    await msg.edit("```Writing Banner of Change My Mind 😁```")
    text_ = _deEmojify(text)
    await _tweets(text_, "changemymind")
    await _finalize(msg)


@userge.on_cmd("kanna", about={
    'header': "Custom text Sticker of kanna",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}kanna [text | reply to text]"})
async def kanna(msg: Message):
    """ Fun sticker of Kanna """
    replied = msg.reply_to_message
    if replied and not msg.filtered_input_str:
        text = replied.text
    else:
        text = msg.filtered_input_str
    if not text:
        await msg.err("```Kanna Need some text to Write 😚```", del_in=3)
        return
    await msg.edit("```Kanna is writing for You 😀```")
    text_ = _deEmojify(text)
    await _tweets(text_, "kannagen")
    await _finalize(msg)


@userge.on_cmd("carry", about={
    'header': "Custom text Sticker of Carryminati",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}carry [text | reply to text]"})
async def carry_minati(msg: Message):
    """ Fun Sticker of Carryminati Tweet """
    replied = msg.reply_to_message
    if replied and not msg.filtered_input_str:
        text = replied.text
    else:
        text = msg.filtered_input_str
    if not text:
        await msg.err("```Carry Need some text to Write 😚```", del_in=3)
        return
    await msg.edit("```Carry Minati is writing for You 😀```")
    text_ = _deEmojify(text)
    await _tweets(text_, "carryminati")
    await _finalize(msg)


@userge.on_cmd("tweet", about={
    'header': "Tweet With Custom text Sticker",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}tweet Text - Username\n"
             "{tr}tweet Text\n"
             "{tr}tweet [Text | with reply to User]"})
async def tweet(msg: Message):
    """ Tweet with your own Username """
    replied = msg.reply_to_message
    if replied and not msg.filtered_input_str:
        text = replied.text
    else:
        text = msg.filtered_input_str
    if not text:
        await msg.err("```Give Me some text to Tweet 😕```", del_in=3)
        return
    username = ''
    if ',' in text:
        text, username = text.split(',')
    if username:
        if replied:
            username = replied.from_user.username or replied.from_user.first_name
        else:
            username = msg.from_user.username or msg.from_user.first_name
    else:
        await message.err("```Give me your Custom Username for Tweet...```")
    await msg.edit("```Creating a Tweet Sticker 😏```")
    text_ = _deEmojify(text.strip())
    type_ = _deEmojify(username.strip())
    await _tweets(text_, type_)
    await _finalize(msg)


def _deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)


async def _tweets(text, type_)
    k = f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username={type_}"
    res = requests.get(k).json()
    tweets_ = res.get("message")
    if not url(tweets_):
        return "```Invalid Syntax, Exiting...```"
    tmp_file = Config.DOWN_PATH + "temp.png"
    with open(tmp_file, "wb") as t_f:
        t_f.write(requests.get(tweets_).content)
    img = Image.open(tmp_file)
    img.save(CONVERTED_IMG)
    img.save(CONVERTED_STIKR)
    os.remove(tmp_file)
    return CONVERTED_IMG, CONVERTED_STIKR


async def _finalize(msg: Message) -> None:
    await msg.delete()
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else None
    if '-s' in msg.flags:
        await msg.client.send_sticker(chat_id=msg.chat.id,
                                      sticker=CONVERTED_STIKR,
                                      reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(chat_id=msg.chat.id,
                                    photo=CONVERTED_IMG,
                                    reply_to_message_id=msg_id)
    for files in (CONVERTED_IMG, CONVERTED_STIKR):
        if files and os.path.exists(files):
            os.remove(files)
