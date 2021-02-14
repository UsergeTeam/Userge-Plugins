""" Virus-Total module to check virus in files """

# By @Krishna_Singhal
# Also see https://github.com/uaudith/VirusTotal-Telegram

import os
import json
import asyncio
import requests

from userge import userge, Message, Config
from userge.utils import progress, humanbytes

API_KEY = os.environ.get("VT_API_KEY", None)


@userge.on_cmd("scan", about={
    'header': "Virus-Total module to check virus in document files.",
    'description': "scan virus in document files which are less then 32MB.",
    'usage': "{tr}scan [reply to document file]"})
async def _scan_file(msg: Message):
    """ scan files and get scan id """
    if API_KEY is None:
        await msg.edit(
            "You have to sign up on `virustotal.com` and get `API_KEY` "
            "and paste in `VT_API_KEY` var.\nFor more info "
            "[see this](https://t.me/UnofficialPluginsHelp/114)."
        )
        return
    replied = msg.reply_to_message
    if not (replied and replied.document):
        await msg.err("you need to reply document file.")
        return
    size_of_file = replied.document.file_size
    if size_of_file > 32 * 1024 * 1024:
        await msg.err("this document is greater than 32MB.")
        return
    await msg.edit("`Downloading file to local...`")
    dls_loc = await msg.client.download_media(
        message=replied,
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(msg, "Downloading file to local...")
    )
    dls = os.path.join(Config.DOWN_PATH, os.path.basename(dls_loc))
    await msg.edit(
        f"`Processing your file`, **File_size:** `{humanbytes(size_of_file)}`")
    response = scan_file(dls)
    os.remove(dls)
    if response is False:
        await msg.err("this file can't be scan")
        return
    await msg.edit(f"`{response.json()['verbose_msg']}`")
    sha1 = response.json()['resource']
    await asyncio.sleep(3)
    que_msg = "Your resource is queued for analysis"
    viruslist = []
    reasons = []
    response = get_report(sha1).json()
    if "Invalid resource" in response.get('verbose_msg'):
        await msg.err(response.get('verbose_msg'))
        return
    if response.get('verbose_msg') == que_msg:
        await msg.edit(f'`{que_msg}`')
        while response.get('verbose_msg') == que_msg:
            await asyncio.sleep(3)
            try:
                response = get_report(sha1).json()
            except json.decoder.JSONDecodeError:
                await asyncio.sleep(3)
    try:
        report = response['scans']
        link = response['permalink']
    except Exception as e:
        await msg.err(e)
        return
    for i in report:
        if report[i]['detected'] is True:
            viruslist.append(i)
            reasons.append('â¤ ' + report[i]['result'])
    if len(viruslist) > 0:
        names = ' , '.join(viruslist)
        reason = '\n'.join(reasons)
        await msg.edit(f"""
☣ __Threats have been detected !__ ☣

**{names}**\n\n__Description__\n\n`{reason}`

[Detailed Report]({link})
""")
    else:
        await msg.edit('`File is clean ✅`')


def scan_file(path: str) -> str:
    """ scan file """
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    path_name = path.split('/')[-1]

    params = {'apikey': API_KEY}
    files = {
        'file': (path_name, open(path, 'rb'))
    }
    response = requests.post(url, files=files, params=params)
    return response


def get_report(sha1: str) -> str:
    """ get report of files """
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {
        'apikey': API_KEY, 'resource': sha1, 'allinfo': 'False'
    }
    response = requests.get(url, params=params)
    return response
