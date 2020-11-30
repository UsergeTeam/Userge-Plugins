# By @Krishna_Singhal

from pyrogram.errors import YouBlockedUser

from userge import userge, Message


@userge.on_cmd("meme", about={
    'header': "Write text on any media. (๑¯ω¯๑)",
    'description': "Top and bottom text are separated by ; ",
    'usage': "{tr}meme [text on top] ; [text on bottom] as a reply."}, allow_via_bot=False)
async def meme_(message: Message):
    """ meme for media """
    replied = message.reply_to_message
    if not (replied and message.input_str):
        await message.err("`Nibba, reply to Media and Give some input...`")
        return
    if not (replied.photo or replied.sticker or replied.video or replied.animation):
        await message.err("`reply to only media...`")
        return
    await message.edit("`memifying...`")
    chat = "@MemeAuto_bot"
    async with userge.conversation(chat) as conv:
        try:
            args = message.input_str
            await conv.send_message("/start")
            await conv.get_response(mark_read=True)
        except YouBlockedUser:
            await message.err(
                "`This cmd not for you, If you want to use, Unblock` **@MemeAutobot**"
            )
            return
        await conv.send_message(args)
        response = await conv.get_response(mark_read=True)
        if not "Okay..." in response.text:
            await message.edit("`Bot is down, Try again Later...`")
            return
        await conv.forward_message(replied)
        response = await conv.get_response(mark_read=True)
        if response.sticker:
            await response.forward(message.chat.id, as_copy=True)
        await message.delete()
