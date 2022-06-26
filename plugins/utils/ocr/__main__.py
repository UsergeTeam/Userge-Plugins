""" ocr reader """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os

from pyrogram import enums

from userge import userge, Message, config
from .. import ocr

CHANNEL = userge.getCLogger(__name__)


@userge.on_cmd("ocr", about={
    'header': "use this to run ocr reader",
    'description': "get ocr result for images (file size limit = 1MB)",
    'examples': [
        "{tr}ocr [reply to image]",
        "{tr}ocr eng [reply to image] (get lang codes from 'https://ocr.space/ocrapi')"]})
async def ocr_gen(message: Message):
    """
    this function can generate ocr output for a image file
    """
    if ocr.OCR_SPACE_API_KEY is None:
        await message.edit(
            "<code>Oops!!get the OCR API from</code> "
            "<a href='https://eepurl.com/bOLOcf'>HERE</a> "
            "<code>& add it to Heroku config vars</code> (<code>OCR_SPACE_API_KEY</code>)",
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML, del_in=0)
        return

    if not message.reply_to_message:
        return await message.err(r"i can't read nothing (°ー°〃)")
    lang_code = message.input_str or "eng"
    await message.edit(r"`Trying to Read.. 📖")
    file_name = await message.reply_to_message.download(config.Dynamic.DOWN_PATH)
    test_file = await ocr.ocr_space_file(file_name, lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except Exception as e_f:
        await message.edit(
            r"`Couldn't read it.. (╯‵□′)╯︵┻━┻`"
            "\n`I guess I need new glasses.. 👓`"
            f"\n\n**ERROR**: `{e_f}`", del_in=0)
        os.remove(file_name)
        return
    else:
        await message.edit(
            "**Here's what I could read from it:**"
            f"\n\n`{ParsedText}`")
        os.remove(file_name)
        return await CHANNEL.log("`ocr` command succefully executed")
