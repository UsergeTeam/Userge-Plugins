import os
import time
from datetime import datetime

from userge import userge, Config, Message

from userge.utils import progress

PHOTO = Config.DOWN_PATH + "profile_pic.jpg"


@userge.on_cmd('setpfp', about={
    'header': "Set profile picture",
    'usage': "{tr}setpfp [reply to any photo]"})
async def set_profile_picture(message: Message):
    """ Set Profile Picture """
    await message.edit("```processing ...```")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        s_time = datetime.now()
        c_time = time.time()

        await userge.download_media(message=replied,
                                    file_name=PHOTO,
                                    progress=progress,
                                    progress_args=(
                                        "trying to download and set profile picture",
                                        userge, message, c_time))

        await userge.set_profile_photo(PHOTO)

        if os.path.exists(PHOTO):
            os.remove(PHOTO)

        e_time = datetime.now()
        t_time = (e_time - s_time).seconds

        await message.edit(
            "<code>Profile picture set in {} seconds.</code>".format(t_time), parse_mode='html', del_in=5)
    else:
        await message.edit("```Reply to any photo to set profile pic```", del_in=5)


@userge.on_cmd('vpfp', about={
    'header': "View current profile picture",
    'usage': "{tr}vpfp\n{tr}vpfp [reply to any user]"})
async def view_profile_picture(message: Message):
    """ View Profile Picture """
    await message.edit("```checking pfp ...```", del_in=3)

    replied = message.reply_to_message
    if replied:
        user = await userge.get_users(replied.from_user.id)
    else:
        user = await userge.get_me()

    if not user.photo:
        await message.err("profile photo not found!")
        return

    await userge.download_media(user.photo.big_file_id, file_name=PHOTO)

    await userge.send_photo(message.chat.id, PHOTO)

    if os.path.exists(PHOTO):
        os.remove(PHOTO)
