""" Fun Stickers for Tweet """

# By @Krishna_Singhal

import os
import re
import requests


from PIL import Image
from validators.url import url

from userge import userge, Config, Message

Converted_img = Config.DOWN_PATH + "img.png"
Converted_stikr = Config.DOWN_PATH + "sticker.webp"


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


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)


@userge.on_cmd("trump", about={
    'header': "Custom Sticker of Trump Tweet",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}trump [text | reply to text]"})
async def trump_tweet(msg: Message):
    """ Fun sticker of Trump Tweet """
    replied = msg.reply_to_message
    args = msg.filtered_input_str
    if args:
        text = args
    elif replied:
        text = args if args else replied.text
    else:
        await msg.err(
            "```Trump Need some Text for Tweet 🙄```", del_in=3)
        return
    await msg.edit("```Requesting trump to tweet... 😃```")
    text = deEmojify(text)
    await trumptweet(text)
    await msg.delete()
    msg_id = replied.message_id if replied else None
    if '-s' in msg.flags:
        await msg.client.send_sticker(
            msg.chat.id,
            Converted_stikr,
            reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(
            msg.chat.id,
            Converted_img,
            reply_to_message_id=msg_id)
    for files in (Converted_img, Converted_stikr):
        if files and os.path.exists(files):
            os.remove(files)


@userge.on_cmd("modi", about={
    'header': "Custom Sticker of Modi Tweet",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}trump [text | reply to text]"})
async def modi_tweet(msg: Message):
    """ Fun Sticker of Modi Tweet """
    replied = msg.reply_to_message
    args = msg.filtered_input_str
    if args:
        text = args
    elif replied:
        text = args if args else replied.text
    else:
        await msg.err(
            "```Modi Need some Text for Tweet 😗```", del_in=3)
        return
    await msg.edit("```Requesting Modi to tweet... 😉```")
    text = deEmojify(text)
    await moditweet(text)
    await msg.delete()
    msg_id = replied.message_id if replied else None
    if '-s' in msg.flags:
        await msg.client.send_sticker(
            msg.chat.id,
            Converted_stikr,
            reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(
            msg.chat.id,
            Converted_img,
            reply_to_message_id=msg_id)
    for files in (Converted_img, Converted_stikr):
        if files and os.path.exists(files):
            os.remove(files)


@userge.on_cmd("cmm", about={
    'header': "Custom Sticker of Change My Mind",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}cmm [text | reply to text]"})
async def Change_My_Mind(msg: Message):
    """ Custom Sticker or Banner of Change My Mind """
    replied = msg.filtered_reply_to_message
    args = msg.input_str
    if args:
        text = args
    elif replied:
        text = args if args else replied.text
    else:
        await msg.err(
            "```Need some Text to Change My Mind 🙂```", del_in=3)
        return
    await msg.edit("```Writing Banner of Change My Mind 😁```")
    text = deEmojify(text)
    await changemymind(text)
    await msg.delete()
    msg_id = replied.message_id if replied else None
    if '-s' in msg.flags:
        await msg.client.send_sticker(
            msg.chat.id,
            Converted_stikr,
            reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(
            msg.chat.id,
            Converted_img,
            reply_to_message_id=msg_id)
    for files in (Converted_img, Converted_stikr):
        if files and os.path.exists(files):
            os.remove(files)


@userge.on_cmd("kanna", about={
    'header': "Custom text Sticker of kanna",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}kanna [text | reply to text]"})
async def kanna(msg: Message):
    """ Fun sticker of Kanna """
    replied = msg.reply_to_message
    args = msg.filtered_input_str
    if args:
        text = args
    elif replied:
        text = args if args else replied.text
    else:
        await msg.err(
            "```Kanna Need some text to Write 😚```", del_in=3)
        return
    await msg.edit("```Kanna is writing for You 😀```")
    text = deEmojify(text)
    await kannagen(text)
    await msg.delete()
    msg_id = replied.message_id if replied else None
    if '-s' in msg.flags:
        await msg.client.send_sticker(
            msg.chat.id,
            Converted_stikr,
            reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(
            msg.chat.id,
            Converted_img,
            reply_to_message_id=msg_id)
    for files in (Converted_img, Converted_stikr):
        if files and os.path.exists(files):
            os.remove(files)


@userge.on_cmd("carry", about={
    'header': "Custom text Sticker of Carryminati",
    'flags': {
        '-s': "To get tweet in Sticker"},
    'usage': "{tr}carry [text | reply to text]"})
async def carry_minati(msg: Message):
    """ Fun Sticker of Carryminati Tweet """
    replied = msg.reply_to_message
    args = msg.filtered_input_str
    if args:
        text = args
    elif replied:
        text = args if args else replied.text
    else:
        await msg.err(
            "```Carry Need some text to Write 😚```", del_in=3)
        return
    await msg.edit("```Carry Minati is writing for You 😀```")
    text = deEmojify(text)
    await carryminati(text)
    await msg.delete()
    msg_id = replied.message_id if replied else None
    if '-s' in msg.flags:
        await msg.client.send_sticker(
            msg.chat.id,
            Converted_stikr,
            reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(
            msg.chat.id,
            Converted_img,
            reply_to_message_id=msg_id)
    for files in (Converted_img, Converted_stikr):
        if files and os.path.exists(files):
            os.remove(files)


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
    args = msg.filtered_input_str
    if args:
        text = args
    elif replied:
        text = args if args else replied.text
    else:
        await msg.err("```Give Me some text to Tweet 😕```", del_in=3)
        return
    await msg.edit("```Creating a Tweet Sticker 😏```")
    if replied:
        u_id = replied.from_user.id
    else:
        u_id = msg.from_user.id
    u_name = (await msg.client.get_users(u_id)).username
    if u_name:
        User_name = u_name
    else:
        User_name = (await msg.client.get_users(u_id)).first_name
    msg_id = replied.message_id if replied else None
    if ',' in msg.filtered_input_str:
        text1, text2 = msg.filtered_input_str.split(',')
        if not text2:
            await msg.err(
                "```Give me Your Custom Username for Tweet... 🙄```"
            )
            return
        Text1 = deEmojify(text1.strip())
        Text2 = deEmojify(text2.strip())
        await tweets(Text1, Text2)
    else:
        Text_1 = deEmojify(text)
        Text_2 = deEmojify(User_name)
        await tweets(Text_1, Text_2)
    await msg.delete()
    if '-s' in msg.flags:
        await msg.client.send_sticker(
            msg.chat.id,
            Converted_stikr,
            reply_to_message_id=msg_id)
    else:
        await msg.client.send_photo(
            msg.chat.id,
            Converted_img,
            reply_to_message_id=msg_id)
    for files in (Converted_img, Converted_stikr):
        if files and os.path.exists(files):
            os.remove(files)


async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
    twEEts = r.get("message")
    tweeturl = url(twEEts)
    if not tweeturl:
        return "```Invalid Syntax, Exiting...```"
    file = Config.DOWN_PATH + "temp.png"
    with open(file, "wb") as twEEt:
        twEEt.write(requests.get(twEEts).content)
    img = Image.open(file)
    img.save(Converted_img)
    img.save(Converted_stikr)
    os.remove(file)
    return Converted_img, Converted_stikr


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
    tweEts = r.get("message")
    tweeturl = url(tweEts)
    if not tweeturl:
        return "```Invalid Syntax, Exiting...```"
    file = Config.DOWN_PATH + "temp.png"
    with open(file, "wb") as twEet:
        twEet.write(requests.get(tweEts).content)
    img = Image.open(file)
    img.save(Converted_img)
    img.save(Converted_stikr)
    os.remove(file)
    return Converted_img, Converted_stikr


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}").json()
    tweetS = r.get("message")
    tweeturl = url(tweetS)
    if not tweeturl:
        return "```Invalid Syntax, Exiting...```"
    file = Config.DOWN_PATH + "temp.png"
    with open(file, "wb") as tweET:
        tweET.write(requests.get(tweetS).content)
    img = Image.open(file)
    img.save(Converted_img)
    img.save(Converted_stikr)
    os.remove(file)
    return Converted_img, Converted_stikr


async def moditweet(text):
    user = "narendramodi"
    k = f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username={user}"
    r = requests.get(k).json()
    tweeTs = r.get("message")
    tweeturl = url(tweeTs)
    if not tweeturl:
        return "```Invalid Syntax, Exiting...```"
    file = Config.DOWN_PATH + "temp.png"
    with open(file, "wb") as tweeT:
        tweeT.write(requests.get(tweeTs).content)
    img = Image.open(file)
    img.save(Converted_img)
    img.save(Converted_stikr)
    os.remove(file)
    return Converted_img, Converted_stikr


async def carryminati(text):
    user = "carryminati"
    k = f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username={user}"
    r = requests.get(k).json()
    Tweets = r.get("message")
    tweeturl = url(Tweets)
    if not tweeturl:
        return "```Invalid Syntax, Exiting...```"
    file = Config.DOWN_PATH + "temp.png"
    with open(file, "wb") as Tweet:
        Tweet.write(requests.get(Tweets).content)
    img = Image.open(file)
    img.save(Converted_img)
    img.save(Converted_stikr)
    os.remove(file)
    return Converted_img, Converted_stikr


async def tweets(text1, text2):
    k = f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    r = requests.get(k).json()
    TWEETS = r.get("message")
    tweeturl = url(TWEETS)
    if not tweeturl:
        return "```Invalid Syntax, Exiting...```"
    file = Config.DOWN_PATH + "temp.png"
    with open(file, "wb") as TWEET:
        TWEET.write(requests.get(TWEETS).content)
    img = Image.open(file)
    img.save(Converted_img)
    img.save(Converted_stikr)
    os.remove(file)
    return Converted_img, Converted_stikr
