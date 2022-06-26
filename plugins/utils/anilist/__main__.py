""" Search for Anime related Info """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# Module Capable of fetching Anime, Airing, Character Info &
# Anime Reverse Search made for UserGe.
# AniList Api (GitHub: https://github.com/AniList/ApiV2-GraphQL-Docs)
# Anime Reverse Search Powered by tracemoepy.
# TraceMoePy (GitHub: https://github.com/DragSama/tracemoepy)
# (C) Author: Phyco-Ninja (https://github.com/Phyco-Ninja) (@PhycoNinja13b)
#
# All rights reserved.

import os
from datetime import datetime

import flag as cflag
import humanize
import tracemoepy
from aiohttp import ClientSession
from html_telegraph_poster import TelegraphPoster
from tracemoepy.errors import ServerError

from userge import userge, Message, get_collection, config
from userge.utils import progress, take_screen_shot

# Logging Errors
CLOG = userge.getCLogger(__name__)

# Default templates for Query Formatting
ANIME_TEMPLATE = """[{c_flag}]**{romaji}**

**ID | MAL ID:** `{idm}` | `{idmal}`
➤ **SOURCE:** `{source}`
➤ **TYPE:** `{formats}`
➤ **GENRES:** `{genre}`
➤ **SEASON:** `{season}`
➤ **EPISODES:** `{episodes}`
➤ **STATUS:** `{status}`
➤ **NEXT AIRING:** `{air_on}`
➤ **SCORE:** `{score}%` 🌟
➤ **ADULT RATED:** `{adult}`
🎬 {trailer_link}
📖 [Synopsis & More]({synopsis_link})"""

SAVED = get_collection("TEMPLATES")

# GraphQL Queries.
ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String, $type: MediaType, $asHtml: Boolean) {
  Media (id: $id, idMal: $idMal, search: $search, type: $type) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    description (asHtml: $asHtml)
    startDate {
      year
      month
      day
    }
    season
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
      thumbnail
    }
    coverImage {
      extraLarge
    }
    bannerImage
    genres
    averageScore
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    isAdult
    characters (role: MAIN, page: 1, perPage: 10) {
      nodes {
        id
        name {
          full
          native
        }
        image {
          large
        }
        description (asHtml: $asHtml)
        siteUrl
      }
    }
    studios (isMain: true) {
      nodes {
        name
        siteUrl
      }
    }
    siteUrl
  }
}
"""

AIRING_QUERY = """
query ($id: Int, $mediaId: Int, $notYetAired: Boolean) {
  Page(page: 1, perPage: 50) {
    airingSchedules (id: $id, mediaId: $mediaId, notYetAired: $notYetAired) {
      id
      airingAt
      timeUntilAiring
      episode
      mediaId
      media {
        title {
          romaji
          english
          native
        }
        duration
        coverImage {
          extraLarge
        }
        nextAiringEpisode {
          airingAt
          timeUntilAiring
          episode
        }
        bannerImage
        averageScore
        siteUrl
      }
    }
  }
}
"""

CHARACTER_QUERY = """
query ($search: String, $asHtml: Boolean) {
  Character (search: $search) {
    id
    name {
      full
      native
    }
    image {
      large
    }
    description (asHtml: $asHtml)
    siteUrl
    media (page: 1, perPage: 25) {
      nodes {
        id
        idMal
        title {
          romaji
          english
          native
        }
        type
        siteUrl
        coverImage {
          extraLarge
        }
        bannerImage
        averageScore
        description (asHtml: $asHtml)
      }
    }
  }
}
"""


@userge.on_start
async def _init():
    global ANIME_TEMPLATE  # pylint: disable=global-statement
    template = await SAVED.find_one({'_id': "ANIME_TEMPLATE"})
    if template:
        ANIME_TEMPLATE = template['anime_data']


async def return_json_senpai(query, vars_):
    """ Makes a Post to https://graphql.anilist.co. """
    url_ = "https://graphql.anilist.co"
    async with ClientSession() as api_:
        post_con = await api_.post(url_, json={'query': query, 'variables': vars_})
        json_data = await post_con.json()
        return json_data


