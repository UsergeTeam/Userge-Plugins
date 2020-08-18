""" Auto Update Bio """

# By @Krishna_Singhal

import time
import asyncio

from pyrogram.errors import FloodWait

from resources.quotes import ENGLISH_QUOTES, HINDI_QUOTES
from userge import userge, Message

BIO_UPDATION = False
AUTOBIO_TIMEOUT = 300

CHANNEL = userge.getCLogger(__name__)
LOG = userge.getLogger(__name__)


@userge.on_cmd("autobio", about={
    'header': "Auto Updates your Profile Bio with 2 languages.",
    'usage': "{tr}autobio (for eng)\n{tr}autobio Hi (for hindi)"})
async def auto_bio(msg: Message):
    """ Auto Update Your Bio """

    global BIO_UPDATION
    if BIO_UPDATION:
        if isinstance(BIO_UPDATION, asyncio.Task):
            BIO_UPDATION.cancel()
        BIO_UPDATION = False

        await msg.edit(
            "Auto Bio Updation is **Stopped** Successfully...", log=__name__, del_in=5)
        return

    if not msg.input_str:
        bio_quotes = ENGLISH_QUOTES
    elif 'hi' in msg.input_str.lower():
        bio_quotes = HINDI_QUOTES
    else:
        await msg.err("Given Input is Invalid...")
        return

    await msg.edit(
        "Auto Bio Updation is **Started** Successfully...", log=__name__, del_in=3)
    BIO_UPDATION = asyncio.get_event_loop().create_task(autobio_worker(msg, bio_quotes))


async def autobio_worker(msg: Message, bio_quotes: list):

    quotes = bio_quotes
    while BIO_UPDATION:
        for k in range(29):
            if not BIO_UPDATION:
                break

            try:
                await msg.client.update_profile(bio=quotes[k])

            except FloodWait as s_c:
                time.sleep(s_c.x)
            except Exception as e:
                LOG.error(e)

            await asyncio.sleep(AUTOBIO_TIMEOUT)
            await CHANNEL.log("Updating Next Quote...")
