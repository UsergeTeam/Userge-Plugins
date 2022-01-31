# Plugin By @ZekXtreme
# Base Script by <https://github.com/xcscxr>


import base64
import os
import re

import requests
from lxml import etree
from userge import Message, userge

crypt = os.environ.get("CRYPT")
MD = os.environ.get("APPDRIVE_MD")
PHPSESSID = os.environ.get("PHPSESSID")


def gen_data_string(data, boundary=f'{"-"*6}_'):
    data_string = ''
    for item in data:
        data_string += f'{boundary}\r\n'
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
    data_string += f'{boundary}--\r\n'
    return data_string


def parse_info(data):
    info = re.findall('>(.*?)<\/li>', data)
    info_parsed = {}
    for item in info:
        kv = [s.strip() for s in item.split(':', maxsplit=1)]
        info_parsed[kv[0].lower()] = kv[1]
    return info_parsed


def appdrive_dl(url):
    client = requests.Session()
    client.cookies.update({
        'MD': MD,
        'PHPSESSID': PHPSESSID
    })
    res = client.get(url)
    key = re.findall('"key",\s+"(.*?)"', res.text)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
    info_parsed = parse_info(res.text)
    info_parsed['error'] = False
    info_parsed['link_type'] = 'login'    # direct/login

    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }

    data = {
        'type': 1,
        'key': key
    }

    data['action'] = 'original'

    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
        data['action'] = 'direct'

    while data['type'] <= 3:
        try:
            response = client.post(url, data=gen_data_string(
                data), headers=headers).json()
            break
        except Exception:
            data['type'] += 1
            print(data['type'])

    if 'url' in response:
        info_parsed['gdrive_link'] = response['url']

    elif 'error' in response and response['error']:
        info_parsed['error'] = True
        info_parsed['error_message'] = response['message']

    info_parsed['src_url'] = url

    return info_parsed


@userge.on_cmd("gdtot", about={
    'header': "parse gdtot links",
    'usage': "{tr}gdtot gdtot_link"})
async def gdtot(message: Message):
    """ Gets gdrive link """
    if not crypt:
        return await message.edit(
            "**Oops, You forgot to Set GDTOT Cookies**\n"
            "see [Help](https://telegra.ph/GDTOT-HELP-01-24) ",
            disable_web_page_preview=True)
    client = requests.Session()
    client.cookies.update({'crypt': crypt})
    args = message.input_str
    if not args:
        await message.err("Send a link along with command")
    else:
        try:
            await message.edit("Parsing")
            res = client.get(args)
            title = re.findall(">(.*?)<\/h5>", res.text)[0]
            info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
            res = client.get(
                f"https://new.gdtot.top/dld?id={args.split('/')[-1]}")
            matches = re.findall('gd=(.*?)&', res.text)
            decoded_id = base64.b64decode(str(matches[0])).decode('utf-8')
            gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
            out = (
                f'Title: {title}\n'
                f'Size: {info[0]}\n'
                f'Date: {info[1]}\n'
                f'\nGDrive-URL:\n{gdrive_url}'
            )
            await message.edit(out, disable_web_page_preview=True)
        except Exception:
            await message.err("Unable To parse Link")


@userge.on_cmd("ad", about={
    'header': "parse appdrive links",
    'usage': "{tr}ad appdrive_link"})
async def appdrive(message: Message):
    if not (MD or PHPSESSID):
        return await message.err(
            "First set APPDRIVE_MD & PHPSESSID from appdrive.in\n "
            "before using this plugin",
            disable_web_page_preview=True
        )
    url = message.input_or_reply_str
    if not url:
        await message.err("Send a link along with command")
    else:
        try:
            await message.edit("Parsing.....")
            res = appdrive_dl(url)
            output = f'''Title: {res['name']}\n
            Drive_Link: {res['gdrive_link']}'''
            await message.edit(output, disable_web_page_preview=True)
        except Exception:
            message.err("Unable to get Drive Link")
