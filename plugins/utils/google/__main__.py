""" google search """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from search_engine_parser import GoogleSearch

from pyrogram.types import (
    LinkPreviewOptions
)

from userge import userge, Message

GoogleSearch.parse_soup = lambda __, _: _.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe")


@userge.on_cmd("google", about={
    'header': "do a Google search",
    'flags': {
        '-p': "page of results to return (default to 1)",
        '-l': "limit the number of returned results (defaults to 5)(max 10)"},
    'usage': "{tr}google [flags] [query | reply to msg]",
    'examples': "{tr}google -p4 -l10 github-userge"})
async def gsearch(message: Message):
    query = message.filtered_input_str
    await message.edit(f"**Googling** for `{query}` ...")
    flags = message.flags
    page = int(flags.get('-p', 1))
    limit = int(flags.get('-l', 5))
    if message.reply_to_message:
        query = message.reply_to_message.text
    if not query:
        await message.err("Give a query or reply to a message to google!")
        return
    try:
        g_search = GoogleSearch()
        gresults = await g_search.async_search(query, page)
    except Exception as e:
        await message.err(e)
        return
    output = ""
    for i in range(limit):
        try:
            title = gresults["titles"][i].replace("\n", " ")
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            output += f"[{title}]({link})\n"
            output += f"`{desc}`\n\n"
        except (IndexError, KeyError):
            break
    output = f"**Google Search:**\n`{query}`\n\n**Results:**\n{output}"
    await message.edit_or_send_as_file(text=output, caption=query,
                                       link_preview_options=LinkPreviewOptions(is_disabled=True))
