# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" last.fm module """

import os

import pylast

from userge import config

API_KEY = os.environ.get("FM_API")
API_SECRET = os.environ.get("FM_SECRET")
USERNAME = os.environ.get("FM_USERNAME")
PASSWORD = pylast.md5(os.environ.get("FM_PASSWORD"))
CHAT_IDS = [
    int(x) for x in os.environ.get("LASTFM_CHAT_ID", str(config.LOG_CHANNEL_ID)).split()
]
