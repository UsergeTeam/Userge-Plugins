import calendar

from userge import userge, Message


@userge.on_cmd("cal", about={
    'header': "Print calendar of any month of any year.",
    'usage': "{tr}cal [ year | month]",
    'examples': "{tr}cal 2020 | 6"})
async def cal_(message: Message):

    if not message.input_str:
        await message.err(
            "I don't found any input text"
            "For more help do .help .cal")
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