def post_to_tp(a_title, content):
    """ Create a Telegram Post using HTML Content """
    post_client = TelegraphPoster(use_api=True)
    auth_name = "@PhycoNinja13b"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=a_title,
        author=auth_name,
        author_url="https://t.me/PhycoNinja13b",
        text=content
    )
    return post_page['url']


def make_it_rw(time_stamp, as_countdown=False):
    """ Converting Time Stamp to Readable Format """
    if as_countdown:
        now = datetime.now()
        air_time = datetime.fromtimestamp(time_stamp)
        return str(humanize.naturaltime(now - air_time))
    return str(humanize.naturaldate(datetime.fromtimestamp(time_stamp)))


@userge.on_cmd("anime", about={
    'header': "Anime Search",
    'description': "Search for Anime using AniList API",
    'flags': {
        '-mid': "Search Anime using MAL ID",
        '-wp': "Get webpage previews "},
    'usage': "{tr}anime [flag] [anime name | ID]",
    'examples': [
        "{tr}anime 98444", "{tr}anime -mid 39576",
        "{tr}anime Asterisk war"]})
async def anim_arch(message: Message):
    """ Search Anime Info """
    query = message.filtered_input_str
    if not query:
        await message.err("NameError: 'query' not defined")
        return
    vars_ = {
        'search': query,
        'asHtml': True,
        'type': "ANIME"
    }
    if query.isdigit():
        vars_ = {
            'id': int(query),
            'asHtml': True,
            'type': "ANIME"
        }
        if '-mid' in message.flags:
            vars_ = {
                'idMal': int(query),
                'asHtml': True,
                'type': "ANIME"
            }

    result = await return_json_senpai(ANIME_QUERY, vars_)
    error = result.get('errors')
    if error:
        await CLOG.log(f"**ANILIST RETURNED FOLLOWING ERROR:**\n\n`{error}`")
        error_sts = error[0].get('message')
        await message.err(f"[{error_sts}]")
        return

    data = result['data']['Media']

    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get('id')
    idmal = data.get('idMal')
    romaji = data['title']['romaji']
    english = data['title']['english']
    native = data['title']['native']
    formats = data.get('format')
    status = data.get('status')
    synopsis = data.get('description')
    season = data.get('season')
    episodes = data.get('episodes')
    duration = data.get('duration')
    country = data.get('countryOfOrigin')
    c_flag = cflag.flag(country)
    source = data.get('source')
    coverImg = data.get('coverImage')['extraLarge']
    bannerImg = data.get('bannerImage')
    genres = data.get('genres')
    genre = genres[0]
    if len(genres) != 1:
        genre = ", ".join(genres)
    score = data.get('averageScore')
    air_on = None
    if data['nextAiringEpisode']:
        nextAir = data['nextAiringEpisode']['airingAt']
        air_on = make_it_rw(nextAir)
    s_date = data.get('startDate')
    adult = data.get('isAdult')
    trailer_link = "N/A"

    if data['trailer'] and data['trailer']['site'] == 'youtube':
        trailer_link = f"[Trailer](https://youtu.be/{data['trailer']['id']})"
    html_char = ""
    for character in data['characters']['nodes']:
        html_ = ""
        html_ += "<br>"
        html_ += f"""<a href="{character['siteUrl']}">"""
        html_ += f"""<img src="{character['image']['large']}"/></a>"""
        html_ += "<br>"
        html_ += f"<h3>{character['name']['full']}</h3>"
        html_ += f"<em>{c_flag} {character['name']['native']}</em><br>"
        html_ += f"<b>Character ID</b>: {character['id']}<br>"
        html_ += f"<h4>About Character and Role:</h4>{character.get('description', 'N/A')}"
        html_char += f"{html_}<br><br>"

    studios = ""
    for studio in data['studios']['nodes']:
        studios += "<a href='{}'>• {}</a> ".format(studio['siteUrl'], studio['name'])
    url = data.get('siteUrl')

    title_img = coverImg or bannerImg
    # Telegraph Post mejik
    html_pc = ""
    html_pc += f"<img src='{title_img}' title={romaji}/>"
    html_pc += f"<h1>[{c_flag}] {native}</h1>"
    html_pc += "<h3>Synopsis:</h3>"
    html_pc += synopsis
    html_pc += "<br>"
    if html_char:
        html_pc += "<h2>Main Characters:</h2>"
        html_pc += html_char
        html_pc += "<br><br>"
    html_pc += "<h3>More Info:</h3>"
    html_pc += f"<b>Started On:</b> {s_date['day']}/{s_date['month']}/{s_date['year']}"
    html_pc += f"<br><b>Studios:</b> {studios}<br>"
    html_pc += f"<a href='https://myanimelist.net/anime/{idmal}'>View on MAL</a>"
    html_pc += f"<a href='{url}'> View on anilist.co</a>"
    html_pc += f"<img src='{bannerImg}'/>"

    title_h = english or romaji
    synopsis_link = post_to_tp(title_h, html_pc)
    try:
        finals_ = ANIME_TEMPLATE.format(**locals())
    except KeyError as kys:
        await message.err(kys)
        return

    if '-wp' in message.flags:
        finals_ = f"[\u200b]({title_img}) {finals_}"
        await message.edit(finals_)
        return
    await message.reply_photo(title_img, caption=finals_)
    await message.delete()


