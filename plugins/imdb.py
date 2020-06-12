import re
import os
import bs4
import requests

from userge import userge, Message, Config

THUMB_PATH = Config.DOWN_PATH + "thumb_image.jpg"


@userge.on_cmd("imdb", about={
    'header': "Scrap Movies & Tv Shows from IMDB",
    'usage': "{tr}imdb [Movie Name]"})
async def imdb(message: Message):
    try:
        movie_name = message.input_str
        remove_space = movie_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get(
            "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name + "&s=all")
        # lnk = str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + odds[0].findNext('td').findNext('td').a['href']
        page1 = requests.get(mov_link)
        soup = bs4.BeautifulSoup(page1.content, 'lxml')
        if soup.find('div', 'poster'):
            poster = soup.find('div', 'poster').img['src']
        else:
            poster = ''
        if soup.find('div', 'title_wrapper'):
            pg = soup.find('div', 'title_wrapper').findNext('div').text
            mov_details = re.sub(r'\s+', ' ', pg)
        else:
            mov_details = ''
        credits_ = soup.findAll('div', 'credit_summary_item')
        if len(credits_) == 1:
            director = credits_[0].a.text
            writer = 'Not available'
            stars = 'Not available'
        elif len(credits_) > 2:
            director = credits_[0].a.text
            writer = credits_[1].a.text
            actors = []
            for x in credits_[2].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        else:
            director = credits_[0].a.text
            writer = 'Not available'
            actors = []
            for x in credits_[1].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        if soup.find('div', "inline canwrap"):
            story_line = soup.find('div', "inline canwrap").findAll('p')[0].text
        else:
            story_line = 'Not available'
        info = soup.findAll('div', "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll('a')
                for i in a:
                    if "country_of_origin" in i['href']:
                        mov_country.append(i.text)
                    elif "primary_language" in i['href']:
                        mov_language.append(i.text)
        if soup.findAll('div', "ratingValue"):
            for r in soup.findAll('div', "ratingValue"):
                mov_rating = r.strong['title']
        else:
            mov_rating = 'Not available'
        des_ = f"""<a href='{poster}'>&#8203;</a>
<b>Title🎬: </b><code>{mov_title}</code>

<b>More Info: </b><code>{mov_details}</code>
<b>Rating⭐: </b><code>{mov_rating}</code>
<b>Country🗺: </b><code>{mov_country[0]}</code>
<b>Language: </b><code>{mov_language[0]}</code>
<b>Cast Info🎗: </b>
  <b>Director📽: </b><code>{director}</code>
  <b>Writer📄: </b><code>{writer}</code>
  <b>Stars🎭: </b><code>{stars}</code>

<b>IMDB URL Link🔗: </b>{mov_link}

<b>Story Line : </b><em>{story_line}</em>"""
    except IndexError:
        await message.edit("Bruh, Plox enter **Valid movie name** kthx")

    if os.path.exists(THUMB_PATH):
        await message.reply_photo(
            photo=THUMB_PATH,
            caption=des_,
            parse_mode="HTML"
        )
    else:
        await message.edit(des_, parse_mode="HTML")
