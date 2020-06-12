from userge import userge, Message, Config
from bs4 import BeautifulSoup as soup
import requests
from random import randint, choice
import os


CHANNEL = userge.getCLogger(__name__)

async def dlimg(link):
    e = requests.get(link).content
    paea = 'donno.{}'.format(link.split('.')[-1])
    path_i = os.path.join(Config.DOWN_PATH, paea)
    with open(path_i, 'wb') as k:
        k.write(e)
    return path_i


async def wall(strin: str):
    if len(strin.split()) > 1:
        strin = '+'.join(strin.split())
    url = 'https://wall.alphacoders.com/search.php?search='
    none_got = 'https://wall.alphacoders.com/finding_wallpapers.php'
    page_link = 'https://wall.alphacoders.com/search.php?search={}&page={}'
    resp = requests.get(f'{url}{strin}')
    if resp.url == none_got:
        return False
    if 'by_category.php' in resp.url:
        page_link = str(resp.url).replace('&amp;', '') + '&page={}'
        check_link = True
    else:
        check_link = False
    resp = soup(resp.content, 'lxml')
    wall_num = resp.find('h1', {'class': 'center title'})
    wall_num = list(wall_num.text.split())
    for i in wall_num:
        try:
            wall_num = int(i)
        except ValueError:
            pass
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
    tit_link = choice(tit_links)
    return tit_link


@userge.on_cmd("wall", about={
    'header': "Search Wallpaper",
    'description': '''Search and Download Hd Wallpaper from
alphacoders and upload to Telegram''',
    'usage': "{tr}wall [Query]",
    'examples': "{tr}wall luffy"
})
async def idk_sir(message: Message):
    if not os.path.isdir(Config.DOWN_PATH):
        os.makedirs(Config.DOWN_PATH)
    if message.input_str:
        qu = message.input_str
        await CHANNEL.log(f"Search Query : {qu}")
        try:
            link = await wall(str(qu))
        except Exception as e:
            await message.edit(e)
            return
        if link:
            await message.edit('**Processing...**')
            idl = await dlimg(link[0])
            await message.edit('**Uploading...**')
            if not len(link[1].split()) < 11:
                capo = '**' + ' '.join(link[1].split()[:11]) + '**'
            else:
                capo = '**' + link[1] + '**'
            try:
                cat_id = message.chat.id
                await userge.send_photo(cat_id, idl, caption=capo)
                await userge.send_document(message.chat.id, idl)
            except Exception as e:
                await message.edit(e)
                return
            await message.delete()
            os.remove(idl)
        else:
            await message.edit('**Result Not Found**')
            await message.reply_sticker('CAADBAADIQEAAl_GARknbPJaYsVA2xYE')
    else:
        await message.edit('**Give me Something to search.**')
        await message.reply_sticker('CAADAQADmQADTusQR6fPCVZ3EhDoFgQ')
