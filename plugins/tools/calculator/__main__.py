""" basic calculator """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# By @Krishna_Singhal

from userge import userge, Message


@userge.on_cmd("calculate", about={
    'header': "calculate given string",
    'usage': "{tr}calculate 5*(19-9)/9+45"})
async def calculate(message: Message):
    """ calculate given expression """

    given = message.input_str
    if not given:
        return await message.err("input not found!")

    try:
        await message.edit(
            f"**GIVEN:**\n`{given}`\n\n"
            f"**OUTPUT:**\n`{eval(given)}`"
        )
    except Exception as e:
        await message.err(str(e))
