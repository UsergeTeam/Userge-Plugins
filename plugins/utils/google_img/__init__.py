# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" google image search """

import os

from userge.utils import secured_env

GCS_API_KEY = secured_env("GCS_API_KEY")
GCS_IMAGE_E_ID = os.environ.get("GCS_IMAGE_E_ID")
