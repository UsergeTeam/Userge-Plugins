"""P*rnhub Comment"""

# BY code-rgb [https://github.com/code-rgb]

import os
import requests
from validators.url import url
from html_telegraph_poster.upload_images import upload_image
from userge import userge, Message, Config


@userge.on_cmd("ph", about={
    'header': "P*rnhub Comment",
    'description': "Creates a P*rnhub Comment of Replied User With Custom Name",
    'usage': "{tr}ph Name | [reply or reply with text]",
    'examples': [
        "{tr}ph Did they ever get the pizza?",
        "{tr}ph David | Did they ever get the pizza?",
        "{tr}ph David | "]}, check_downpath=True)
async def ph_comment(message: Message):
    """ Create P*rnhub Comment for Replied User """
    replied = message.reply_to_message
    if replied:
        if "|" in message.input_str:
            u_name, msg_text = message.input_str.split('|')
            name = u_name.strip()
            comment = msg_text or replied.text
        else:
            if replied.from_user.last_name:
                name = replied.from_user.first_name + " " + replied.from_user.last_name
            else:
                name = replied.from_user.first_name
            comment = message.input_str or replied.text
    else:
        await message.err("```Input not found!...```", del_in=3)
        return
    await message.delete()
    await message.edit("```Creating A PH Comment 😜```", del_in=1)
    if replied.from_user.photo:
        pfp_photo = replied.from_user.photo.small_file_id
        file_name = os.path.join(Config.DOWN_PATH, "profile_pic.jpg")
        picture = await userge.download_media(
            pfp_photo,
            file_name=file_name
        )
        loc_f = upload_image(picture)
        os.remove(picture)
    else:
        loc_f = "https://telegra.ph/file/9844536dbba404c227181.jpg"
    path = await phcomment(loc_f, comment, name)
    if path == "ERROR":
        return await message.edit("😔 Something Wrong see Help!", del_in=2)
    chat_id = message.chat.id
    await message.delete()
    await message.client.send_photo(
        chat_id=chat_id,
        photo=path,
        reply_to_message_id=replied.message_id
    )


async def phcomment(text1, text2, text3):
    site = "https://nekobot.xyz/api/imagegen?type=phcomment&image="
    r = requests.get(f"{site}{text1}&text={text2}&username={text3}").json()
    urlx = r.get("message")
    ph_url = url(urlx)
    if not ph_url:
        return "ERROR"
    return urlx
