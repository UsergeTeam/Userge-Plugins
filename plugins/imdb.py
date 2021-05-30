import re
import os

import bs4
import wget
import requests

from userge import userge, Message, Config, pool

THUMB_PATH = Config.DOWN_PATH + "imdb_thumb.jpg"


@userge.on_cmd("imdb", about={
    'header': "Scrap Movies & Tv Shows from IMDB",
    'description': "Get info about a Movie on IMDB.\n"
                   "[NOTE: To use a custom poster, download "
                   "the poster with name imdb_thumb.jpg]",
    'usage': "{tr}imdb [Movie Name]"})
async def imdb(message: Message):
    try:
        movie_name = message.input_str
        await message.edit(f"__searching IMDB for__ : `{movie_name}`")
        final_name = movie_name.replace(' ', '+')
        page = await _get(
            f"https://www.imdb.com/find?ref_=nv_sr_fn&q={final_name}&s=all")
        soup = bs4.BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + odds[0].findNext('td').findNext('td').a['href']
        page1 = await _get(mov_link)
        soup = bs4.BeautifulSoup(page1.content, 'lxml')
        image_link = soup.find('a', attrs={"class": "ipc-lockup-overlay ipc-focusable"})
        mov_details = get_movie_details(soup)
        director, writer, stars = get_credits_text(soup)
        story = soup.find('div', attrs={"class": "ipc-html-content ipc-html-content--base"})
        if story:
            story_line = story.findAll('div')[0].text
        else:
            story_line = 'Not available'
        mov_country, mov_language = get_countries_and_languages(soup)
        pg = soup.find('div', attrs={"data-testid": "hero-title-block__aggregate-rating__score"})
        if pg:
            rating = [i.text for i in pg]
            voted_users = pg.findNext('div').findNext('div').text
            mov_rating = f"{rating[0]}{rating[1]} based on {voted_users} users ratings."
        else:
            mov_rating = 'Not available'
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
    if os.path.exists(THUMB_PATH):
        if len(des_) > 1024:
            des_ = des_[:1021] + "..."
        await message.client.send_photo(
            chat_id=message.chat.id,
            photo=THUMB_PATH,
            caption=des_,
            parse_mode="html"
        )
        await message.delete()
    elif image_link is not None:
        await message.edit("__downloading thumb ...__")
        image = await get_image(image_link)
        if image:
            img_path = await pool.run_in_thread(
                wget.download
            )(image, os.path.join(Config.DOWN_PATH, 'imdb_thumb.jpg'))
            if len(des_) > 1024:
                des_ = des_[:1021] + "..."
            await message.client.send_photo(
                chat_id=message.chat.id,
                photo=img_path,
                caption=des_,
                parse_mode="html"
            )
            await message.delete()
            os.remove(img_path)
        else:
            if len(des_) > 1024:
                des_ = des_[:1021] + "..."
            await message.edit(des_, parse_mode="HTML")
    else:
        if len(des_) > 1024:
            des_ = des_[:1021] + "..."
        await message.edit(des_, parse_mode="HTML")


def get_movie_details(soup):
    mov_details = []
    inline = soup.find('ul', attrs={"class": "ipc-inline-list"})
    if inline:
        inline = soup.find('ul', attrs={"class": "ipc-inline-list"})
        if ["titleblockmetadata" in a.lower() for a in inline.attrs['class']]:
            for i in inline.findAll('li'):
                mov_details.append(i.span.text.strip() if i.span else i.text.strip())
    tags = soup.find('div', attrs={"class": "ipc-chip-list"})
    if tags:
        for i in tags.findAll('a'):
            mov_details.append(i.text.strip())
    if mov_details:
        return ' | '.join(mov_details)
    return ''


def get_countries_and_languages(soup):
    languages = []
    countries = []
    pg = soup.find('div', attrs={"data-testid": "title-details-section"})
    if pg:
        for li in pg.findNext('ul'):
            detail_header = li.span.text if li.span else None
            print(detail_header)
            if detail_header == "Country of origin":
                for ct in li.findAll(
                    'a', attrs={"class": "ipc-metadata-list-item__list-content-item"}
                ):
                    countries.append(ct.text.strip())
            elif detail_header == "Languages":
                for lg in li.findAll(
                    'a', attrs={"class": "ipc-metadata-list-item__list-content-item"}
                ):
                    languages.append(lg.text.strip())
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
        ct_text = "No Writer Found!"
    return ct_text, lg_text


def get_credits_text(soup):
    direc = []
    writer = []
    actor = []
    pg = soup.find('ul', attrs={"class": "ipc-metadata-list"})
    if pg:
        for data in pg:
            credit_name = data.span.text if data.span else data.a.text
            for name in data.findAll('a', {"class": "ipc-metadata-list-item__list-content-item"}):
                if credit_name == "Director":
                    direc.append(name.text.strip())
                if credit_name == "Writers":
                    writer.append(name.text.strip())
                if credit_name == "Stars":
                    actor.append(name.text.strip())
    director = writers = actors = ""
    if direc:
        if len(direc) > 1:
            director = ', '.join(direc)
        else:
            director = direc[0]
    else:
        director = "No Director Found!"
    if writer:
        if len(writer) > 1:
            writers = ', '.join(writer)
        else:
            writers = writer[0]
    else:
        writers = "No Writer Found!"
    if actor:
        if len(actor) > 1:
            actors = ', '.join(actor)
        else:
            actors = actor[0]
    else:
        director = "No Actor Found!"
    return director, writers, actors


async def get_image(image_link: str):
    image_content = await _get(
        "https://imdb.com" + image_link.get("href").replace("/?ref_=tt_ov_i", "")
    )
    soup = bs4.BeautifulSoup(image_content.content, 'lxml')

    for i in soup.findAll("img"):
        if "portraitimage" in i.attrs['class'][0].lower():
            return i.get("src")
    return None


@pool.run_in_thread
def _get(url: str) -> requests.Response:
    return requests.get(url)
