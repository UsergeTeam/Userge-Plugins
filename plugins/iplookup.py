# (c) @AbirHasan2005
# A IP Address Lookup Plugin!
# Modded from @AHToolsBot by @Discovery_Updates

import aiohttp

from userge import userge, Message


@userge.on_cmd(
    "iplook", about={
        'header': "A IPLookUp Plugin",
        'description': "Put IP Address to get some details about that.",
        'usage': "{tr}iplook [IP Address]"})
async def _ip_look_up(message: Message):
    await message.edit("`Checking IP Address ...`")
    if not message.input_str:
        await message.edit("`No IP Address Found!`")
        return
    url = f"https://extreme-ip-lookup.com/json/{message.input_str}"
    async with aiohttp.ClientSession() as requests:
        data = await requests.get(url)
        values = await data.json()
    status = values['status']
    if status != "success":
        await message.edit("`Provided IP Address invalid!`")
        return
    host = values['ipName']
    isp = values['isp']
    org = values['org']
    continent = values['continent']
    tip = values['ipType']
    country = values['country']
    region = values['region']
    city = values['city']
    localisation = f"{values['lat']}, {values['lon']}"
    gmap_lock = f"https://www.google.fr/maps?q={localisation}".replace(" ", "")

    await message.edit(
        text=(f"Here details of `{message.input_str}`\n\n"
              f"**Host:** `{host}`\n"
              f"**ISP:** `{isp}`\n"
              f"**Organisation:** `{org}`\n"
              f"**Region:** `{region}, {country}`\n"
              f"**Continent:** `{continent}`\n"
              f"**IP Type:** `{tip}`\n"
              f"**City:** `{city}`\n"
              f"**Location:** `{localisation}`\n"
              f"**Google Map:** {gmap_lock}"),
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )
