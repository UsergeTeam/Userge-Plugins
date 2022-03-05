# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" search movies/tv series in imdb """

import os

API_ONE_URL = os.environ.get("IMDB_API_ONE_URL")
API_TWO_URL = os.environ.get("IMDB_API_TWO_URL")
API_THREE_URL = os.environ.get("IMDB_API_THREE_URL")
WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", "en_IN")