@userge.on_cmd("airing", about={
    'header': "Airing Info",
    'description': "Fetch Airing Detail of a Anime",
    'usage': "{tr}airing [Anime Name | Anilist ID]",
    'examples': "{tr}airing 108632"})
async def airing_anim(message: Message):
    """ Get Airing Detail of Anime """
    query = message.input_str
    if not query:
        await message.err("NameError: 'query' not defined")
        return
    vars_ = {
        'search': query,
        'asHtml': True,
        'type': "ANIME"
    }
    if query.isdigit():
        vars_ = {
            'id': int(query),
            'asHtml': True,
            'type': "ANIME"
        }
    result = await return_json_senpai(ANIME_QUERY, vars_)
    error = result.get('errors')
    if error:
        await CLOG.log(f"**ANILIST RETURNED FOLLOWING ERROR:**\n\n`{error}`")
        error_sts = error[0].get('message')
        await message.err(f"[{error_sts}]")
        return

    data = result['data']['Media']

    # Airing Details
    mid = data.get('id')
    romaji = data['title']['romaji']
    english = data['title']['english']
    native = data['title']['native']
    status = data.get('status')
    episodes = data.get('episodes')
    country = data.get('countryOfOrigin')
    c_flag = cflag.flag(country)
    source = data.get('source')
    coverImg = data.get('coverImage')['extraLarge']
    genres = data.get('genres')
    genre = genres[0]
    if len(genres) != 1:
        genre = ", ".join(genres)
    score = data.get('averageScore')
    air_on = None
    if data['nextAiringEpisode']:
        nextAir = data['nextAiringEpisode']['airingAt']
        episode = data['nextAiringEpisode']['episode']
        air_on = make_it_rw(nextAir, True)

    title_ = english or romaji
    out = f"[{c_flag}] **{native}** \n   (`{title_}`)"
    out += f"\n\n**ID:** `{mid}`"
    out += f"\n**Status:** `{status}`\n"
    out += f"**Source:** `{source}`\n"
    out += f"**Score:** `{score}`\n"
    out += f"**Genres:** `{genre}`\n"
    if air_on:
        out += f"**Airing Episode:** `[{episode}/{episodes}]`\n"
        out += f"\n`{air_on}`"
    if len(out) > 1024:
        await message.edit(out)
        return
    await message.reply_photo(coverImg, caption=out)
    await message.delete()


@userge.on_cmd("scheduled", about={
    'header': "Scheduled Animes",
    'description': "Fetch a list of Scheduled Animes from "
                   "AniList API. [<b>Note:</b> If Query exceeds "
                   "Limit (i.e. 9 aprox) remaining Animes from "
                   "will be directly posted to Log Channel "
                   "to avoid Spam of Current Chat.]",
    'usage': "{tr}scheduled"})
