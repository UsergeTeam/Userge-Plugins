# pylint: disable=missing-module-docstring
#
# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os


class Config:
    ALIVE_MEDIA = os.environ.get("ALIVE_MEDIA")
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO",
                                   "https://github.com/UsergeTeam/Userge")
