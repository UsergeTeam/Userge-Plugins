""" auto fastly """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# By @AsmSafone

import asyncio
import os

from userge import userge, Message, filters, config, get_collection
from ...utils import ocr

IS_ENABLED = False
USER_DATA = get_collection("CONFIGS")

CHANNEL = userge.getCLogger(__name__)
LOG = userge.getLogger(__name__)


@userge.on_start
async def _init() -> None:
    global IS_ENABLED  # pylint: disable=global-statement
    data = await USER_DATA.find_one({'_id': 'AUTO_FASTLY'})
    if data:
        IS_ENABLED = data['on']


@userge.on_cmd("autofastly", about={
    'header': "Auto Fastly Response",
    'description': "enable or disable auto fastly response",
    'usage': "{tr}autofastly"},
    allow_channels=False, allow_via_bot=False)
async def autofastly(msg: Message):
    """
    Auto Fastly Response
    """
    global IS_ENABLED  # pylint: disable=global-statement
    if ocr.OCR_SPACE_API_KEY is None:
        await msg.edit(
            "<code>Oops!!get the OCR API from</code> "
            "<a href='http://eepurl.com/bOLOcf'>HERE</a> "
            "<code>& add it to Heroku config vars</code> (<code>OCR_SPACE_API_KEY</code>)",
            disable_web_page_preview=True,
            parse_mode="html", del_in=0)
        return

    if IS_ENABLED:
        IS_ENABLED = False
        USER_DATA.update_one({'_id': 'AUTO_FASTLY'},
                             {"$set": {'on': False}}, upsert=True)
        await asyncio.sleep(1)
        await msg.edit(
            "Auto Fastly Response is **Disabled** Successfully...", log=__name__, del_in=5)
        return

    IS_ENABLED = True
    USER_DATA.update_one({'_id': 'AUTO_FASTLY'},
                            {"$set": {'on': True}}, upsert=True)
    await asyncio.sleep(1)
    await msg.edit(
        "Auto Fastly Response is **Enabled** Successfully...", log=__name__, del_in=5)


@userge.on_filters(filters.photo & filters.incoming & filters.group
    & filters.user([1806208310, 1983714367, 1877720720, 5053950120]), group=-1)
async def fastly_handler(msg: Message):
    if not IS_ENABLED:
        return
    img = await msg.download(config.Dynamic.DOWN_PATH)
    parse = await ocr.ocr_space_file(img)
    try:
        text = parse["ParsedResults"][0]["ParsedText"]
    except Exception as e_x:  # pylint: disable=broad-except
        LOG.error(e_x)
        os.remove(img)
        return
    else:
        text = text.split("By@")[0].replace("\n", "").replace("\r", "")
        await msg.reply_text(text.capitalize(), quote=True)
        CHANNEL.log(f'Auto Fastly Responded in {msg.chat.title} [{msg.chat.id}]')
    if os.path.exists(img):
        os.remove(img)