async def get_schuled(message: Message):
    """ Get List of Scheduled Anime """
    var = {'notYetAired': True}
    await message.edit("`Fetching Scheduled Animes`")
    result = await return_json_senpai(AIRING_QUERY, var)
    error = result.get('errors')
    if error:
        await CLOG.log(f"**ANILIST RETURNED FOLLOWING ERROR:**\n\n{error}")
        error_sts = error[0].get('message')
        await message.err(f"[{error_sts}]")
        return

    data = result['data']['Page']['airingSchedules']
    c = 0
    totl_schld = len(data)
    out = ""
    for air in data:
        romaji = air['media']['title']['romaji']
        english = air['media']['title']['english']
        mid = air['mediaId']
        epi_air = air['episode']
        air_at = make_it_rw(air['airingAt'], True)
        site = air['media']['siteUrl']
        title_ = english or romaji
        out += f"<h3>[🇯🇵]{title_}</h3>"
        out += f" • <b>ID:</b> {mid}<br>"
        out += f" • <b>Airing Episode:</b> {epi_air}<br>"
        out += f" • <b>Next Airing:</b> {air_at}<br>"
        out += f" • <a href='{site}'>[Visit on anilist.co]</a><br><br>"
        c += 1
    if out:
        out_p = f"<h1>Showing [{c}/{totl_schld}] Scheduled Animes:</h1><br><br>{out}"
        link = post_to_tp("Scheduled Animes", out_p)
        await message.edit(f"[Open in Telegraph]({link})")


@userge.on_cmd("character", about={
    'header': "Anime Character",
    'description': "Get Info about a Character and much more",
    'usage': "{tr}character [Name of Character]",
    'examples': "{tr}character Subaru Natsuki"})
async def character_search(message: Message):
    """ Get Info about a Character """
    query = message.input_str
    if not query:
        await message.err("NameError: 'query' not defined")
        return
    var = {
        'search': query,
        'asHtml': True
    }
    result = await return_json_senpai(CHARACTER_QUERY, var)
    error = result.get('errors')
    if error:
        await CLOG.log(f"**ANILIST RETURNED FOLLOWING ERROR:**\n\n`{error}`")
        error_sts = error[0].get('message')
        await message.err(f"[{error_sts}]")
        return

    data = result['data']['Character']

    # Character Data
    id_ = data['id']
    name = data['name']['full']
    native = data['name']['native']
    img = data['image']['large']
    site_url = data['siteUrl']
    description = data['description']
    featured = data['media']['nodes']

    sp = 0
    cntnt = ""
    for cf in featured:
        out = "<br>"
        out += f'''<img src="{cf['coverImage']['extraLarge']}"/>'''
        out += "<br>"
        title = cf['title']['english'] if cf['title']['english'] else cf['title']['romaji']
        out += f"<h3>{title}</h3>"
        out += f"<em>[🇯🇵] {cf['title']['native']}</em><br>"
        out += f'''<a href="{cf['siteUrl']}>{cf['type']}</a><br>'''
        out += f"<b>Media ID:</b> {cf['id']}<br>"
        out += f"<b>SCORE:</b> {cf['averageScore']}/100<br>"
        out += cf.get('description', "N/A") + "<br>"
        cntnt += out
        sp += 1
        if sp > 5:
            break

    html_cntnt = f"<img src='{img}' title={name}/>"
    html_cntnt += f"<h1>[🇯🇵] {native}</h1>"
    html_cntnt += "<h3>About Character:</h3>"
    html_cntnt += description
    html_cntnt += "<br>"
    if cntnt:
        html_cntnt += "<h2>Top Featured Anime</h2>"
        html_cntnt += cntnt
        html_cntnt += "<br><br>"
    url_ = post_to_tp(name, html_cntnt)
    cap_text = f"""[🇯🇵] __{native}__
    (`{name}`)
**ID:** {id_}
[About Character]({url_})

[Visit Website]({site_url})"""

    await message.reply_photo(img, caption=cap_text)
    await message.delete()


