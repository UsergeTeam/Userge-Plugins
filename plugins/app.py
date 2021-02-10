""" Fetch App Details from Playstore.
.app <app_name> to fetch app details.
"""

# By - @kirito6969

import bs4
import aiohttp
import requests

from userge import userge, Message


@userge.on_cmd("app", about={
    'header': "Search application details of any app in play store.\n"
              "Plugin by - @kirito6969, @Krishna_Singhal",
    'usage': "{tr}app telegram"})
async def app(message: Message):
    try:
        await message.edit("`Searching...`")
        app_name = '+'.join(message.input_str.split(' '))
        page = requests.get(f"https://play.google.com/store/search?q={app_name}&c=apps")
        soup = bs4.BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')
        results = soup.findAll("div", "ZmHEEd")

        app_name = results[0].findNext('div', 'Vpfmgd').findNext('div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext('div', 'Vpfmgd').findNext('div', 'KoLSrc').text
        app_dev_link = "https://play.google.com" + results[0].findNext(
            'div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext('div', 'Vpfmgd').findNext(
            'div', 'pf5lIe'
        ).find('div')['aria-label'].replace("Rated ", "⭐️ ").replace(
            " out of ", "/"
        ).replace(" stars", "", 1).replace(" stars", "⭐️").replace("five", "5")
        app_link = "https://play.google.com" + results[0].findNext(
            'div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext('div', 'Vpfmgd').findNext('div', 'uzcko').img['data-src']

        app_details = f"[📲]({app_icon}) **{app_name}**\n\n"
        app_details += f"`Developer :` [{app_dev}]({app_dev_link})\n"
        app_details += f"`Rating :` {app_rating}\n"
        app_details += f"`Features :` [View in Play Store]({app_link})"
        await message.edit(app_details, disable_web_page_preview=False)
    except IndexError:
        await message.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await message.err(err)


# Android user may need this
# Credits : Telegram-Paperplane & UserindoBot Team
@userge.on_cmd(
    'magisk',
    about={
        'header': "Fetch all magisk release from source.",
        'usage': "{tr}magisk",
    },
)
async def magisk(message: Message):
    """ Scrap all magisk version from source. """
    magisk_dict = {
        'Stable': "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        'Beta': "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
        'Canary': "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/canary.json",
    }
    releases = "**Latest Magisk Releases:**\n\n"
    async with aiohttp.ClientSession() as session:
        for name, release_url in magisk_dict.items():
            async with session.get(release_url) as res:
                data = await res.json(content_type="text/plain")
                if name == "Canary":
                    data['magisk']['link'] = (
                        "https://github.com/topjohnwu/magisk_files/raw/canary/"
                        + data['magisk']['link']
                    )
                    data['app']['link'] = (
                        "https://github.com/topjohnwu/magisk_files/raw/canary/"
                        + data['app']['link']
                    )
                    data['uninstaller']['link'] = (
                        "https://github.com/topjohnwu/magisk_files/raw/canary/"
                        + data['uninstaller']['link']
                    )

                releases += (
                    f"**{name}**:\n"
                    f"°[ ZIP - v{data['magisk']['version']}]({data['magisk']['link']})\n"
                    f"° **[APK v{data['app']['version']}]({data['app']['link']})**\n"
                    f"° **[Uninstaller]({data['uninstaller']['link']})**\n\n"
                )
        await message.edit(releases)
