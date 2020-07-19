#!/usr/bin/env python3
# https://github.com/Sorrow446/ZS-DL
# plugin by @aryanvikash

import os
import re
import sys
import json
import time
import requests
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote
import asyncio
from userge import userge, Message


@userge.on_cmd("zippy", about={
    'description': "generate Direct link of zippyshare url",
    'usage': "{tr}zippy : [Zippyshare Link ]",
    'examples': "{tr}zippy https://www10.zippyshare.com/v/dyh988sh/file.html"}, del_pre=True)
async def zippyshare(m: Message):
    url = m.filtered_input_str
    loop = asyncio.get_event_loop()
    await m.edit("Generating url ....")
    try:
        direct_url, fname = await loop.run_in_executor(None, generate_zippylink, url)

        await m.edit(f"Original : `{url}`\n\nFilename :`{fname}` \n\nDirect link : `{direct_url}`")

    except Exception as e:
        await m.edit(f"`{e}`")


# From Here script part starts

def decrypt_dlc(abs):
    # Thank you, dcrypt owner(s).
    url = "http://dcrypt.it/decrypt/paste"
    r = s.post(url, data={
        'content': open(abs)
    }
    )
    r.raise_for_status()
    j = json.loads(r.text)
    if not j.get('success'):
        raise Exception(j)
    return j['success']['links']


def check_url(url):
    regex = r'https://www(\d{1,3}).zippyshare.com/v/([a-zA-Z\d]{8})/file.html'
    match = re.match(regex, url)
    if match:
        return match.group(1), match.group(2)
    raise ValueError("Invalid URL: " + str(url))


def extract(url, server, id):
    regex = (
        r'document.getElementById\(\'dlbutton\'\).href = "/d/'
        r'([a-zA-Z\d]{8})/" \+ \((\d*) % (\d*) \+ (\d*) % '
        r'(\d*)\) \+ "/(.*)";'
    )
    for _ in range(3):
        r = s.get(url)
        if r.status_code != 500:
            break
        time.sleep(1)
    r.raise_for_status()
    meta = re.search(regex, r.text)
    if not meta:
        raise Exception('Failed to get file URL. Down?')
    num_1 = int(meta.group(2))
    num_2 = int(meta.group(3))
    num_3 = int(meta.group(4))
    num_4 = int(meta.group(5))
    enc_fname = meta.group(6)
    final_num = num_1 % num_2 + num_3 % num_4
    file_url = "https://www{}.zippyshare.com/d/{}/{}/{}".format(server,
                                                                id,
                                                                final_num,
                                                                enc_fname)
    fname = unquote(enc_fname)
    return file_url, fname


def get_file(ref, url):
    s.headers.update({
        'Range': "bytes=0-",
        'Referer': ref
    })
    r = s.get(url, stream=True)
    del s.headers['Range']
    del s.headers['Referer']
    r.raise_for_status()
    length = int(r.headers['Content-Length'])
    return r, length


def generate_zippylink(url):
    global s
    s = requests.Session()
    s.headers.update({
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        "/75.0.3770.100 Safari/537.36"
    })
    server, id = check_url(url)

    return extract(url, server, id)
