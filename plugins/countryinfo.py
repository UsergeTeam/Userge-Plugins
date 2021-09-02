from userge import userge, Message

@userge.on_cmd("country", about={
    'header': "Country Info",
    'usage': "{tr} get information of a country"})
async def attach(update: Message):
    country = await update.text.split(" ", 1)[1]
