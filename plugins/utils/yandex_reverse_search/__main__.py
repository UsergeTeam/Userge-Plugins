""" Yandex reverse search """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# Userge Plugin for Labstack Uploads (https://up.labstack.com)
# Author: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)

from aiofiles import os
from telegraph import upload_file

from userge import userge, config, Message, pool


@userge.on_cmd("yrs", about={
    'header': "Yandex Reverse Search",
    'description': "Reverse Search any Image/sticker",
    'usage': "{tr}yrs [Reply to image | sticker]",
    'note': "Gif & Animated Stickers won't work!"}, check_downpath=True)
async def labstack(message: Message):
    replied = message.reply_to_message
    if replied and (replied.sticker or replied.photo):
        await message.edit("`processing ...`")
        dl_loc = await message.client.download_media(
            message=message.reply_to_message,
            file_name=config.Dynamic.DOWN_PATH,
        )
    else:
        return await message.err("Media not found!")

    try:
        response = await pool.run_in_thread(upload_file)(dl_loc)
    except Exception as t_e:
        await message.err(str(t_e))
    else:
        media_link = f"https://telegra.ph{response[0]}"
        yandex_link = f"https://yandex.com/images/search?rpt=imageview&url={media_link}"
        await message.edit(f"**[Yandex Search Results]({yandex_link})**")
    finally:
        await os.remove(dl_loc)
