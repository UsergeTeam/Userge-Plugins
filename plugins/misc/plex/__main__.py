# Copyright (C) 2022 by Fatih Ka. (xybydy), < https://github.com/xybydy >.
#
# This file is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" plex api support """

import asyncio
import argparse
import os
import pickle
import re
from functools import wraps
from urllib.parse import unquote

from plexapi import utils
from plexapi.exceptions import BadRequest
from plexapi.myplex import MyPlexAccount
from plexapi.video import Episode, Movie, Show

from userge import userge, Message, config, get_collection, pool


_CREDS: object = None
_ACTIVE_SERVER: object = None


_LOG = userge.getLogger(__name__)
_SAVED_SETTINGS = get_collection("CONFIGS")


_VALID_TYPES: tuple = (Movie, Episode, Show)
SESSION_FILE = 'session'

server = None

user = None

@userge.on_start
async def _init() -> None:
    global _CREDS  # pylint: disable=global-statement
    _LOG.debug("Setting Plex DBase...")
    result = await _SAVED_SETTINGS.find_one({'_id': 'PLEX'}, {'creds': 1})
    _CREDS = pickle.loads(result['creds']) if result else None  # nosec

async def _set_creds(creds: object) -> str:
    global _CREDS  # pylint: disable=global-statement
    _LOG.info("Setting Creds...")
    _CREDS = creds
    result = await _SAVED_SETTINGS.update_one(
        {'_id': 'PLEX'}, {"$set": {'creds': pickle.dumps(creds)}}, upsert=True)
    if result.upserted_id:
        return "`Creds Added`"
    return "`Creds Updated`"

async def _clear_creds() -> str:
    global _CREDS  # pylint: disable=global-statement
    _CREDS = None
    _LOG.info("Clearing Creds...")
    if await _SAVED_SETTINGS.find_one_and_delete({'_id': 'PLEX'}):
        return "`Creds Cleared`"
    return "`Creds Not Found`"

def creds_dec(func):
    """ decorator for check CREDS """
    @wraps(func)
    async def wrapper(self):
        # pylint: disable=protected-access
        if _CREDS:
            await func(self)
        else:
            await self._message.edit("Please run `.plogin` first", del_in=5)
    return wrapper

@userge.on_cmd("plogin", about={'header': "Login Plex",
'usage': "{tr}plogin [username password]",'examples': "{tr}plogin uname passwd"})
async def plogin(message: Message):
    """ setup creds """
    msg = message.input_str.split(" ")
    if len(msg) != 2:
        await message.edit("Invalid usage. Please check usage `.help plogin`")
    else:
        trimmed_uname = msg[0].strip()
        trimmed_passwd = msg[1].strip()
        if trimmed_uname == "" and trimmed_passwd == "":
            await message.edit("Username or password seem to be empty. Check them.")
            return
        else:
            class Opts:
                username = trimmed_uname
                password = trimmed_passwd 
            try:
                _LOG.debug(Opts.username,Opts.password)
                account = utils.getMyPlexAccount(Opts)
            except BadRequest as e:
                await message.edit("Plex login failed. Please check logs.")
                _LOG.exception(e)
            else:
                await asyncio.gather(
                _set_creds(account),
                message.edit("`Saved Plex Creds!`", del_in=3, log=__name__))

# u = User(session=account._session, token=account.authenticationToken)

def __get_filename(part):
    return os.path.basename(part.file)

@userge.on_cmd("pserver", about={'header': "Get Plex Server List",
'usage': "{tr}pserver\n{tr}pserver [no of server]",'examples': "{tr}pserver 1",
"description": "Command to get server list and set default active server"})
async def pservers(message: Message):
    """ plex list servers """
    if message.input_str:
        pass

    servers = [s for s in _CREDS.resources() if 'server' in s.provides]
    msg = ""
    for i in range(len(servers)):
        msg+=f"{i}. {servers[i]}\n"

    await message.edit("The servers are:\n{}".format(msg))


def search_for_item(url=None, account=None):
    global server
    if url: return get_item_from_url(url, account)
    servers = [s for s in account.resources() if 'server' in s.provides]
    server = utils.choose('Choose a Server', servers, 'name').connect()
    query = input('What are you looking for?: ')
    item = []
    items = [i for i in server.search(query) if i.__class__ in _VALID_TYPES]
    items = utils.choose('Choose result', items, lambda x: '(%s) %s' % (x.type.title(), x.title[0:60]))

    if not isinstance(items, list):
        items = [items]

    for i in items:
        if isinstance(i, Show):
            display = lambda i: '%s %s %s' % (i.grandparentTitle, i.seasonEpisode, i.title)
            selected_eps = utils.choose('Choose episode', i.episodes(), display)
            if isinstance(selected_eps, list):
                item += selected_eps
            else:
                item.append(selected_eps)

        else:
            item.append(i)

    if not isinstance(item, list):
        item = [item]

    return item


def get_item_from_url(url, account=None):
    global server
    # Parse the ClientID and Key from the URL
    clientid = re.findall('[a-f0-9]{40}', url)
    key = re.findall('key=(.*?)(&.*)?$', url)
    if not clientid or not key:
        raise SystemExit('Cannot parse URL: %s' % url)
    clientid = clientid[0]
    key = unquote(key[0][0])
    # Connect to the server and fetch the item
    servers = [r for r in account.resources() if r.clientIdentifier == clientid]
    if len(servers) != 1:
        raise SystemExit('Unknown or ambiguous client id: %s' % clientid)
    server = servers[0].connect()
    return server.fetchItem(key)





def download_url(url, account):
    items = get_item_from_url(url, account)

    for item in items:
        if isinstance(item, Show):
            for episode in item.episodes():
                if not os.path.exists(episode.parentTitle):
                    os.mkdir(episode.parentTitle)
                for part in episode.iterParts():
                    filename = __get_filename(part)
                    url = item.url('%s?download=1' % part.key, )
        else:
            for part in item.iterParts():
                filename = __get_filename(part)
                url = item.url('%s?download=1' % part.key, )
