# by Alone

from pyfiglet import Figlet
from userge import userge, Message


@userge.on_cmd("figlet", about={
    'header': "Figlet",
    'description': "Make Fancy Style text using Figlet",
    'usage': "{tr}figlet font_name | [text | reply]",
    'Available Fonts': "To know the font name list run command \n\n"
    "```.term pyfiglet --list_fonts```\n\n"
    "**By the Way Plugin by:**\n\nAlone , @krishna_singhal"})
async def figlet_(message: Message):
    args = message.input_or_reply_str
    if not args:
        await message.edit("**Do You think this is Funny?**\n\n"
        "__Try this Blek Mejik:__\n\n"
        "```.help .figlet```")
        await message.reply_sticker(sticker="CAADBAAD1AIAAnV4kzMWpUTkTJ9JwRYE")
        return
    if "|" in message.input_or_reply_str:
        style, text = message.input_str.split('|')
        custom_fig = Figlet(font=style.strip())
        await message.edit(f"```{custom_fig.renderText(text.strip())}```")
        return
    str_ = ' '.join(args)
    custom_fig = Figlet(font='xsans')
    await message.edit(f"```{custom_fig.renderText(str_)}```")
