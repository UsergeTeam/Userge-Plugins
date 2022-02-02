# Plugin By @ZekXtreme
# Base Script by <https://github.com/xcscxr>

import os
import re
import json
import base64
import requests
from bs4 import BeautifulSoup

from userge import Message, userge, pool

CRYPT = os.environ.get("CRYPT")
MD = os.environ.get("APPDRIVE_MD")


async def _init():
    global CRYPT, MD  # pylint: disable=global-statement
    if CRYPT:
        try:
            crypt = json.loads(CRYPT)
        except Exception:
            pass  # user entered only crypt value from dict
        else:
            CRYPT = crypt.get("cookie").split('=')[-1]
    if MD:
        try:
            md = json.loads(MD)
        except Exception:
            pass  # user entered only crypt value from dict
        else:
            MD = md.get("cookie").split(';')[0].split('=')[-1]


def gen_data_string(data, boundary=f'{"-"*6}_'):
    data_string = ''
    for item in data:
        data_string += f'{boundary}\r\n'
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
    data_string += f'{boundary}--\r\n'
    return data_string


def parse_info(data):
    soup = BeautifulSoup(data, 'html.parser')
    info = soup.find_all('li', {'class': 'list-group-item'})
    info_parsed = {}
    for item in info:
        kv = [s.strip() for s in item.text.split(':', maxsplit=1)]
        info_parsed[kv[0].lower()] = kv[1]
    return info_parsed


async def appdrive_dl(url):

    client = requests.Session()
    client.cookies.update({'MD': MD})

    res = await pool.run_in_thread(client.get)(url)
    key = re.findall(r'"key",\s+"(.*?)"', res.text)[0]
    soup = BeautifulSoup(res.content, 'html.parser')
    ddl_btn = soup.find('button', {'id': 'drc'})
    info_parsed = parse_info(res.text)
    info_parsed['error'] = False
    info_parsed['link_type'] = 'login'  # direct/login

    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        "user-agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/97.0.4692.99 Safari/537.36")
    }

    data = {
        'key': key,
        'action': 'original'
    }

    if ddl_btn:
        info_parsed['link_type'] = 'direct'
        data['action'] = 'direct'

    for i in range(1, 4):
        data['type'] = i
        try:
            response = (await pool.run_in_thread(client.post)(
                url,
                data=gen_data_string(data),
                headers=headers
            )).json()
            break
        except Exception as e:
            response = {
                'error': True,
                'message': str(e)
            }
    if 'url' in response:
        info_parsed['gdrive_link'] = response['url']

    elif response.get('error'):
        info_parsed['error'] = True
        info_parsed['error_message'] = response['message']

    return info_parsed


@userge.on_cmd("gdtot", about={
    'header': "parse gdtot links",
    'description': "you have to set <code>CRYPT</code>.\nget it by reading "
                   "<a href='https://t.me/UnofficialPluginsHelp/129'>help</a>.",
    'usage': "{tr}gdtot gdtot_link"})
async def gdtot(message: Message):
    """ Gets gdrive link """
    if not CRYPT:
        return await message.err("read .help gdtot")
    client = requests.Session()
    client.cookies.update({'crypt': CRYPT})
    args = message.input_str
    if not args:
        await message.err("Send a link along with command")
    else:
        try:
            await message.edit("Parsing...")
            res = await pool.run_in_thread(client.get)(args)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find(
                'h5', {'class': lambda x: x and "modal-title" not in x}).text
            info = soup.find_all('td', {'align': 'right'})
            res = await pool.run_in_thread(client.get)(
                f"https://new.gdtot.top/dld?id={args.split('/')[-1]}")
            matches = re.findall(r'gd=(.*?)&', res.text)
            decoded_id = base64.b64decode(str(matches[0])).decode('utf-8')
            gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
            out = (
                f'Title: {title.strip()}\n'
                f'Size: {info[0].text.strip()}\n'
                f'Date: {info[1].text.strip()}\n'
                f'\nGDrive-URL:\n{gdrive_url}'
            )
            await message.edit(out, disable_web_page_preview=True)
        except Exception:
            await message.err("Unable To parse Link")


@userge.on_cmd("appdrive", about={
    'header': "parse appdrive links",
    'description': "you have to set <code>APPDRIVE_MD</code>.\nget it by reading "
                   "<a href='https://t.me/UnofficialPluginsHelp/129'>help</a>.",
    'usage': "{tr}appdrive appdrive_link"})
async def appdrive(message: Message):
    if not MD:
        return await message.err("read .help appdrive")
    url = message.input_or_reply_str
    if not url:
        await message.err("Send a link along with command")
    else:
        try:
            await message.edit("Parsing.....")
            res = await appdrive_dl(url)
            if res.get('error') and res.get('error_message'):
                raise Exception(res.get('error_message'))
            output = (
                f'Title: {res.get("name")}\n'
                f'Format: {res.get("format")}\n'
                f'Size: {res.get("size")}\n'
                f'Drive_Link: {res.get("gdrive_link")}'
            )
            await message.edit(output, disable_web_page_preview=True)
        except Exception as e:
            await message.err(e)
