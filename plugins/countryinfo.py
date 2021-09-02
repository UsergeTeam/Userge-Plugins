# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from countryinfo import CountryInfo
from userge import userge, Message


PREVIEW = False  # False for instant view


@userge.on_cmd("country", about={
    'header': "Country Info",
    'usage': "{tr} get information of a country"})
async def countryinfo(update: Message):
    if " " not in update.text:
        await update.edit_text("Send with country name")
        return
    country = CountryInfo(update.text.split(" ", 1)[1])
    info = f"""**Country Information**

Name : `{country.name()}`
Native Name : `{country.native_name()}`
Capital : `{country.capital()}`
Population : `{country.population()}`
Region : `{country.region()}`
Sub Region : `{country.subregion()}`
Top Level Domains : `{country.tld()}`
Calling Codes : `{country.calling_codes()}`
Currencies : `{country.currencies()}`
Residence : `{country.demonym()}`
Timezone : `{country.timezones()}`
Wiki : {country.wiki()}"""
    try:
        await update.edit_text(text=info, disable_web_page_preview=PREVIEW)
    except Exception as error:
        await update.edit_text(text=error, disable_web_page_preview=True)
