""" All Profile Settings for User """

# by krishna
# del_pfp by Phyco-Ninja

import os
from datetime import datetime

from pyrogram.errors.exceptions.bad_request_400 import (
    UsernameOccupied, AboutTooLong, UsernameNotOccupied)

from userge import userge, Config, Message
from userge.utils import progress

PHOTO = Config.DOWN_PATH + "profile_pic.jpg"
USER_DATA = {}


@userge.on_cmd("setname", about={
    'header': "Update first, last name and username",
    'flags': {
        '-fname': "update only first name",
        '-lname': "update only last name",
        '-dlname': "delete last name",
        '-uname': "update username",
        '-duname': "delete username"},
    'usage': "{tr}setname [flag] [name]\n"
             "{tr}setname [first name] | [last name]",
    'examples': [
        "{tr}setname -dlname",
        "{tr}setname -fname krishna",
        "{tr}setname -lname singhal",
        "{tr}setname krishna | singhal",
        "{tr}setname -uname username",
        "{tr}setname -duname"]}, allow_via_bot=False)
async def setname_(message: Message):
    """ set or delete profile name and username """
    if not message.input_str:
        await message.edit("```Need Text to Change Profile !```", del_in=3)
        return
    if '-dlname' in message.flags:
        await userge.update_profile(last_name="")
        await message.edit("```Last Name is Successfully Removed ...```", del_in=3)
        return
    if '-duname' in message.flags:
        await userge.update_username(username="")
        await message.edit("```Username is successfully Removed ...```", del_in=3)
        return
    arg = message.filtered_input_str
    if not arg:
        await message.edit("```Need Text to Change Profile  ...```", del_in=3)
        return
    if '-fname' in message.flags:
        await userge.update_profile(first_name=arg.strip())
        await message.edit("```First Name is Successfully Updated ...```", del_in=3)
    elif '-lname' in message.flags:
        await userge.update_profile(last_name=arg.strip())
        await message.edit("```Last Name is Successfully Updated ...```", del_in=3)
    elif '-uname' in message.flags:
        try:
            await userge.update_username(username=arg.strip())
        except UsernameOccupied:
            await message.edit("```Username is Not Available !```", del_in=3)
        else:
            await message.edit("```Username is Successfully Updated ...```", del_in=3)
    elif '|' in message.input_str:
        fname, lname = message.input_str.split('|', maxsplit=1)
        if not lname:
            await message.edit("```Need Last Name to Update Profile !```", del_in=3)
            return
        await userge.update_profile(first_name=fname.strip(), last_name=lname.strip())
        await message.edit("```My Profile Name is Successfully Updated ...```", del_in=3)
    else:
        await message.edit("```Invalid Args, Exiting ...```", del_in=3)


@userge.on_cmd("bio", about={
    'header': "Update bio, Maximum limit 70 characters",
    'flags': {
        '-delbio': "delete bio"},
    'usage': "{tr}bio [flag] \n"
             "{tr}bio [Bio]",
    'examples': [
        "{tr}bio -delbio",
        "{tr}bio  My name is krishna :-)"]}, allow_via_bot=False)
async def bio_(message: Message):
    """ Set or delete profile bio """
    if not message.input_str:
        await message.edit("```Need Text to Change Bio !```", del_in=3)
        return
    if '-delbio' in message.flags:
        await userge.update_profile(bio="")
        await message.edit("```Bio is Successfully Deleted ...```", del_in=3)
        return
    if message.input_str:
        try:
            await userge.update_profile(bio=message.input_str)
        except AboutTooLong:
            await message.edit("```Bio is More then 70 characters !...```", del_in=3)
        else:
            await message.edit("```My Profile Bio is Successfully Updated ...```", del_in=3)


@userge.on_cmd('setpfp', about={
    'header': "Set profile picture",
    'usage': "{tr}setpfp [reply to any photo]"}, allow_via_bot=False)
async def set_profile_picture(message: Message):
    """ Set Profile Picture """
    await message.edit("```processing ...```")
    replied = message.reply_to_message
    if (replied and replied.media and (
            replied.photo or (replied.document and "image" in replied.document.mime_type))):
        s_time = datetime.now()

        await userge.download_media(message=replied,
                                    file_name=PHOTO,
                                    progress=progress,
                                    progress_args=(
                                        message, "trying to download and set profile picture"))

        await userge.set_profile_photo(photo=PHOTO)

        if os.path.exists(PHOTO):
            os.remove(PHOTO)

        e_time = datetime.now()
        t_time = (e_time - s_time).seconds

        await message.edit(
            "<code>Profile picture set in {} seconds.</code>".format(t_time), parse_mode='html')
    else:
        await message.edit("```Reply to any photo to set profile pic```", del_in=5)


@userge.on_cmd('vpf', about={
    'header': "View Profile of any user",
    'flags': {
        '-fname': "Print only first name",
        '-lname': "Print only last name",
        '-flname': "Print full name",
        '-bio': "Print bio",
        '-uname': "Print username",
        '-pp': "Upload profile picture"},
    'usage': "{tr}vpf [flags]\n{tr}vpf [flags] [reply to any user]",
    'note': "<b> -> Use 'me' after flags to print own profile</b>\n"
            "<code>{tr}vpf [flags] me</code>"})
async def view_profile(message: Message):
    """ View Profile  """

    if not message.input_or_reply_str:
        await message.err("```User id / Username not found ! ...```", del_in=3)
        return
    if message.reply_to_message:
        input_ = message.reply_to_message.from_user.id
    else:
        input_ = message.filtered_input_str
    if not input_:
        await message.err("```User id / Username not found ! ...```", del_in=3)
        return
    if not message.flags:
        await message.err("```Flags Required```")
        return
    if "me" in message.filtered_input_str:
        user = await message.client.get_me()
        bio = await message.client.get_chat("me")
    else:
        user = await message.client.get_users(input_)
        bio = await message.client.get_chat(input_)
    if '-fname' in message.flags:
        await message.edit("```checking, wait plox !...```", del_in=3)
        first_name = user.first_name
        await message.edit("<code>{}</code>".format(first_name), parse_mode='html')
    elif '-lname' in message.flags:
        if not user.last_name:
            await message.err("```User not hab last name !...```", del_in=3)
        else:
            await message.edit("```checking, wait plox !...```", del_in=3)
            last_name = user.last_name
            await message.edit("<code>{}</code>".format(last_name), parse_mode='html')
    elif '-flname' in message.flags:
        await message.edit("```checking, wait plox !...```", del_in=3)
        if not user.last_name:
            await message.edit("<code>{}</code>".format(user.first_name), parse_mode='html')
        else:
            full_name = user.first_name + " " + user.last_name
            await message.edit("<code>{}</code>".format(full_name), parse_mode='html')
    elif '-bio' in message.flags:
        if not bio.description:
            await message.err("```User not hab bio !...```", del_in=3)
        else:
            await message.edit("```checking, wait plox !...```", del_in=3)
            about = bio.description
            await message.edit("<code>{}</code>".format(about), parse_mode='html')
    elif '-uname' in message.flags:
        if not user.username:
            await message.err("```User not hab username !...```", del_in=3)
        else:
            await message.edit("```checking, wait plox !...```", del_in=3)
            username = user.username
            await message.edit("<code>{}</code>".format(username), parse_mode='html')
    elif '-pp' in message.flags:
        if not user.photo:
            await message.err("```profile photo not found!```", del_in=3)
        else:
            await message.edit("```checking pfp, wait plox !...```", del_in=3)
            await message.client.download_media(user.photo.big_file_id, file_name=PHOTO)
            await message.client.send_photo(message.chat.id, PHOTO)
            if os.path.exists(PHOTO):
                os.remove(PHOTO)


@userge.on_cmd("delpfp", about={
    'header': "Delete Profile Pics",
    'description': "Delete profile pic in one blow"
                   " [NOTE: May Cause Flood Wait]",
    'usage': "{tr}delpfp [pfp count]"}, allow_via_bot=False)
async def del_pfp(message: Message):
    """ delete profile pics """
    if message.input_str:
        try:
            del_c = int(message.input_str)
        except ValueError as v_e:
            await message.err(v_e)
            return
        await message.edit(f"```Deleting first {del_c} Profile Photos ...```")
        start = datetime.now()
        ctr = 0
        async for photo in userge.iter_profile_photos("me", limit=del_c):
            await userge.delete_profile_photos(photo.file_id)
            ctr += 1
        end = datetime.now()
        difff = (end - start).seconds
        await message.edit(f"Deleted {ctr} Profile Pics in {difff} seconds!")
    else:
        await message.edit("```What am i supposed to delete nothing !...```")
        await message.reply_sticker(sticker="CAADAQAD0wAD976IR_CYoqvCwXhyFgQ")


