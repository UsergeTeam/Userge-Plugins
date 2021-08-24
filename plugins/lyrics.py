import os
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from googlesearch import search

from userge import userge, Message, pool


@userge.on_cmd("glyrics", about={
    'header': "Genius Lyrics",
    'description': "Scrape Song Lyrics from Genius.com",
    'usage': "{tr}glyrics [Song Name]",
    'examples': "{tr}glyrics Swalla Nicki Minaj"})
async def glyrics(message: Message):
    song = message.input_str
    if not song:
        await message.edit("Bruh WTF?")
        return
    await message.edit(f"__Searching Lyrics For {song}__")
    to_search = song + "genius lyrics"
    gen_surl = list(search(to_search, num=1, stop=1))[0]
    async with ClientSession() as ses, ses.get(gen_surl) as res:
        gen_page = await res.text()
    scp = BeautifulSoup(gen_page, 'html.parser')
    lyrics = await get_lyrics(scp)
    if not lyrics:
        await message.edit(f"No Results Found for: `{song}`")
        return
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    lyrics = os.linesep.join((s for s in lyrics.splitlines() if s))
    title = scp.find('title').get_text().split("|")
    writers = await get_writers(scp) or "UNKNOWN"
    lyr_format = ''
    lyr_format += '**' + title[0] + '**\n\n'
    lyr_format += '__' + lyrics + '__'
    lyr_format += "\n\n**Written By: **" + '__' + writers + '__'
    lyr_format += "\n**Source: **" + '`' + title[1] + '`'

    if lyr_format:
        await message.edit(lyr_format)
    else:
        await message.edit(f"No Lyrics Found for **{song}**")


# Added seperate scraping functions to change logic easily in future...
@pool.run_in_thread
def get_lyrics(bs):
    lyrics = bs.find_all("div", class_="eOLwDW")
    if not lyrics:
        return None
    for lyric in lyrics:
        for br in lyric.find_all("br"):
            br.replace_with("\n")
    return "\n".join([x.text for x in lyrics])


@pool.run_in_thread
def get_writers(bs):
    writers = bs.find("div", class_="fognin")
    if writers.contents[0].extract().text == "Written By":
        return writers.text
    return None
