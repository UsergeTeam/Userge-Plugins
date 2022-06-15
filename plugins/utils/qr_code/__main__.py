""" Generate QR code or get QR code data """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# by @krishna_singhal

import asyncio
import os

import qrcode
from bs4 import BeautifulSoup

from userge import userge, config, Message


@userge.on_cmd("mkqr", about={
    'header': "Returns Qr code of text or replied text",
    'usage': "{tr}mkqr [text | reply to text msg]"})
async def make_qr(message: Message):
    """ Make Qr code """
    replied = message.reply_to_message
    input_ = message.input_str
    if input_:
        text = input_
    elif replied:
        text = input_ if input_ else replied.text
    else:
        await message.err("```Input not found...```")
        return
    await message.edit("```Creating a Qr Code...```")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.webp", "PNG")
    await message.delete()
    await userge.send_sticker(
        message.chat.id,
        "qrcode.webp",
        reply_to_message_id=replied.id if replied else None
    )
    os.remove("qrcode.webp")


@userge.on_cmd("getqr", about={
    'header': "Get data of any qr code",
    'usage': "{tr}getqr [Reply to qr code]"})
async def get_qr(message: Message):
    """ Get Qr code data """
    replied = message.reply_to_message
    if not (replied and replied.media and (replied.photo or replied.sticker)):
        await message.err("```reply to qr code to get data...```", del_in=5)
        return
    if not os.path.isdir(config.Dynamic.DOWN_PATH):
        os.makedirs(config.Dynamic.DOWN_PATH)
    await message.edit("```Downloading media to my local...```")
    down_load = await message.client.download_media(
        message=replied,
        file_name=config.Dynamic.DOWN_PATH
    )
    await message.edit("```Processing your QR Code...```")
    cmd = [
        "curl",
        "-X", "POST",
        "-F", "f=@" + down_load + "",
        "https://zxing.org/w/decode"
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    out_response = stdout.decode().strip()
    err_response = stderr.decode().strip()
    os.remove(down_load)

    if not (out_response or err_response):
        await message.err("```Couldn't get data of this QR Code...```")
        return
    try:
        soup = BeautifulSoup(out_response, "html.parser")
        qr_contents = soup.find_all("pre")[0].text
    except IndexError:
        await message.err("List Index Out Of Range")
        return
    await message.edit(f"**Data Found in this QrCode:**\n`{qr_contents}`")
