from userge import userge, Message


@userge.on_cmd("delpfp", about={
    'header': "Delete Profile Pics",
    'description': "Delete profile pic in one blow"
                   "For profile pics more that 100 keeps pfp"
                   "counts in multiple of 100 plox. Kekthnx",
    'usage': "{tr}delpfp [pfp count]"})
async def del_pfp(message: Message):
    if message.input_str:
        try:
            del_c = int(message.input_str)
        except ValueError as e:
            await message.err(text=e)
            return
        if del_c <= 100:
            to_del = await userge.get_profile_photos("me", limit=del_c)
            await userge.delete_profile_photos([photo.file_id for photo in to_del])
        elif del_c > 100:
            loop = del_c // 100
            for _ in range(loop):
                to_del = await userge.get_profile_photos("me", limit=100)
                await userge.delete_profile_photos([photo.file_id for photo in to_del])
    else:
        await message.edit("What am i supposed to delete nothing")
        await message.reply_sticker(sticker="CAADBQADPwAD7BHsKmSxAAHVc0NMKBYE")