@userge.on_cmd("clone", about={
    'header': "Clone first name, last name, bio and profile picture of any user",
    'flags': {
        '-fname': "Clone only first name",
        '-lname': "Clone only last name",
        '-bio': "Clone only bio",
        '-pp': "Clone only profile picture"},
    'usage': "{tr}clone [flag] [username | reply to any user]\n"
             "{tr}clone [username | reply to any user]",
    'examples': [
        "{tr}clone -fname username", "{tr}clone -lname username",
        "{tr}clone -pp username", "{tr}clone -bio username",
        "{tr}clone username"],
    'note': "<code>● Use revert after clone to get original profile</code>\n"
            "<code>● Don't use @ while giving username</code>"}, allow_via_bot=False)
async def clone_(message: Message):
    """ Clone first name, last name, bio and profile picture """
    if not message.input_or_reply_str:
        await message.err("```User id / Username not found ! ...```", del_in=3)
        return

    if message.reply_to_message:
        input_ = message.reply_to_message.from_user.id
    else:
        input_ = message.filtered_input_str

    if not input_:
        await message.err("```User id / Username not found ! ...```", del_in=3)
        return

    await message.edit("`clonning...`")

    try:
        chat = await userge.get_chat(input_)
        user = await userge.get_users(input_)
    except UsernameNotOccupied:
        await message.err("```Username not exist !...```", del_in=5)
        return
    me = await userge.get_me()

    if '-fname' in message.flags:
        if 'first_name' in USER_DATA:
            await message.err("```First Revert ! ...```", del_in=3)
            return
        USER_DATA['first_name'] = me.first_name or ''
        await userge.update_profile(first_name=user.first_name or '')
        await message.edit("```First Name is Successfully cloned ...```", del_in=3)
    elif '-lname' in message.flags:
        if 'last_name' in USER_DATA:
            await message.err("```First Revert ! ...```", del_in=3)
            return
        USER_DATA['last_name'] = me.last_name or ''
        await userge.update_profile(last_name=user.last_name or '')
        await message.edit("```Last name is successfully cloned ...```", del_in=3)
    elif '-bio' in message.flags:
        if 'bio' in USER_DATA:
            await message.err("```First Revert ! ...```", del_in=3)
            return
        mychat = await userge.get_chat(me.id)
        USER_DATA['bio'] = mychat.description or ''
        await userge.update_profile(bio=chat.description or '')
        await message.edit("```Bio is Successfully Cloned ...```", del_in=3)
    elif '-pp' in message.flags:
        if os.path.exists(PHOTO):
            await message.err("```First Revert ! ...```", del_in=3)
            return
        if not user.photo:
            await message.err("```User not have any profile pic ...```", del_in=5)
            return
        await userge.download_media(user.photo.big_file_id, file_name=PHOTO)
        await userge.set_profile_photo(photo=PHOTO)
        await message.edit("```Profile photo is Successfully Cloned ...```", del_in=3)
    else:
        if USER_DATA or os.path.exists(PHOTO):
            await message.err("```First Revert ! ...```", del_in=3)
            return
        mychat = await userge.get_chat(me.id)
        USER_DATA.update({
            'first_name': me.first_name or '',
            'last_name': me.last_name or '',
            'bio': mychat.description or ''})
        await userge.update_profile(
            first_name=user.first_name or '',
            last_name=user.last_name or '',
            bio=chat.description or '')
        if not user.photo:
            await message.edit(
                "`User not have profile photo, I only cloning Name and bio ...`", del_in=5)
            return
        await userge.download_media(user.photo.big_file_id, file_name=PHOTO)
        await userge.set_profile_photo(photo=PHOTO)
        await message.edit("```Profile is Successfully Cloned ...```", del_in=3)


@userge.on_cmd("revert", about={
    'header': "Returns original profile",
    'usage': "{tr}revert"}, allow_via_bot=False)
async def revert_(message: Message):
    """ Returns Original Profile """
    if not (USER_DATA or os.path.exists(PHOTO)):
        await message.err("```Already Reverted ! ...```", del_in=3)
        return
    if USER_DATA:
        await userge.update_profile(**USER_DATA)
        USER_DATA.clear()
    if os.path.exists(PHOTO):
        me = await userge.get_me()
        photo = (await userge.get_profile_photos(me.id, limit=1))[0]
        await userge.delete_profile_photos(photo.file_id)
        os.remove(PHOTO)
    await message.edit("```Profile is Successfully Reverted ...```", del_in=3)
