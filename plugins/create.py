# don't use this code in your repo without permission
# https://github.com/UsergeTeam/Userge

from userge import userge, Message


@userge.on_cmd(
    "channel",
    about="Creates a channel",
    allow_channels=False,
    allow_bots=False
)
async def create_channel(message: Message):
    try:
        args = message.input_str
        if not args:
            return await message.err("title not found!")
        await userge.create_channel(args, 'nice')
        await message.edit(f"Successfully made a new channel **{args}**")
    except Exception as e:
        await message.err(str(e))
