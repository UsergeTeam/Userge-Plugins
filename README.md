# Userge-Plugins 💎

[![Build Status](https://travis-ci.com/UsergeTeam/Userge-Plugins.svg?branch=master)](https://travis-ci.com/UsergeTeam/Userge-Plugins) ![Python Version](https://img.shields.io/badge/python-3.8-lightgrey) ![Release](https://img.shields.io/github/v/release/UsergeTeam/Userge) ![Stars](https://img.shields.io/github/stars/UsergeTeam/Userge-Plugins) ![Forks](https://img.shields.io/github/forks/UsergeTeam/Userge-Plugins) ![Issues Open](https://img.shields.io/github/issues/UsergeTeam/Userge-Plugins) ![Issues Closed](https://img.shields.io/github/issues-closed/UsergeTeam/Userge-Plugins) ![PR Open](https://img.shields.io/github/issues-pr/UsergeTeam/Userge-Plugins) ![PR Closed](https://img.shields.io/github/issues-pr-closed/UsergeTeam/Userge-Plugins) ![Contributors](https://img.shields.io/github/contributors/UsergeTeam/Userge-Plugins) ![Repo Size](https://img.shields.io/github/repo-size/UsergeTeam/Userge-Plugins) ![License](https://img.shields.io/github/license/UsergeTeam/Userge-Plugins) ![Commit Activity](https://img.shields.io/github/commit-activity/m/UsergeTeam/Userge-Plugins) [![Main Repo!](https://img.shields.io/badge/Main%20Repo-!-orange)](https://github.com/UsergeTeam/Userge) [![Join Channel!](https://img.shields.io/badge/Join%20Channel-!-red)](https://t.me/theUserge) [![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/UsergeTeam/Userge-Plugins/?ref=repository-badge)

## [Documentation](https://userge.tech) 📘

## [Main Repo](https://github.com/UsergeTeam/Userge) 💡

## Contributing 👥

You can support us by contributing to this project development. If you have any suggestions or improvements, please [create an issue](https://github.com/UsergeTeam/Userge-Plugins/issues/new). Pull Requests are most welcome ! 

## Example Plugin 🤨

```python
from userge import userge, Message, filters

LOG = userge.getLogger(__name__)  # logger object
CHANNEL = userge.getCLogger(__name__)  # channel logger object

# add command handler
@userge.on_cmd("test", about="help text to this command")
async def test_cmd(message: Message):
   LOG.info("starting test command...")  # log to console
   ...
   await message.edit("testing...", del_in=5)  # this will be automatically deleted after 5 sec
   ...
   await CHANNEL.log("testing completed!")  # log to channel

# add filters handler
@userge.on_filters(filters.me & filters.private)  # filter my private messages
async def test_filter(message: Message):
   LOG.info("starting filter command...")
   ...
   await message.reply(f"you typed - {message.text}", del_in=5)
   ...
   await CHANNEL.log("filter executed!")
```

### Support & Discussions 👥

> Head over to the [Discussion Group](https://t.me/slbotsbugs) and [Update Channel](https://t.me/theUserge)

### Copyright & License 👮

* Copyright (C) 2020 - 2022 by [UsergeTeam](https://github.com/UsergeTeam)
* Licensed under the terms of the [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](https://github.com/UsergeTeam/Userge-Plugins/blob/master/LICENSE)
