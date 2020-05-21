import asyncio
import io
import os
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from userge import userge, Message, Config
from userge.utils import progress, humanbytes


FF_MPEG_DOWN_LOAD_MEDIA_PATH = "userge.media.ffmpeg"


@userge.on_cmd("ffmpegsave", about={'header': "Save a media that is to be used in ffmpeg"})
async def ff_mpeg_trim_cmd(message: Message):
    ffm_path = "/app/downloads/" + FF_MPEG_DOWN_LOAD_MEDIA_PATH
    if not os.path.exists(ffm_path):
        if not os.path.isdir(Config.DOWN_PATH):
            os.makedirs(Config.DOWN_PATH)
        if message.reply_to_message.media:
            start = datetime.now()
            c_time = time.time()
            reply_message = message.reply_to_message
            try:
                c_time = time.time()
                downloaded_file_name = await userge.download_media(
                    message=reply_message,
                    file_name=FF_MPEG_DOWN_LOAD_MEDIA_PATH,
                    progress=progress,
                    progress_args=(
                        "trying to download", userge, message, c_time
                    )
                )
            except Exception as e:  # pylint:disable=C0103,W0703
                await event.edit(str(e))
            else:
                end = datetime.now()
                ms = (end - start).seconds
                await message.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        else:
            await message.edit("Reply to a Telegram media file")
    else:
        await message.edit(f"a media file already exists in path. Please remove the media and try again!\n`.exec rm {FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")


@userge.on_cmd("ffmpegtrim", about={
    'header': "Trim a given media",
    'usage': "{tr}ffmpegtrim [start time] [end time]})
async def ff_mpeg_trim_cmd(message: Message):
    ffm_path = "/app/downloads/" + FF_MPEG_DOWN_LOAD_MEDIA_PATH
    if not os.path.exists(ffm_path):
        await message.edit(f"a media file needs to be downloaded, and saved to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")
        return
    current_message_text = message.input_str
    cmt = current_message_text.split(" ")
    start = datetime.now()
    if len(cmt) == 3:
        # output should be video
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            ffm_path,
            #FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.DOWN_PATH,
            start_time,
            end_time
        )
        try:
            c_time = time.time()
            await userge.send_video(
                chat_id=message.chat.id,
                video=o,
                caption=" ".join(cmt[1:])
            )
            os.remove(o)
        except Exception as e:
            await message.edit(str(e))
    elif len(cmt) == 2:
        # output should be image
        cmd, start_time = cmt
        o = await take_screen_shot(
            ffm_path,
            #FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.DOWN_PATH,
            start_time
        )

        try:
            c_time = time.time()
            await userge.send_photo(
                chat_id=event.chat_id,
                photo=o,
                caption=" ".join(cmt[1:])
            )
            os.remove(o)
        except Exception as e:
            await message.edit(str(e))
    else:
        await event.edit("RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await message.edit(f"Completed Process in {ms} seconds")


async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26

async def cult_small_video(video_file, output_directory, start_time, end_time):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(round(time.time())) + ".mp4"
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:

        return None
