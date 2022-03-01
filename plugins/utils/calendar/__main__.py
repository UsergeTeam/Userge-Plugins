""" get calendar """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import calendar  # pylint: disable=W0406
from datetime import datetime

from userge import userge, Message


@userge.on_cmd("calendar", about={
    'header': "Print calendar of any month of any year.",
    'usage': "{tr}calendar\n{tr}calendar [ year | month]",
    'examples': "{tr}calendar 2020 | 6"})
async def _calendar(message: Message):

    if not message.input_str:
        await message.edit("`Searching...`")
        try:
            today = datetime.today()
            input_ = calendar.month(today.year, today.month)
            await message.edit(f"```{input_}```")
        except Exception as e:
            await message.err(e)
        return
    if '|' not in message.input_str:
        await message.err("both year and month required!")
        return
    await message.edit("`Searching...`")
    year, month = message.input_str.split('|', maxsplit=1)
    try:
        input_ = calendar.month(int(year.strip()), int(month.strip()))
        await message.edit(f"```{input_}```")
    except Exception as e:
        await message.err(e)
