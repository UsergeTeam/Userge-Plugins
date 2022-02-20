""" install any command on any OS """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# Copyright (c) 2019 Łukasz Lach <llach@llach.pl>
# Portions Copyright (c) tl;dr; authors and contributors <https://github.com/tldr-pages/tldr>

import aiohttp
from bs4 import BeautifulSoup

from userge import userge, Message


@userge.on_cmd(
    "cnf",
    about={
        "header": "Install any command on any operating system.",
        "usage": "{tr}cnf\n{tr}cnf [command ]",
        "examples": "{tr}cnf python",
    },
)
async def cnf(message: Message):

    await message.edit("`Searching...`")
    base_url = "https://command-not-found.com/"

    if not message.input_str:
        # find a random command
        async with aiohttp.ClientSession() as ses, ses.get(base_url) as page:
            soup = BeautifulSoup(await page.text(), "lxml")
        cmd = soup.find(
            "a", attrs={"class": "h5 brand-text d-block mb-1 other-command"}
        ).text.strip()
    else:
        cmd = message.input_str.split()[0]

    try:
        async with aiohttp.ClientSession() as ses, ses.get(base_url + cmd) as page:
            soup = BeautifulSoup(await page.text(), "lxml")

        # heading
        payload = f"**[{cmd}]({base_url + cmd})**\n"
        # description
        payload += f"{soup.find('p', attrs = {'class':'my-0'}).text.strip()}\n\n"

        lst = soup.findAll("div", attrs={"class": "command-install"})

        # items
        for row in lst:
            try:
                row["class"][2] == "d-none"
                # ignore this its stil not implemented by Łukasz
                continue
            except IndexError:
                pass
            os = row.dt.findAll(text=True, recursive=False)[-1].strip()
            command = row.dd.code.text

            payload += f"{os}\n`{command}`\n\n"

        await message.edit(payload, disable_web_page_preview=False)
    except IndexError:
        await message.edit("Command Not Found")
    except Exception as err:
        await message.err(err)
