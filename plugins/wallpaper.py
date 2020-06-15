"""Wallpaper Module"""
from userge import userge, Message, Config
from bs4 import BeautifulSoup as soup
import requests
from random import randint, choice
import os
import asyncio
from PIL import Image

down_p = str(Config.DOWN_PATH.rstrip('/'))


async def dlimg(link):
    e = requests.get(link).content
    paea = 'donno.{}'.format(link.split('.')[-1])
    path_i = os.path.join(down_p, paea)
    with open(path_i, 'wb') as k:
        k.write(e)
    return path_i


async def walld(strin: str):
    if len(strin.split()) > 1:
        strin = '+'.join(strin.split())
    url = 'https://wall.alphacoders.com/search.php?search='
    none_got = ['https://wall.alphacoders.com/finding_wallpapers.php']
    none_got.append('https://wall.alphacoders.com/search-no-results.php')
               
    page_link = 'https://wall.alphacoders.com/search.php?search={}&page={}'
    resp = requests.get(f'{url}{strin}')
    if resp.url in none_got:
        return False
    if 'by_category.php' in resp.url:
        page_link = str(resp.url).replace('&amp;', '') + '&page={}'
        check_link = True
    else:
        check_link = False
    resp = soup(resp.content, 'lxml')
    try:
        page_num = resp.find('div', {'class': 'visible-xs'})
        page_num = page_num.find('input', {'class': 'form-control'})
        page_num = int(page_num['placeholder'].split(' ')[-1])
    except Exception:
        page_num = 1
    n = randint(1, page_num)
    if page_num != 1:
        if check_link:
            resp = requests.get(page_link.format(n))
        else:
            resp = requests.get(page_link.format(strin, n))
        resp = soup(resp.content, 'lxml')
    a_s = resp.find_all('a')
    list_a_s = []
    tit_links = []
    r = ['thumb', '350', 'img', 'big.php?i', 'data-src', 'title']
    for a_tag in a_s:
        if all(d in str(a_tag) for d in r):
            list_a_s.append(a_tag)
    try:
        for df in list_a_s:
            imgi = df.find('img')
            li = str(imgi['data-src']).replace('thumb-350-', '')
            titl = str(df['title']).replace('|', '')
            titl = titl.replace('  ', '')
            titl = titl.replace('Image', '')
            titl = titl.replace('HD', '')
            titl = titl.replace('Wallpaper', '')
            titl = titl.replace('Background', '')
            p = (li, titl)
            tit_links.append(p)
    except Exception:
        pass
    del list_a_s
    if len(tit_links) != 0:
        tit_link = choice(tit_links)
    else:
        return False
    return tit_link


@userge.on_cmd("wall", about={
    'header': "Search Wallpaper",
    'description': '''Search and Download Hd Wallpaper from
alphacoders and upload to Telegram''',
    'usage': "{tr}wall [Query], [Second Query]",
    'examples': "{tr}wall luffy",
    'Another Example': "`{tr}wall Luffy, Naruto`"
})
async def idk_sir(message: Message):
    if not os.path.isdir(down_p):
        os.makedirs(down_p)
    cat_id = message.chat.id
    if message.input_str:
        qu = message.input_str
        for q in qu.split(','):
            q = q.strip()
            await message.edit(f'**Processing...**\n**Searching for **`{q}`')
            try:
                link = await walld(str(q))
            except Exception as e:
                await message.edit(e)
                return
            if link:
                idl = await dlimg(link[0])
                if link[0].endswith('png'):
                    im = Image.open(idl)
                    idl = idl.replace('png', 'jpeg')
                    im = im.convert('RGB')
                    im.save(idl, 'jpeg')
                    os.remove(idl)
                await message.edit('**Uploading...**')
                if not len(link[1].split()) < 11:
                    capo = '**' + ' '.join(link[1].split()[:11]) + '**'
                else:
                    capo = '**' + link[1] + '**'
                try:
                    await userge.send_photo(cat_id, idl, caption=capo)
                    await userge.send_document(cat_id, idl)
                    os.remove(idl)
                except Exception as e:
                    await message.edit(e)
            else:
                await message.edit('**Result Not Found**')
        await asyncio.sleep(3)
        await message.delete()
    else:
        await message.edit('**Give me Something to search.**')
        await userge.send_sticker(cat_id, 'CAADAQADmQADTusQR6fPCVZ3EhDoFgQ')
