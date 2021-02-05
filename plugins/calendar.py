import calendar  # pylint: disable=W0406
from datetime import datetime

from userge import userge, Message


@userge.on_cmd("cal", about={
    'header': "Print calendar of any month of any year.",
    'usage': "{tr}cal\n{tr}cal [ year | month]",
    'examples': "{tr}cal 2020 | 6"})
async def cal_(message: Message):

    if not message.input_str:
        await message.edit("`Searching...`")
        try:
            today = datetime.today()
            input_ = calendar.month(today.year, today.month)
            await message.edit(f"```{input_}```")
        except Exception as e:
            await message.err(e)
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
