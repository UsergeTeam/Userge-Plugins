# pylint: disable=missing-module-docstring
#
# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from os import environ


class Dynamic:
    ANTISPAM_SENTRY: bool = True


class Config:
    USERGE_ANTISPAM_API = environ.get("USERGE_ANTISPAM_API")
    SPAM_WATCH_API = environ.get("SPAM_WATCH_API")
