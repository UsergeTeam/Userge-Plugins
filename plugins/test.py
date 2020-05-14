from userge import userge


@userge.on_cmd("test$", about={'header': "haha"})
async def hack_func(message):
    await message.edit("test complete")