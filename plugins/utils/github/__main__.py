""" Plugin for getting information about an user on GitHub

Syntax: .github USERNAME
"""

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


import requests

from userge import userge, Message


@userge.on_cmd("github", about={
    'header': "Get info about an GitHub User",
    'flags': {'-l': "repo limit : default to 5"},
    'usage': ".github [flag] [username]",
    'examples': [".github cyberboysumanjay", ".github -l5 cyberboysumanjay"]})
async def fetch_github_info(message: Message):
    replied = message.reply_to_message
    username = message.filtered_input_str
    if replied:
        username = replied.text
    if not username:
        await message.err("invalid input !")
        return
    url = "https://api.github.com/users/{}".format(username)
    res = requests.get(url)
    if res.status_code == 200:
        await message.edit("`fetching github info ...`")
        data = res.json()
        photo = data["avatar_url"]
        if data['bio']:
            data['bio'] = data['bio'].strip()
        repos = []
        sec_res = requests.get(data["repos_url"])
        if sec_res.status_code == 200:
            limit = int(message.flags.get('-l', 5))
            for repo in sec_res.json():
                repos.append(f"[{repo['name']}]({repo['html_url']})")
                limit -= 1
                if limit == 0:
                    break
        template = """
\b👤 **Name** : [{name}]({html_url})
🔧 **Type** : `{type}`
🏢 **Company** : `{company}`
🔭 **Blog** : {blog}
📍 **Location** : `{location}`
📝 **Bio** : __{bio}__
❤️ **Followers** : `{followers}`
👁 **Following** : `{following}`
📊 **Public Repos** : `{public_repos}`
📄 **Public Gists** : `{public_gists}`
🔗 **Profile Created** : `{created_at}`
✏️ **Profile Updated** : `{updated_at}`\n""".format(**data)
        if repos:
            template += "🔍 **Some Repos** : " + ' | '.join(repos)
        await message.client.send_photo(chat_id=message.chat.id,
                                        caption=template,
                                        photo=photo,
                                        disable_notification=True)
        await message.delete()
    else:
        await message.edit("No user found with `{}` username!".format(username))
