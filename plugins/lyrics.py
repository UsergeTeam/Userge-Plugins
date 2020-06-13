import os

from userge import userge, Message


@userge.on_cmd("glyrics", about={
    'header': "Lyrics",
    'description': "Scrape Song Lyrics from MetroLyrics",
    'usage': "{tr}glyrics [Song Name]",
    'examples': "{tr}glyrics Swalla Nicki Minaj"})
async def glyrics(message: Message):
