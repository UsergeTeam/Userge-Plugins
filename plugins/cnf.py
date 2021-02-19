"""
MIT License

Copyright (c) 2019 Łukasz Lach <llach@llach.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Portions Copyright (c) tl;dr; authors and contributors <https://github.com/tldr-pages/tldr>
"""

import requests
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
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        cmd = soup.find(
            "a", attrs={"class": "h5 brand-text d-block mb-1 other-command"}
        ).text.strip()
    else:
        cmd = message.input_str.split()[0]

    try:
        page = requests.get(base_url + cmd)
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")

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
