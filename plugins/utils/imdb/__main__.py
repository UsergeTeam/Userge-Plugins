""" search movies/tv series in imdb """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import json
import os
from urllib.parse import urlparse

import requests
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram import enums

from userge import userge, Message, config, pool
from .. import imdb

TMDB_KEY = "5dae31e75ff0f7a0befc272d5deadd73"
THUMB_PATH = config.Dynamic.DOWN_PATH + "imdb_thumb.jpg"


@userge.on_cmd("imdb", about={
    'header': "Scrap Movies & Tv Shows from IMDB",
    'description': "Get info about a Movie on IMDB.\n"
                   "[NOTE: To use a custom poster, download "
                   "the poster with name imdb_thumb.jpg]",
    'usage': "{tr}imdb [Movie Name]",
    'use inline': "@botusername imdb [Movie Name]"})
async def _imdb(message: Message):
    if not (imdb.API_ONE_URL or imdb.API_TWO_URL):
        return await message.err(
            "First set [these two vars](https://t.me/UsergePlugins/127) before using imdb",
            disable_web_page_preview=True
        )
    try:
        movie_name = message.input_str
        await message.edit(f"__searching IMDB for__ : `{movie_name}`")
        response = await _get(imdb.API_ONE_URL.format(theuserge=movie_name))
        srch_results = json.loads(response.text)
        mov_imdb_id = srch_results.get("d")[0].get("id")
        image_link, description = await get_movie_description(
            mov_imdb_id, config.MAX_MESSAGE_LENGTH
        )
    except (IndexError, json.JSONDecodeError, AttributeError):
        await message.edit("Bruh, Plox enter **Valid movie name** kthx")
        return

    if os.path.exists(THUMB_PATH):
        await message.client.send_photo(
            chat_id=message.chat.id,
            photo=THUMB_PATH,
            caption=description,
            parse_mode=enums.ParseMode.HTML
        )
        await message.delete()
    elif image_link is not None:
        await message.client.send_photo(
            chat_id=message.chat.id,
            photo=image_link.replace("_V1_", "_V1_UX720"),
            caption=description,
            parse_mode=enums.ParseMode.HTML
        )
        await message.delete()
    else:
        await message.edit(
            description,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )


async def get_movie_description(imdb_id, max_length):
    response = await _get(imdb.API_TWO_URL.format(imdbttid=imdb_id))
    soup = json.loads(response.text)

    yt_code = None
    response2 = await _get(
        "http://api.themoviedb.org/3/movie/" + imdb_id + "/videos?api_key=" + TMDB_KEY
    )
    soup2 = json.loads(response2.text)
    try:
        yt_code = soup2.get("results")[0].get("key")
    except (IndexError, json.JSONDecodeError, AttributeError, TypeError):
        if soup.get("trailer_vid_id"):
            yt_code = soup.get("trailer_vid_id")

    mov_link = f"https://www.imdb.com/title/{imdb_id}"
    mov_name = soup.get('title')
    image_link = soup.get('poster')
    genres = soup.get("genres")
    duration = soup.get("duration")
    mov_rating = soup.get("UserRating").get("rating")
    if mov_rating.strip() == '/':
        mov_rating = "<code>Ratings not found!</code>"
    else:
        users = soup.get("UserRating").get("numeric_description_only")
        if users:
            mov_rating += f" (based on {users} users)"
    if duration:
        genres.append(duration)

    mov_country, mov_language = get_countries_and_languages(soup)
    director, writer, stars = get_credits_text(soup)
    story_line = soup.get("summary").get("plot", 'Not available')

    description = f"<b>Title</b><a href='{image_link}'>🎬</a>: <code>{mov_name}</code>"
    description += f"""
<b>Genres: </b><code>{' '.join(genres) if len(genres) > 0 else ''}</code>
<b>Rating⭐: </b><code>{mov_rating}</code>
<b>Country🗺: </b><code>{mov_country}</code>
<b>Language: </b><code>{mov_language}</code>
<b>Cast Info🎗: </b>
  <b>Director📽: </b><code>{director}</code>
  <b>Writer📄: </b><code>{writer}</code>
  <b>Stars🎭: </b><code>{stars}</code>

<b>IMDB URL Link🔗: </b>{mov_link}
<b>YOUTUBE TRAILER 🎦: </b> https://m.youtube.com/watch?v={yt_code}

<b>Story Line : </b><em>{story_line}</em>"""

    povas = await search_jw(mov_name, imdb.WATCH_COUNTRY)
    if len(description + povas) > max_length:
        inc = max_length - len(description + povas)
        description = description[:inc - 3].strip() + "..."
    if povas != "":
        description += f"\n\n{povas}"
    return image_link, description


