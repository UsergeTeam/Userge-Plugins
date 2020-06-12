from userge import userge, Message


@userge.on_cmd("delpfp", about={
    'header': "Delete Profile Pics",
    'description': "Delete profile pic in one blow"
                   " [NOTE: May Cause Flood Wait]",
    'usage': "{tr}delpfp [pfp count]"})
async def del_pfp(message: Message):
    if message.input_str:
        try:
            del_c = int(message.input_str)
        except ValueError as e:
            await message.err(text=e)
            return
        await message.edit(f"Deleting first {del_c} Profile Photos")
        async for photo in userge.iter_profile_photos("me", limit=del_c):
            await userge.delete_profile_photos(photo.file_id)
    else:
        await message.edit("What am i supposed to delete nothing")
        await message.reply_sticker(sticker="CAADBQADPwAD7BHsKmSxAAHVc0NMKBYE")
