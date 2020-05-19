import heroku3
import requests
import math
import asyncio
from userge import Config, userge, Message

# ================= CONSTANT =================
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
# ================= CONSTANT =================


@userge.on_cmd("usage", outgoing=True, about="__Get Dyno hours usage__")  # pylint:disable=E0602
async def usage(message: Message):
    # async def dyno_usage(dyno):
    """
        Get your account Dyno Usage
    """
    await message.edit("`Processing...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await message.edit("`Error: something bad happened`\n\n"
                                  f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await message.edit("**Dyno Usage:**\n\n"
                              f" -> `Dyno usage for`  **{HEROKU_APP_NAME}**:\n"
                              f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                              f"**|**  [`{AppPercentage}`**%**]"
                              "\n"
                              " -> `Dyno hours quota remaining this month`:\n"
                              f"     •  `{hours}`**h**  `{minutes}`**m**  "
                              f"**|**  [`{percentage}`**%**]"
                              )
