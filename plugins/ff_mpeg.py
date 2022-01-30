import re
import json
import ffmpeg
import asyncio
from typing import Tuple, Optional

from math import floor
from pathlib import Path
from datetime import datetime
from asyncio import create_subprocess_exec, subprocess

from ffmpeg._run import Error, compile as ffmpg_compile
from ffmpeg._utils import convert_kwargs_to_cmd_line_args

from userge import userge, Message
from userge.utils import humanbytes, is_url
from userge.plugins.misc.download import tg_download, url_download

FF_MPEG_DOWN_LOAD_MEDIA_PATH = Path("/app/downloads/userge.media.ffmpeg")

logger = userge.getLogger(__name__)


async def probe(filename, cmd='ffprobe', **kwargs):
    # https://gist.github.com/fedej/7f848d20205efbff4db4a0fc78eae7ba
    args = [cmd, '-show_format', '-show_streams', '-of', 'json']
    args += convert_kwargs_to_cmd_line_args(kwargs)
    args += [filename]

    p = await create_subprocess_exec(*args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    coroutine = p.communicate()
    out, err = await coroutine
    if p.returncode != 0:
        raise Error('ffprobe', out, err)
    return json.loads(out.decode('utf-8'))


async def run(stream_spec, cmd='ffmpeg', pipe_stdin=False, pipe_stdout=False, pipe_stderr=False,
              input_file=None, quiet=True, overwrite_output=True):
    # https://gist.github.com/fedej/7f848d20205efbff4db4a0fc78eae7ba
    args = ffmpg_compile(stream_spec, cmd, overwrite_output=overwrite_output)
    stdin_stream = subprocess.PIPE if pipe_stdin else None
    stdout_stream = subprocess.PIPE if pipe_stdout or quiet else None
    stderr_stream = subprocess.PIPE if pipe_stderr or quiet else None
    p = await create_subprocess_exec(
        *args, stdin=stdin_stream, stdout=stdout_stream, stderr=stderr_stream
    )
    out, err = await p.communicate(input_file)
    if p.returncode != 0:
        raise Error('ffmpeg', out, err)
    return out, err


async def get_media_path_and_name(
    message: Message, input_str = ""
) -> Tuple[Optional[str], Optional[str]]:
    if not input_str:
        input_str = message.filtered_input_str
    dl_loc, file_name = "", ""
    replied = message.reply_to_message
    if hasattr(replied, 'media'):
        dl_loc, _ = await tg_download(message, replied)
        if hasattr(replied.audio, 'file_name'):
            file_name = replied.audio.file_name
        elif hasattr(replied.video, 'file_name'):
            file_name = replied.video.file_name
        elif hasattr(replied.document, 'file_name'):
            file_name = replied.document.file_name
        else:
            file_name = Path(dl_loc).name
    elif input_str:
        if is_url(input_str):
            try:
                dl_loc, _ = await url_download(message, input_str)
                file_name = Path(dl_loc).name
            except Exception as err:
                await message.err(str(err))
                return None, None
    else:
        await message.err("nothing provided for further process")
        return None, None
    if dl_loc:
        file_path = dl_loc
    else:
        file_path = input_str.strip()
        file_name = Path(file_path).name
    if not Path(file_path).exists():
        await message.err("Seems that an invalid file path provided?")
        return None, None
    return file_path, file_name


@userge.on_cmd("x256", about={
    'header': "Encode a file using x256",
    'flags': {'-b': 'Custom bitrate'},
    'usage': "{tr}x256 [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}x256 link', '{tr}x256 path']}, check_downpath=True)
async def encode_x256(message: Message):
    replied = message.reply_to_message
    if not (message.filtered_input_str and hasattr(replied, 'media')):
        return await message.err("please read .help x256")
    custom_bitrate = 28
    if message.flags and '-b' in message.flags:
        custom_bitrate = int(message.flags.get('-b'))
    dl_loc, file_name = await get_media_path_and_name(message)

    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    video_file = f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/x256_{file_name}"
    await message.edit("`Encoding to x256...`")
    start = datetime.now()
    try:
        await run(
            ffmpeg.input(dl_loc).output(
                video_file, vcodec="libx265", crf=custom_bitrate, preset="ultrafast"
            )
        )
    except ffmpeg.Error as e:
        await message.err(f"`{e.stderr}`")
    else:
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")
        caption = (
            f"[{humanbytes(Path(video_file).stat().st_size)}]\n"
            f"{replied.caption if hasattr(replied, 'media') else file_name}"
        )
        message_id = replied.message_id if replied else None
        await asyncio.gather(
            message.delete(),
            message.client.send_video(
                chat_id=message.chat.id, reply_to_message_id=message_id,
                video=video_file, caption=caption
            )
        )
    finally:
        Path(video_file).unlink(missing_ok=True)
        Path(f"downloads/{file_name}").unlink(missing_ok=True)


@userge.on_cmd("v2a", about={
    'header': "Convert a video to audio",
    'flags': {'-b': 'Custom bitrate'},
    'usage': "{tr}v2a [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}v2a link', '{tr}v2a path']}, check_downpath=True)
async def video_to_audio(message: Message):
    replied = message.reply_to_message
    if not (message.filtered_input_str and hasattr(replied, 'media')):
        return await message.err("please read .help v2a")

    if message.flags and '-b' in message.flags:
        custom_bitrate = message.flags.get('-b', "48000")
    dl_loc, file_name = await get_media_path_and_name(message)

    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    await message.edit("`Extracting audio...`")
    audio_file = f"{file_name.split('.')[0]}.mp3"
    start = datetime.now()

    try:
        await run(
            ffmpeg.input(dl_loc).output(
                f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/{audio_file}",
                format="mp3", audio_bitrate=custom_bitrate
            ).overwrite_output()
        )
    except ffmpeg.Error as e:
        await message.err(f"{e.stderr}")
    else:   
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")

        message_id = replied.message_id if replied else None
        caption = (
            f"[{humanbytes(Path(FF_MPEG_DOWN_LOAD_MEDIA_PATH / audio_file).stat().st_size)}]\n"
            f"{replied.caption if hasattr(replied, 'media') else file_name}"
        )
        await asyncio.gather(
            message.delete(),
            message.client.send_audio(
                chat_id=message.chat.id, reply_to_message_id=message_id,
                audio=f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/{audio_file}",
                caption=caption
            )
        )
    finally:
        Path(f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/{audio_file}").unlink(missing_ok=True)
        Path(f"downloads/{file_name}").unlink(missing_ok=True)


@userge.on_cmd("vscale", about={
    'header': "Scale a video to a given quality using h264",
    'flags': {'-q': 'Video Quality 144/240/360/480/720/etc',
              '-b': 'Custom bitrate',
              '-c': 'Compress using x256'},
    'usage': "{tr}vscale -q quality [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}vscale -q 360 link', '{tr}vscale 360 path']}, check_downpath=True)
async def scale_video(message: Message):
    replied = message.reply_to_message
    if not (message.filtered_input_str and hasattr(replied, 'media')):
        return await message.err("please read .help vscale")
    flags = message.flags
    if not '-q' in flags:
        return await message.err("You muse specify a quality!")

    quality = int(flags.get('-q').rstrip('p'))
    custom_bitrate = flags.get('-b', "28")
    encoder = "libx265" if "-c" in flags else "h264"

    dl_loc, file_name = await get_media_path_and_name(message)

    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    await message.edit("`Scaling the video...`")
    video_file = f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/{quality}_{file_name}"
    start = datetime.now()
    try:
        await run(
            ffmpeg.input(dl_loc).filter(
                "scale", -1, quality).output(
                video_file, vcodec=encoder, crf=custom_bitrate, preset="ultrafast"
            )
        )
    except ffmpeg.Error as e:
        await message.err(f"{e.stderr}")
    else:
        message_id = replied.message_id if replied else None
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")
        caption = (
            f"[{humanbytes(Path(video_file).stat().st_size)}]\n"
            f"{replied.caption if hasattr(replied, 'media') else file_name}"
        )
        await asyncio.gather(
            message.delete(),
                message.client.send_video(
                chat_id=message.chat.id, reply_to_message_id=message_id,
                video=video_file, caption=caption
            )
        )
    finally:
        Path(video_file).unlink(missing_ok=True)
        Path(f"downloads/{file_name}").unlink(missing_ok=True)


@userge.on_cmd("vth", about={
    'header': "Get video thumbnail",
    'usage': "{tr}vth [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}vth link', '{tr}vth path']}, check_downpath=True)
async def video_thumbnail(message: Message):
    replied = message.reply_to_message
    if not (message.filtered_input_str and hasattr(replied, 'media')):
        return await message.err("please read .help vth")
    dl_loc, file_name = await get_media_path_and_name(message, message.input_str)

    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    await message.edit("`Extracting video thumbnail...`")
    thumbnail_file = f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/{file_name.split('.')[0]}.png"
    start = datetime.now()
    try:
        await run(
            ffmpeg.input(dl_loc, ss="00:01:00").filter('scale', 720, -1).output(
                thumbnail_file, vframes=1
            )
        )
    except ffmpeg.Error as e:
        await message.err(f"{e.stderr}")
    else:
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")
        message_id = replied.message_id if replied else None
        await asyncio.gather(
            message.delete(),
            message.client.send_photo(
                chat_id=message.chat.id,
                reply_to_message_id=message_id,
                photo=thumbnail_file,
                caption=replied.caption if hasattr(replied, 'media') else file_name
            )
        )
    finally:
        Path(thumbnail_file).unlink(missing_ok=True)
        Path(f"downloads/{file_name}").unlink(missing_ok=True)


@userge.on_cmd("vtrim", about={
    'header': "Trim a video",
    'usage': "{tr}vtrim [duration] | [file / folder path | direct link | reply to telegram file]",
    'examples': [
        '{tr}vtrim 00:00:00 00:01:00 | link',
        '{tr}vtrim 00:10:00 00:20:00 | path'
    ]}, check_downpath=True)
@userge.on_cmd("atrim", about={
    'header': "Trim an audio track",
    'usage': "{tr}atrim [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}atrim link', '{tr}atrim path']}, check_downpath=True)
async def video_trim(message: Message):
    replied = message.reply_to_message
    if not (message.input_str and hasattr(replied, 'media')):
        return await message.err("please read .help vtrim/atrim")
    if '|' not in message.input_str:
        return await message.err("path not specified!")
    match = re.search(
        r'(\d{2}:\d{2}:\d{2})? ?(\d{2}:\d{2}:\d{2})?',
        message.input_str.split('|', 1)[0]
    )
    if not (match and match.group(1) and match.group(2)):
        return await message.err("You muse specify end time at least!")

    dl_loc, file_name = await get_media_path_and_name(
        message,
        input_str=message.input_str.split('|', 1)[1]
    )

    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    await message.edit("`Trimming media...`")
    end_time = match.group(1) if not match.group(2) else match.group(2)
    start_time = match.group(1) if match.group(1) and match.group(1) != end_time else "00:00:00"
    video_file = f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/trimmed_{file_name}"
    start = datetime.now()
    try:
        await run(ffmpeg.input(dl_loc, ss=start_time, to=end_time).output(video_file))
    except ffmpeg.Error as e:
        await message.err(f"{e.stderr}")
    else:
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")
        message_id = replied.message_id if replied else None
        caption = (
            f"[{humanbytes(Path(video_file).stat().st_size)}]\n"
            f"{replied.caption if hasattr(replied, 'media') else file_name}"
        )
        await asyncio.gather(
            message.delete(),
            message.client.send_video(
                chat_id=message.chat.id, reply_to_message_id=message_id,
                video=video_file, caption=caption
            )
        )
    finally:
        Path(f"downloads/{file_name}").unlink(missing_ok=True)
        Path(video_file).unlink(missing_ok=True)


@userge.on_cmd("vcompress", about={
    'header': "Compress a video file",
    'usage': "{tr}vcompress percentage [file / folder | direct link | reply to telegram file]",
    'examples': ['{tr}vcompress 70 link', '{tr}vcompress 50 path']}, check_downpath=True)
async def video_compress(message: Message):
    replied = message.reply_to_message
    if not (message.input_str and hasattr(replied, 'media')):
        return await message.edit("`Please read .help vcompress`")

    if ' ' not in message.input_str:
        return await message.err("path not specified!")

    percentage, input_str = message.input_str.split(' ', 1)
    dl_loc, file_name = await get_media_path_and_name(message, input_str=input_str)

    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    await message.edit("`Compressing media...`")
    # https://github.com/kkroening/ffmpeg-python/issues/545
    info = await probe(dl_loc)
    total_time = floor(float(info['streams'][0]['duration']))
    target_percentage = int(percentage)
    filesize = Path(dl_loc).stat().st_size
    # https://github.com/AbirHasan2005/VideoCompress/blob/main/bot/helper_funcs/ffmpeg.py#L60
    calculated_percentage = 100 - target_percentage
    target_size = (calculated_percentage / 100) * filesize
    target_bitrate = int(floor(target_size * 8 / total_time))
    if target_bitrate // 1000000 >= 1:
        bitrate = str(target_bitrate // 1000000) + "M"
    else:
        bitrate = str(target_bitrate // 1000) + "k"
    video_file = f"{FF_MPEG_DOWN_LOAD_MEDIA_PATH}/compressed_{file_name}"
    start = datetime.now()
    try:
        await run(ffmpeg.input(dl_loc).output(
            video_file, video_bitrate=bitrate, bufsize=bitrate, vcodec="h264", preset="ultrafast"))
    except ffmpeg.Error as e:
        await message.err(f"{e.stderr}")
    else:
        message_id = replied.message_id if replied else None
        caption = (
            f"[{humanbytes(Path(video_file).stat().st_size)}]\n"
            f"{replied.caption if hasattr(replied, 'media') else file_name}"
        )
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")
        await asyncio.gather(
            message.delete(),
            message.client.send_video(
                chat_id=message.chat.id,
                reply_to_message_id=message_id,
                video=video_file, caption=caption
            )
        )
    finally:
        Path(video_file).unlink(missing_ok=True)
        Path(f"downloads/{file_name}").unlink(missing_ok=True)


@userge.on_cmd("minfo", about={
    'header': "Get media info",
    'flags': {'-d': 'Delete media after getting info'},
    'usage': "{tr}minfo [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}minfo link', '{tr}minfo path']}, check_downpath=True)
async def media_info(message: Message):
    replied = message.reply_to_message
    if not (message.filtered_input_str and hasattr(replied, 'media')):
        return await message.err("`please read .help minfo`")
        
    dl_loc, file_name = await get_media_path_and_name(message)
    if not (dl_loc or file_name):
        return

    FF_MPEG_DOWN_LOAD_MEDIA_PATH.mkdir(parents=True, exist_ok=True)
    await message.edit("`Extracting media info...`")
    start = datetime.now()

    try:
        info = await probe(dl_loc)
        await message.reply(f"`{json.dumps(info, indent=1, ensure_ascii=False)}`")
    except ffmpeg.Error as e:
        await message.err(f"`{e.stderr}`")
    else:
        await message.edit(f"`Done in in {(datetime.now() - start).seconds} seconds!`")
    finally:
        if '-d' in message.flags:
            Path(f"downloads/{file_name}").unlink(missing_ok=True)
