# Plugin By @ZekXtreme
# Base Script by <https://github.com/xcscxr>

import os
import re
import base64
import requests
from bs4 import BeautifulSoup

from userge import Message, userge

crypt = os.environ.get("CRYPT")


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
