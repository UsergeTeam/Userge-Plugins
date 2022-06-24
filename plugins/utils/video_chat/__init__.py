# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" manage video chats """

import os
import logging
from typing import List, Union

from pyrogram import Client
from pyrogram.types import Message as RawMessage
from pytgcalls import PyTgCalls

from userge import userge, config
from userge.utils import secured_env
from .resource import TgResource, UrlResource

logging.getLogger("pytgcalls").setLevel(logging.WARNING)

YTDL_PATH = os.environ.get("YOUTUBE_DL_PATH", "yt_dlp")
MAX_DURATION = int(os.environ.get("MAX_DURATION", 900))
VC_SESSION = secured_env("VC_SESSION_STRING")

if VC_SESSION:
    VC_CLIENT = Client(
        "usergeMusic",
        config.API_ID,
        config.API_HASH,
        session_string=VC_SESSION)
    VC_CLIENT.storage.session_string = VC_SESSION
else:
    userge.__class__.__module__ = 'pyrogram.client'
    VC_CLIENT = userge

call = PyTgCalls(VC_CLIENT, overload_quiet_mode=True)
call._env_checker.check_environment()  # pylint: disable=protected-access

CHANNEL = userge.getCLogger(__name__)
LOG = userge.getLogger()

CURRENT_SONG = {}
CONTROL_CHAT_IDS: List[int] = []
CQ_MSG: List[RawMessage] = []
QUEUE: List[Union[TgResource, UrlResource]] = []
GROUP_CALL_PARTICIPANTS: List[int] = []


class Vars:
    CHAT_NAME = ""
    CHAT_ID = 0
    CLIENT = userge
    BACK_BUTTON_TEXT = ""


class Dynamic:
    PLAYING = False
    CMDS_FOR_ALL = False
