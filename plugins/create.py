# don't use this code in your repo without permission
# https://github.com/UsergeTeam/Userge

from userge import userge, Message


@userge.on_cmd(
    "channel",
    about={
        'header': "Creates a channel",
        'usage': "{tr}channel TheUserge | Hello"
    },
    allow_channels=False,
    allow_bots=False
)
async def create_channel(message: Message):
    try:
        args = message.input_str
        if not args:
            return await message.err("title not found!")

        if '|' in args:
            title, des = args.split('|', maxsplit=1)
        else:
            title, des = args, "This channel is created using @TheUserge"
        if len(des) > 256:
            des = des.strip()[:253] + "..."
        await userge.create_channel(title.strip(), des.strip())
        await message.edit(f"Successfully made a new channel **{title.strip()}**")
    except Exception as e:
        await message.err(str(e))
