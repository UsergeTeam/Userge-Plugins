""" urban dictionary """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from json.decoder import JSONDecodeError
from typing import List
from urllib.parse import quote

import aiohttp
from pyrogram import filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from pyrogram import enums

from userge import userge, Message, config
from ..ud import URBAN_API_URL


@userge.on_cmd("ud", about={
    'header': "Searches Urban Dictionary for the query",
    'flags': {'-l': "limit : defaults to 1"},
    'usage': "{tr}ud [flag] [query]",
    'examples': ["{tr}ud userge", "{tr}ud -l3 userge"]})
async def urban_dict(message: Message):
    await message.edit("Processing...")
    query = message.filtered_input_str

    if not query:
        await message.err("Not found any query!")
        return

    try:
        mean = await wpraip(query)
    except JSONDecodeError:
        await message.edit(f"Sorry, couldn't find any results for: `{query}`", del_in=5)
        return

    output = ''
    limit = int(message.flags.get('-l', 1))
    for i, mean_ in enumerate(mean, start=1):
        output += f"{i}. {mean_.input_message_content.message_text}\n\n"
        if limit <= i:
            break

    if not output:
        await message.edit(f"No result found for **{query}**", del_in=5)
        return

    output = f"<b>Query:</b> <code>{query}</code>\n<b>Limit:</b> <code>{limit}</code>\n\n{output}"
    await message.edit_or_send_as_file(text=output, caption=query, parse_mode=enums.ParseMode.HTML)


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
                f"ℹ️ Definition of <b>{term.get('word')}</b>\n"
                f"<code>{term.get('definition')}</code>\n"
                "\n"
                "📌 Example\n"
                f"<u>{term.get('example')}</u>"
            )
            oorse.append(
                InlineQueryResultArticle(
                    title=term.get("word", " "),
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode=enums.ParseMode.HTML,
                        disable_web_page_preview=False
                    ),
                    url=term.get("permalink"),
                    description=term.get("definition", " ")
                )
            )
    return oorse


if userge.has_bot:

    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("ud ")
                and inline_query.from_user
                and inline_query.from_user.id in config.OWNER_ID
            ),
            # https://t.me/UserGeSpam/359404
            name="UdInlineFilter"
        ),
        group=-2
    )
    async def inline_fn(_, inline_query: InlineQuery):
        query = inline_query.query.split("ud ")[1].strip()
        try:
            riqa = await wpraip(query)
            switch_pm_text = f"Found {len(riqa)} results for {query}"
        except JSONDecodeError:
            riqa = []
        if not riqa:
            switch_pm_text = f"Sorry, couldn't find any results for: {query}"
        await inline_query.answer(results=riqa[:49], switch_pm_text=switch_pm_text,
                                  switch_pm_parameter="ud")
        inline_query.stop_propagation()
