""" get date and time """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from datetime import datetime

from pytz import timezone
from pyrogram import enums

from userge import userge, Message
from . import COUNTRY_CITY

LOG = userge.getLogger(__name__)  # logger object


@userge.on_cmd("dt", about={
    'header': "Get the time and date of a City/Country/Timezone.",
    'flags': {
        '-list | -l': "Gives a list of all Country/City Combos.",
        '-code | -c': "Uses Country_City code given."
    },
    'usage':
        "{tr}dt to show the Time & Date of your predefined City.\n"
        "{tr}dt -list | {tr}dt -l to display all TZ Combo's for the Config.\n"
        "{tr}dt -code | {tr}dt -c to use a defined Country/City combo.",

    'examples': ['{tr}dt', '{tr}dt [Flag]']
}, del_pre=True)
async def grab_time(message: Message):
    LOG.debug("Time: Starting now...")
    country_input = await flag_checks(message)
    if country_input is None:
        return
    country_code = COUNTRY_CITY if not country_input else country_input
    try:
        timezone(country_code)
    except BaseException:
        LOG.debug("Time: Incorrect Country Code...")
        await message.err(" ".join([
            "Unable To Determine Timezone With Given Country Code |",
            country_code, "\nUse the -l flag to see compatible codes."
        ]))
        return
    datetime_now = datetime.now(timezone(country_code))
    date_day = datetime_now.strftime("%d")
    date_time = datetime_now.strftime('%I:%M%p')
    if date_day[0] == "0":
        date_day = date_day[1:]
    if date_time[0] == "0":
        date_time = date_time[1:]
    await message.edit(" ".join(
        ["It's", date_time, "on",
         datetime_now.strftime('%A'), datetime_now.strftime('%B'),
         date_day + ordinal_suffix(int(date_day)), "in",
         country_code.replace("_", " ") + "."
         ]
    ))
    LOG.debug("Time: Command Finished Successfully")


def ordinal_suffix(day: int):
    if 3 < day < 21 or 23 < day < 31:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]


async def flag_checks(message: Message):
    default_message = (
        "<code>Below is a list of all the Timezones Avaliable</code> \n<a "
        "href=https://raw.githubusercontent.com/UsergeTeam/Userge-Plugins/main"
        "/plugins/utils/time/citylist.txt>Click Here!</a>\n<code>Enter one in"
        " your Config Under</code> (<code>COUNTRY_CITY</code>)\n"
        "<code>Ex: America/Los_Angeles</code>")
    if 'list' in message.flags or 'l' in message.flags:
        LOG.debug("Time | FLAG = List: Giving TZ list...")
        await message.edit(default_message, disable_web_page_preview=True,
                           parse_mode=enums.ParseMode.HTML, del_in=30)
        return None

    if 'code' in message.flags or 'c' in message.flags:
        LOG.debug("Time | FLAG = Code: Grabbing Country_Code...")
        flags = message.flags
        country_input = message.filtered_input_str.strip()
        country_input = flags.get('c') or flags.get('code') or country_input
        if not country_input:
            await message.err("No Country_City code found after the flag...")
            return None
        return country_input
    if not COUNTRY_CITY:
        LOG.debug("Time: No Config Set")
        await message.edit(default_message, disable_web_page_preview=True,
                           parse_mode=enums.ParseMode.HTML, del_in=30)
        return None

    return False
