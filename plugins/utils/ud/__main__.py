""" urban dictionary """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import aiohttp
from pyrogram.types import (
    # TODO
)
from urllib.parse import quote
from ..ud import URBAN_API_URL

from userge import userge, Message


@userge.on_cmd("ud", about={
    'header': "Searches Urban Dictionary for the query",
    'flags': {'-l': "limit : defaults to 1"},
    'usage': "{tr}ud [flag] [query]",
    'examples': ["{tr}ud userge", "{tr}ud -l3 userge"]})
async def urban_dict(message: Message):
    await message.edit("Processing...")
    query = message.filtered_input_str
    if not query:
        await message.err("No found any query!")
        return
    try:
        mean = urbandict.define(query)
    except HTTPError:
        await message.edit(f"Sorry, couldn't find any results for: `{query}`", del_in=5)
        return
    output = ''
    limit = int(message.flags.get('-l', 1))
    for i, mean_ in enumerate(mean, start=1):
        output += f"{i}. **{mean_['def']}**\n" + \
            f"  Examples:\n  * `{mean_['example'] or 'not found'}`\n\n"
        if limit <= i:
            break
    if not output:
        await message.edit(f"No result found for **{query}**", del_in=5)
        return
    output = f"**Query:** `{query}`\n**Limit:** `{limit}`\n\n{output}"
    await message.edit_or_send_as_file(text=output, caption=query)



async def wpraip(query: str) -> List[InlineQueryResultArticle]:
    oorse = []
    async with aiohttp.ClientSession() as requests:
        two = await (
            await requests.get(
                URBAN_API_URL.format(
                    Q=quote(query)
                )
            )
        ).json()
        for term in two.get("list", []):
            message_text = (
                "ℹ️ Definition of {term.get('word')}\n"
                "{term.get('definition')}\n"
                "\n"
                "📌 Example\n"
                "{term.get('example')}"
            )
            oorse.append(
                InlineQueryResultArticle(
                    title=term.get("word", " "),
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode="html",
                        disable_web_page_preview=False
                    ),
                    url=term.get("permalink"),
                    description=term.get("definition", " ")
                )
            )
    return oorse
            
        
