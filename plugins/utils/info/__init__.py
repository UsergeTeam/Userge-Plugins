# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" check user's info """

from os import environ

from userge.utils import secure_env


USERGE_ANTISPAM_API = environ.get(secure_env("USERGE_ANTISPAM_API"))
SPAM_WATCH_API = environ.get(secure_env("SPAM_WATCH_API"))