@userge.on_cmd("ars", about={
    'header': "Anime Reverse Search",
    'description': "Reverse Search any anime by providing "
                   "a snap, or short clip of anime.",
    'usage': "{tr}ars [reply to Photo/Gif/Video]"})
async def trace_bek(message: Message):
    """ Reverse Search Anime Clips/Photos """
    replied = message.reply_to_message
    if not replied:
        await message.edit("Ara Ara... Reply to a Media Senpai")
        return
    if not (replied.photo or replied.video or replied.animation):
        await message.err("Nani, reply to gif/photo/video")
        return
    if not os.path.isdir(config.Dynamic.DOWN_PATH):
        os.makedirs(config.Dynamic.DOWN_PATH)
    await message.edit("He he, let me use my skills")
    dls = await message.client.download_media(
        message=message.reply_to_message,
        file_name=config.Dynamic.DOWN_PATH,
        progress=progress,
        progress_args=(message, "Downloading Media")
    )
    dls_loc = os.path.join(config.Dynamic.DOWN_PATH, os.path.basename(dls))
    if replied.animation or replied.video:
        img_loc = os.path.join(config.Dynamic.DOWN_PATH, "trace.png")
        await take_screen_shot(dls_loc, 0, img_loc)
        if not os.path.lexists(img_loc):
            await message.err("Media not found...", del_in=5)
            return
        os.remove(dls_loc)
        dls_loc = img_loc
    if dls_loc:
        async with ClientSession() as session:
            tracemoe = tracemoepy.AsyncTrace(session=session)
            try:
                search = await tracemoe.search(dls_loc, upload_file=True)
            except ServerError:
                try:
                    search = await tracemoe.search(dls_loc, upload_file=True)
                except ServerError:
                    await message.reply('Couldnt parse results!!!')
                    return
            result = search["result"][0]
            caption_ = (
                f"**Title**: {result['anilist']['title']['english']}"
                f" (`{result['anilist']['title']['native']}`)\n"
                f"\n**Anilist ID:** `{result['anilist']['id']}`"
                f"\n**Similarity**: `{(str(result['similarity']*100))[:5]}`"
                f"\n**Episode**: `{result['episode']}`"
            )
            preview = result['video']
        await message.reply_video(preview, caption=caption_)
        await message.delete()


@userge.on_cmd("setemp", about={
    'header': "Anime Template",
    'description': "Set your own Custom Anime Template "
                   "that will be used to format .anime "
                   "searches [<b>NOTE:</b> Requires "
                   "proper key to be entered in curly braces]",
    'usage': "{tr}setemp [Reply to text Message | Content]"})
async def ani_save_template(message: Message):
    """ Set Custom Template for .anime """
    text = message.input_or_reply_str
    if not text:
        await message.err("Invalid Syntax")
        return
    await SAVED.update_one({'_id': "ANIME_TEMPLATE"}, {"$set": {'anime_data': text}}, upsert=True)
    await message.edit("Custom Anime Template Saved")


@userge.on_cmd("anitemp", about={
    'header': "Anime Template Settings",
    'description': "Remove or View current Custom "
                   "that is being used. ",
    'flags': {
        '-d': "Delete Saved Template",
        '-v': "View Saved Template"},
    'usage': "{tr}anitemp [A valid flag]"})
async def view_del_ani(message: Message):
    """ View or Delete .anime Template """
    if not message.flags:
        await message.err("Flag Required")
        return
    template = await SAVED.find_one({'_id': "ANIME_TEMPLATE"})
    if not template:
        await message.err("No Custom Anime Template Saved Peru")
        return
    if "-d" in message.flags:
        await SAVED.delete_one({'_id': "ANIME_TEMPLATE"})
        await message.edit("Custom Anime Template deleted Successfully")
    if "-v" in message.flags:
        await message.edit(template['anime_data'])
