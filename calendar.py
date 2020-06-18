import calendar

from userge import userge, Message

@userge.on_cmd("calendar", about={
    'header': "Print calendar of any month of any year.",
    'usage': "{tr}calendar [ year | month]",
    'examples': "{tr}calendar 2020 | 6"})
async def calendar_(message: Message):

    if not message.input_str:
        await message.err(
            "I don't found any input text"
            "For more help do .help .calendar")
        return
    if '|' not in message.input_str:
        await message.err("both year and month required!")
        return
    await message.edit("`Searching...`")
    year, month = message.input_str.split('|', maxsplit=1)
    try:
        input_ = calendar.month(int(year.strip()), int(month.strip()))
        await message.edit(f"```{input_}```")
    except Exception as e:
        await message.err(e)