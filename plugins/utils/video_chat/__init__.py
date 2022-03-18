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
from typing import List

from userge import Message
from userge.utils import secured_env

logging.getLogger("pytgcalls").setLevel(logging.WARNING)

QUEUE: List[Message] = []

YTDL_PATH = os.environ.get("YOUTUBE_DL_PATH", "yt_dlp")
MAX_DURATION = int(os.environ.get("MAX_DURATION", 900))
VC_SESSION = secured_env("VC_SESSION_STRING")


class Dynamic:
    PLAYING = False
    CMDS_FOR_ALL = False
