""" Fun Stickers for Tweet """

# By @Krishna_Singhal

import os
import requests

from PIL import Image
from validators.url import url

from userge.utils import demojify
from userge import userge, Config, Message

CONVERTED_IMG = Config.DOWN_PATH + "img.png"
CONVERTED_STIKR = Config.DOWN_PATH + "sticker.webp"

CELEBRITIES = {
    "ab": "SrBachchan",
    "ambani": "Asliambani",
    "ananya": "ananyapandayy",
    "android": "Android",
    "apple": "apple",
    "arnab": "ArnabGoswamiRTV",
    "ashish": "ashchanchlani",
    "bb": "Bhuvan_Bam",
    "bjp": "bjp4india",
    "chris": "chrishhemsworth",
    "elvish": "ElvishYadav",
    "fb": "facebook",
    "hashmi": "Emraanhashmi",
    "harsh": "iamharshbeniwal",
    "ht": "htTweets",
    "jio": "reliancejio",
    "karan": "karanjohar",
    "kiara": "advani_kiara",
    "netflix": "netflix",
    "osama": "ItstherealOsama",
    "ph": "pornhub",
    "rahul": "RahulGandhi",
    "rajni": "rajinikanth",
    "ramdev": "yogrishiramdev",
    "rdj": "RobertDowneyJr",
    "salman": "BeingSalmanKhan",
    "setu": "Arogyasetu",
    "sonakshi": "Aslisonagold",
    "sonam": "sonamakapoor",
    "srk": "iamsrk",
    "telegram": "telegram",
    "whatsapp": "WhatsApp",
    "yogi": "myogiadityanath",
    "yt": "youtube",
    "zee": "ZeeNews"}


@userge.on_cmd("trump", about={
    'header': "Custom Sticker of Trump Tweet",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}trump [text | reply to text]"})
async def trump_tweet(msg: Message):
    """ Fun sticker of Trump Tweet """
    replied = msg.reply_to_message
    text = msg.filtered_input_str
    if replied and not text:
        text = replied.text
    if not text:
        await msg.err("Trump Need some Text for Tweet 🙄")
        return
    await msg.edit("```Requesting trump to tweet... 😃```")
    await _tweets(msg, text, type_="trumptweet")


@userge.on_cmd("modi", about={
    'header': "Custom Sticker of Modi Tweet",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}modi [text | reply to text]"})
async def modi_tweet(msg: Message):
    """ Fun Sticker of Modi Tweet """
    replied = msg.reply_to_message
    text = msg.filtered_input_str
    if replied and not text:
        text = replied.text
    if not text:
        await msg.err("Modi Need some Text for Tweet 😗")
        return
    await msg.edit("```Requesting Modi to tweet... 😉```")
    await _tweets(msg, text, "narendramodi")


@userge.on_cmd("cmm", about={
    'header': "Custom Sticker of Change My Mind",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}cmm [text | reply to text]"})
async def Change_My_Mind(msg: Message):
    """ Custom Sticker or Banner of Change My Mind """
    replied = msg.reply_to_message
    text = msg.filtered_input_str
    if replied and not text:
        text = replied.text
    if not text:
        await msg.err("Need some Text to Change My Mind 🙂")
        return
    await msg.edit("```Writing Banner of Change My Mind 😁```")
    await _tweets(msg, text, type_="changemymind")


@userge.on_cmd("kanna", about={
    'header': "Custom text Sticker of kanna",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}kanna [text | reply to text]"})
async def kanna(msg: Message):
    """ Fun sticker of Kanna """
    replied = msg.reply_to_message
    text = msg.filtered_input_str
    if replied and not text:
        text = replied.text
    if not text:
        await msg.err("Kanna Need some text to Write 😚")
        return
    await msg.edit("```Kanna is writing for You 😀```")
    await _tweets(msg, text, type_="kannagen")


@userge.on_cmd("carry", about={
    'header': "Custom text Sticker of Carryminati",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}carry [text | reply to text]"})
async def carry_minati(msg: Message):
    """ Fun Sticker of Carryminati Tweet """
    replied = msg.reply_to_message
    text = msg.filtered_input_str
    if replied and not text:
        text = replied.text
    if not text:
        await msg.err("Carry Need some text to Write 😚")
        return
    await msg.edit("```Carry Minati is writing for You 😀```")
    await _tweets(msg, text, "carryminati")


@userge.on_cmd("tweet", about={
    'header': "Tweet With Custom text Sticker",
    'available celebrities': "<code>Check this</code> "
             "<a href='https://telegra.ph/dogbin---crollokoph-08-09'>link</a>"
             " <code>to know available Celebrities.</code>",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}tweet text , username\n"
             "{tr}tweet username [reply to text]\n"})
async def tweet(msg: Message):
    """ Create Tweets of given celebrities """
    replied = msg.reply_to_message
    args = msg.filtered_input_str
    if replied and replied.text:
        text = replied.text
        username = args
        if not username:
            username = replied.from_user.username or replied.from_user.first_name
    elif args:
        if ',' in args:
            text, user_name = args.split(',', maxsplit=1)
            text = text.strip()
            username = user_name.strip()
        if not user_name:
            username = msg.from_user.username or msg.from_user.first_name
    else:
        await msg.err("Input not found!")
        return
    if username in CELEBRITIES:
        celebrity = CELEBRITIES[username]
    else:
        celebrity = username
    await msg.edit(f"`{celebrity} is tweeting 😏`")
    await _tweets(msg, text, celebrity)


async def _tweets(msg: Message, text: str, username: str = '', type_: str = "tweet") -> None:
    api_url = f"https://nekobot.xyz/api/imagegen?type={type_}&text={demojify(text)}"
    if username:
        api_url += f"&username={demojify(username)}"
    res = requests.get(api_url).json()
    tweets_ = res.get("message")
    if not url(tweets_):
        await msg.err("Invalid Syntax, Exiting...")
        return
    tmp_file = Config.DOWN_PATH + "temp.png"
    with open(tmp_file, "wb") as t_f:
        t_f.write(requests.get(tweets_).content)
    img = Image.open(tmp_file)
    img.save(CONVERTED_IMG)
    img.save(CONVERTED_STIKR)
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
    os.remove(tmp_file)
    os.remove(CONVERTED_IMG)
    os.remove(CONVERTED_STIKR)