def get_countries_and_languages(soup):
    languages = soup.get("Language")
    countries = soup.get("CountryOfOrigin")
    if languages:
        if len(languages) > 1:
            lg_text = ', '.join(languages)
        else:
            lg_text = languages[0]
    else:
        lg_text = "No Languages Found!"
    if countries:
        if len(countries) > 1:
            ct_text = ', '.join(countries)
        else:
            ct_text = countries[0]
    else:
        ct_text = "No Country Found!"
    return ct_text, lg_text


def get_credits_text(soup):
    pg = soup.get("sum_mary")
    direc = pg.get("Directors")
    writer = pg.get("Writers")
    actor = pg.get("Stars")
    if direc:
        if len(direc) > 1:
            director = ', '.join([x["NAME"] for x in direc])
        else:
            director = direc[0]["NAME"]
    else:
        director = "No Director Found!"
    if writer:
        if len(writer) > 1:
            writers = ', '.join([x["NAME"] for x in writer])
        else:
            writers = writer[0]["NAME"]
    else:
        writers = "No Writer Found!"
    if actor:
        if len(actor) > 1:
            actors = ', '.join([x["NAME"] for x in actor])
        else:
            actors = actor[0]["NAME"]
    else:
        actors = "No Actor Found!"
    return director, writers, actors


@pool.run_in_thread
def _get(url: str, attempts: int = 0) -> requests.Response:
    while True:
        abc = requests.get(url)
        if attempts > 5:
            raise IndexError
        if abc.status_code == 200:
            break
        attempts += 1
    return abc


if userge.has_bot:

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"imdb\((.+)\)"))
    async def imdb_callback(_, c_q: CallbackQuery):
        if c_q.from_user and c_q.from_user.id in config.OWNER_ID:
            imdb_id = str(c_q.matches[0].group(1))
            _, description = await get_movie_description(
                imdb_id, config.MAX_MESSAGE_LENGTH
            )
            await c_q.edit_message_text(
                text=description,
                disable_web_page_preview=False,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Open IMDB!",
                                url=f"https://imdb.com/title/{imdb_id}"
                            )
                        ]
                    ]
                )
            )
        else:
            await c_q.answer("This is not for you", show_alert=True)

    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("imdb ")
                and inline_query.from_user
                and inline_query.from_user.id in config.OWNER_ID
            ),
            # https://t.me/UserGeSpam/359404
            name="ImdbInlineFilter"
        ),
        group=-1
    )
    async def inline_fn(_, inline_query: InlineQuery):
        movie_name = inline_query.query.split("imdb ")[1].strip()
        search_results = await _get(imdb.API_ONE_URL.format(theuserge=movie_name))
        srch_results = json.loads(search_results.text)
        asroe = srch_results.get("d")
        oorse = []
        for sraeo in asroe:
            title = sraeo.get("l", "")
            description = sraeo.get("q", "")
            stars = sraeo.get("s", "")
            imdb_url = f"https://imdb.com/title/{sraeo.get('id')}"
            year = sraeo.get("yr", "").rstrip('-')
            image_url = sraeo.get("i").get("imageUrl")
            message_text = f"<a href='{image_url}'>🎬</a>"
            message_text += f"<a href='{imdb_url}'>{title} {year}</a>"
            oorse.append(
                InlineQueryResultArticle(
                    title=f" {title} {year}",
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode=enums.ParseMode.HTML,
                        disable_web_page_preview=False
                    ),
                    url=imdb_url,
                    description=f" {description} | {stars}",
                    thumb_url=image_url,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Get IMDB details",
                                    callback_data=f"imdb({sraeo.get('id')})"
                                )
                            ]
                        ]
                    )
                )
            )
        resfo = srch_results.get("q")
        await inline_query.answer(results=oorse,
                                  switch_pm_text=f"Found {len(oorse)} results for {resfo}",
                                  switch_pm_parameter="imdb")
        inline_query.stop_propagation()


async def search_jw(movie_name: str, locale: str):
    m_t_ = ""
    if not imdb.API_THREE_URL:
        return m_t_
    response = await _get(imdb.API_THREE_URL.format(
        q=movie_name,
        L=locale
    ))
    soup = json.loads(response.text)
    items = soup["items"]
    for item in items:
        if movie_name.lower() == item.get("title", "").lower():
            offers = item.get("offers", [])
            t_m_ = []
            for offer in offers:
                url = offer.get("urls").get("standard_web")
                if url not in t_m_:
                    p_o = get_provider(url)
                    m_t_ += f"<a href='{url}'>{p_o}</a> | "
                t_m_.append(url)
            if m_t_ != "":
                m_t_ = m_t_[:-2].strip()
            break
    return m_t_


def get_provider(url):

    def pretty(names):
        name = names[1]
        if names[0] == "play":
            name = "Google Play Movies"
        return name.title()

    netloc = urlparse(url).netloc
    return pretty(netloc.split('.'))
