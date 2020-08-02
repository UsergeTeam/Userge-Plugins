import os
import random
import asyncio

from hachoir.metadata import extractMetadata as XMan
from hachoir.parser import createParser as CPR

from userge import userge, Message, Config
from userge.utils import take_screen_shot, progress


@userge.on_cmd("genss", about={
    'header': "Screen Shot Generator",
    'description': "Generate Random Screen Shots from any video "
                   " **[NOTE: If no frame count is passed, default"
                   " value for number of ss is 5. ",
    'usage': "{tr}genss [No of SS] (optional) as reply to Video"})
async def ss_gen(message: Message):
    replied = message.reply_to_message
    vid_loc = ''
    ss_c = 5
    await message.edit("Checking you Input?🧐🤔😳")
    if message.input_str:
        if '|' in message.input_str:
            ss_c, vid_loc = message.input_str.split("|")
        elif len(message.input_str.split()) == 1:
            try:
                ss_c = int(message.input_str)
            except ValueError:
                vid_loc = message.input_str
                should_clean = False

    if replied:
        if not replied.video:
            await message.edit("I doubt it is a video")
            return
        await message.edit("Downloading Video to my Local")
        vid = await message.client.download_media(
            message=replied,
            file_name=Config.DOWN_PATH,
            progress=progress,
            progress_args=(message, "Downloading🧐? W8 plox")
        )
        vid_loc = os.path.join(Config.DOWN_PATH, os.path.basename(vid))
        should_clean = True
    await message.edit("Compiling Resources")
    meta = XMan(CPR(vid_loc))
    if meta and meta.has("duration"):
        vid_len = meta.get("duration").seconds
    else:
        await message.edit("Something went wrong, Not able to gather metadata")
        return
    await message.edit("Done, Generating Screen Shots and uploading")
    try:
        for frames in random.sample(range(vid_len), ss_c):
            capture = await take_screen_shot(vid_loc, int(frames), "ss_cap.jpeg")
            await message.client.send_photo(chat_id=message.chat.id, photo=capture)
            os.remove(capture)
        await message.edit("Uploaded")
    except Exception as e:
        await message.edit(e)
    if should_clean:
        os.remove(vid_loc)
    await asyncio.sleep(0.5)
    await message.delete()
