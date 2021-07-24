import json
import os
import requests
import wget
from operator import truediv
from PIL import Image

from userge import userge, Message, Config, pool

THUMB_PATH = Config.DOWN_PATH + "imdb_thumb.jpg"
# ask in @UserGeSpam to get API URLs
# Please don't steal this code.
API_ONE_URL = os.environ.get("IMDB_API_ONE_URL")
API_TWO_URL = os.environ.get("IMDB_API_TWO_URL")


@userge.on_cmd("imdb", about={
    'header': "Scrap Movies & Tv Shows from IMDB",
    'description': "Get info about a Movie on IMDB.\n"
                   "[NOTE: To use a custom poster, download "
                   "the poster with name imdb_thumb.jpg]",
    'usage': "{tr}imdb [Movie Name]"})
async def imdb(message: Message):
    if not (API_ONE_URL or API_TWO_URL):
        return await message.err(
            "First set [these two vars](https://t.me/UnofficialPluginsHelp/127) before using imdb",
            disable_web_page_preview=True
        )
    try:
        movie_name = message.input_str
        await message.edit(f"__searching IMDB for__ : `{movie_name}`")
        search_results = await _get(API_ONE_URL.format(theuserge=movie_name))
        srch_results = json.loads(search_results.text)
        first_movie = srch_results.get("d")[0]
        mov_title = first_movie.get("l")
        mov_imdb_id = first_movie.get("id")
        mov_link = f"https://www.imdb.com/title/{mov_imdb_id}"
        page2 = await _get(API_TWO_URL.format(imdbttid=mov_imdb_id))
        second_page_response = json.loads(page2.text)
        image_link = first_movie.get("i").get("imageUrl")
        mov_details = get_movie_details(second_page_response)
        director, writer, stars = get_credits_text(second_page_response)
        story_line = second_page_response.get("summary").get("plot", 'Not available')
        mov_country, mov_language = get_countries_and_languages(second_page_response)
        mov_rating = second_page_response.get("UserRating").get("description")
        des_ = f"""<b>Title🎬: </b><code>{mov_title}</code>

<b>More Info: </b><code>{mov_details}</code>
<b>Rating⭐: </b><code>{mov_rating}</code>
<b>Country🗺: </b><code>{mov_country}</code>
<b>Language: </b><code>{mov_language}</code>
<b>Cast Info🎗: </b>
  <b>Director📽: </b><code>{director}</code>
  <b>Writer📄: </b><code>{writer}</code>
  <b>Stars🎭: </b><code>{stars}</code>

<b>IMDB URL Link🔗: </b>{mov_link}

<b>Story Line : </b><em>{story_line}</em>"""
    except IndexError:
        await message.edit("Bruh, Plox enter **Valid movie name** kthx")
        return
    if len(des_) > 1024:
        des_ = des_[:1021] + "..."
    if os.path.exists(THUMB_PATH):
        optimize_image(THUMB_PATH)
        await message.client.send_photo(
            chat_id=message.chat.id,
            photo=THUMB_PATH,
            caption=des_,
            parse_mode="html"
        )
        await message.delete()
    elif image_link is not None:
        await message.edit("__downloading thumb ...__")
        image = image_link
        img_path = await pool.run_in_thread(
            wget.download
        )(image, os.path.join(Config.DOWN_PATH, 'imdb_thumb.jpg'))
        optimize_image(img_path)
        await message.client.send_photo(
            chat_id=message.chat.id,
            photo=img_path,
            caption=des_,
            parse_mode="html"
        )
        await message.delete()
        os.remove(img_path)
    else:
        await message.edit(des_, parse_mode="HTML")


def optimize_image(path):
    _image = Image.open(path)
    if _image.size[0] > 720:
        _image.resize((720, round(truediv(*_image.size[::-1]) * 720))).save(path, quality=95)


def get_movie_details(soup):
    mov_details = []
    inline = soup.get("Genres")
    if inline and len(inline) > 0:
        for io in inline:
            mov_details.append(io)
    tags = soup.get("duration")
    if tags:
        mov_details.append(tags)
    if mov_details and len(mov_details) > 1:
        mov_details_text = ' | '.join(mov_details)
    else:
        mov_details_text = mov_details[0] if mov_details else ''
    return mov_details_text


def get_countries_and_languages(soup):
    languages = soup.get("Language")
    countries = soup.get("CountryOfOrigin")
    lg_text = ""
    if languages:
        if len(languages) > 1:
            lg_text = ', '.join([lng["NAME"] for lng in languages])
        else:
            lg_text = languages[0]["NAME"]
    else:
        lg_text = "No Languages Found!"
    if countries:
        if len(countries) > 1:
            ct_text = ', '.join([ctn["NAME"] for ctn in countries])
        else:
            ct_text = countries[0]["NAME"]
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
