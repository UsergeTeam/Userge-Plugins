""" scrape articles """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import re
from asyncio import sleep

from newspaper import Article, ArticleException

from userge import userge, Message

regex: str = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.' \
             r'[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*))'
max_chars = 3900


@userge.on_cmd("con", about={
    'header': "Scrape article content",
    'usage': "{tr}con [link | reply to msg]"})
async def con_(message: Message):
    """ Articles Scraper """
    text = message.input_str
    if message.reply_to_message:
        text = message.reply_to_message.text
    if not text:
        await message.err("Input not found")
        return
    try:
        url: str = re.search(regex, text).group(1)
        article: Article = Article(url)
        article.download()
        article.parse()
        # split article content into chunks
        # credits to https://github.com/eternnoir/pyTelegramBotAPI/blob/
        # 2dec4f1ffc3f7842844e747b388edf0d6560a5b6/telebot/util.py#L224
        chunks = [article.text[i:i + max_chars] for i in range(0, len(article.text), max_chars)]
        header = f"**{article.title}**\n{article.publish_date}\n\n"
        if len(chunks) == 1:
            await message.edit(header + article.text)
        else:
            await message.edit(header + chunks[0])
            for chunk in chunks[1:]:
                await message.reply(chunk)
                await sleep(2)
    except AttributeError:
        await message.edit("`Can't find a valid URL!`")
    except ArticleException:
        await message.edit("`Failed to scrape the article!`")
