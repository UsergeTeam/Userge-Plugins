import os
import time
import asyncio
from datetime import datetime

from userge import userge, Message, Config
from userge.utils import progress

FF_MPEG_DOWN_LOAD_MEDIA_PATH = "/app/downloads/userge.media.ffmpeg"


@userge.on_cmd("ffmpegsave", about={'header': "Save a media that is to be used in ffmpeg"})
async def ffmpegsave(message: Message):
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        if not os.path.isdir(Config.DOWN_PATH):
            os.makedirs(Config.DOWN_PATH)
        if message.reply_to_message.media:
            start = datetime.now()
            reply_message = message.reply_to_message
            try:
                downloaded_file_name = await message.client.download_media(
                    message=reply_message,
                    file_name=FF_MPEG_DOWN_LOAD_MEDIA_PATH,
                    progress=progress,
                    progress_args=(message, "trying to download")
                )
            except Exception as e:  # pylint:disable=C0103,W0703
                await message.edit(str(e))
            else:
                end = datetime.now()
                ms = (end - start).seconds
                await message.edit(
                    "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        else:
            await message.edit("Reply to a Telegram media file")
    else:
        await message.edit(
            "a media file already exists in path. "
            f"Please remove the media and try again!\n`.term rm {FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")


@userge.on_cmd("ffmpegtrim", about={
    'header': "Trim a given media",
    'usage': "{tr}ffmpegtrim [start time] [end time]"})
async def ffmpegtrim(message: Message):
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await message.edit(
            "a media file needs to be downloaded, and saved to the "
            f"following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")
        return
    current_message_text = message.text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    if len(cmt) == 3:
        # output should be video
        _, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.DOWN_PATH,
            start_time,
            end_time
        )
        try:
            await message.client.send_video(
                chat_id=message.chat.id,
                video=o,
                caption=" ".join(cmt[1:])
            )
            os.remove(o)
        except Exception as e:
            await message.edit(str(e))
    elif len(cmt) == 2:
        # output should be image
        _, start_time = cmt
        o = await take_screen_shot(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.DOWN_PATH,
            start_time
        )

        try:
            await message.client.send_photo(
                chat_id=message.chat.id,
                photo=o,
                caption=" ".join(cmt[1:])
            )
            os.remove(o)
        except Exception as e:
            await message.edit(str(e))
    else:
        await message.edit("RTFM")
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
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
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
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None
