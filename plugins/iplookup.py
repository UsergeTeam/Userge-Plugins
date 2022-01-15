# (c) @AbirHasan2005 | @Jigarvarma2005
# A IP Address Lookup Plugin!
# Modded from @AHToolsBot by @Discovery_Updates

import aiohttp
from userge import userge, Message


@userge.on_cmd(
    "iplook", about={
        'header': "A IPLookUp Plugin",
        'description': "Put IP Address to get some details about that.",
        'usage': "{tr}iplook [IP Address]",
        'example': "{tr}iplook 23.1.1.15"})
async def _ip_look_up(message: Message):
    await message.edit("`Checking IP Address ...`")
    if not message.input_str:
        await message.edit("`No IP Address Found!`")
        return
    url = f"https://ipapi.co/{message.input_str}/json"
    async with aiohttp.ClientSession() as requests:
        data = await requests.get(url)
        values = await data.json()
    is_error = values.get('error', False)
    if is_error:
        await message.edit("`Provided IP Address invalid!`")
        return
    org = values['org']
    tip = values['version']
    country = values['country_name']
    region = values['region']
    city = values['city']
    localisation = f"{values['latitude']}, {values['longitude']}"
    gmap_lock = f"https://www.google.fr/maps?q={localisation}".replace(" ", "")
    postal = values["postal"]
    timezone = values["timezone"]
    currency = values["currency_name"]
    asn = values["asn"]
    population = values["population"]
    if timezone:
        try:
            continent = timezone.split("/",1)[0]
        except:
            continent = values["continent_code"]

    await message.edit(
        text=(f"Here details of `{message.input_str}`\n\n"
              f"**Organisation:** `{org}`\n"
              f"**asn**: `{asn}`\n"
              f"**IP Type:** `{tip}`\n"
              f"**City:** `{city}`\n"
              f"**Region:** `{region}`\n"
              f"**Country:** `{country}`\n"
              f"**Postal Code:** `{postal}`\n"
              f"**population:** `{population}`\n"
              f"**Continent:** `{continent}`\n"
              f"**Time Zone:** `{timezone}`\n"
              f"**Currency:** `{currency}`\n"
              f"**Location:** `{localisation}`\n"
              f"**Google Map:** {gmap_lock}"),
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )
