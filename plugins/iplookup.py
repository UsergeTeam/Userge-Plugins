# (c) @AbirHasan2005
# A IP Address Lookup Plugin!
# Modded from @AHToolsBot by @Discovery_Updates

import requests
import json
from userge import userge, Message

@userge.on_cmd(
    "iplook", about={
        'header': "A IPLookUp Plugin",
        'description': "Put IP Address to get some details about that.",
        'usage': "{tr}iplook [IP Address]"})

async def IPLookUpTool(message: Message):
    await message.edit("`Checking IP Address ...`", parse_mode="Markdown")
    if not message.input_str:
        await message.edit("`No IP Address Found!`")
        return
    ip_address = message.input_str
    url = "https://extreme-ip-lookup.com/json/"
    data = requests.get(url+ip_address).content.decode('utf-8')
    values = json.loads(data)
    status = values['status']
    if status != "success":
        await message.edit("`Your IP Address Not Valid!`")
        return
    HOST_name = values['ipName']
    ISP_value = values['isp']
    org_value = values['org']
    continent_value = values['continent']
    IP_Type = values['ipType']
    country_value = values['country']
    region_value = values['region']
    city_value = values['city']
    localisation = values['lat']+','+values['lon']
    gmap_lock = "https://www.google.fr/maps?q="+localisation

    await message.edit(
        text=f"Here details of `{ip_address}`\n\n**Host:** `{HOST_name}`\n**ISP:** `{ISP_value}`\n**Organisation:** `{org_value}`\n**Region:** `{region_value}`\n**Continent:** `{continent_value}`\n**IP Type:** `{IP_Type}`\n**City:** `{city_value}`\n**Location:** `{localisation}`\n**Google Map:** {gmap_lock}",
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )
