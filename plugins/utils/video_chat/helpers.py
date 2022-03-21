import os
import time
import shutil
import shlex
import requests
from typing import Optional
from pathlib import Path
from traceback import format_exc

from pyrogram.raw.types import GroupCall
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserBannedInChannel
)

from pytgcalls import StreamType
from pytgcalls.types import (
    AudioVideoPiped,
    AudioPiped,
    VideoParameters
)
from pytgcalls.exceptions import GroupCallNotFound, NotInGroupCallError

from userge import userge, Message, pool
from userge.utils import is_url, time_formatter, progress
from . import (
    call, CQ_MSG, QUEUE, GROUP_CALL_PARTICIPANTS,
    CONTROL_CHAT_IDS, CURRENT_SONG, VC_CLIENT,
    MAX_DURATION, LOG, CHANNEL, Dynamic, Vars
)
from .utils import (
    reply_text, is_yt_url, requester, default_markup,
    get_scheduled_text, get_song_info, get_song,
    get_file_info, get_quality_ratios, get_yt_info,
    get_stream_link, get_duration
)


async def play_music(msg: Message, forceplay: bool):
    """ play music """
    input_str = msg.filtered_input_str or getattr(msg.reply_to_message, 'text', '') or ''
    flags = msg.flags
    is_video = "-v" in flags
    path = Path(input_str)
    quality = flags.get('-q', 80)
    if input_str:
        if is_yt_url(input_str):
            details = await get_song_info(input_str)
            if not details:
                return await reply_text(msg, "**ERROR:** `Max song duration limit reached!`")
            name, duration = details
            if Dynamic.PLAYING and not forceplay:
                msg = await reply_text(msg, get_scheduled_text(name, input_str))
            else:
                msg = await reply_text(msg, f"[{name}]({input_str})")
            flags["duration"] = duration
            setattr(msg, '_flags', flags)
            if forceplay:
                QUEUE.insert(0, msg)
            else:
                QUEUE.append(msg)
        elif is_url(input_str) or (path.exists() and path.is_file()):
            if path.exists():
                if not path.name.endswith(
                    (".mkv", ".mp4", ".webm", ".m4v", ".mp3", ".flac", ".wav", ".m4a")
                ):
                    return await reply_text(msg, "`invalid file path provided to stream!`")
                path_to_media = str(path.absolute())
                filename = path.name
            else:
                try:
                    res = await pool.run_in_thread(
                        requests.get
                    )(input_str, allow_redirects=True, stream=True)
                    headers = dict(res.headers)
                    if (
                        "video" not in headers.get("Content-Type", '')
                        and "audio" not in headers.get("Content-Type", '')
                    ):
                        height, width, has_audio, has_video = await get_file_info(input_str)
                        setattr(
                            msg, 'file_info', (height, width, has_audio, has_video))
                        if not has_audio and not has_video:
                            raise Exception
                    path_to_media = input_str
                    try:
                        filename = headers["Content-Disposition"].split('=', 1)[1].strip('"') or ''
                    except KeyError:
                        filename = None
                    if not filename:
                        if hasattr(msg, 'file_info'):
                            _, _, _, has_video = msg.file_info
                            filename = "Video" if has_video else "Music"
                        else:
                            filename = 'Link'
                except Exception as e:
                    LOG.exception(e)
                    return await reply_text(msg, "`invalid direct link provided to stream!`")
            setattr(msg, 'path_to_media', path_to_media)
            setattr(msg, 'file_name', filename.replace('_', ' '))
            setattr(msg, 'is_video', is_video)
            setattr(msg, 'quality', quality)
            Vars.CLIENT = msg.client
            if forceplay:
                QUEUE.insert(0, msg)
            else:
                if Dynamic.PLAYING:
                    await reply_text(msg, get_scheduled_text(msg.file_name))
                QUEUE.append(msg)
        else:
            mesg = await reply_text(msg, f"Searching `{input_str}` on YouTube")
            title, link = await get_song(input_str)
            if link:
                details = await get_song_info(link)
                if not details:
                    return await mesg.edit("Invalid YouTube link found during search!")
                _, duration = details
                if Dynamic.PLAYING and not forceplay:
                    msg = await reply_text(msg, get_scheduled_text(title, link))
                else:
                    msg = await msg.edit(f"[{title}]({link})")
                flags["duration"] = duration
                await mesg.delete()
                setattr(msg, '_flags', flags)
                if forceplay:
                    QUEUE.insert(0, msg)
                else:
                    QUEUE.append(msg)
            else:
                await mesg.edit("No results found.")
    elif msg.reply_to_message:
        replied = msg.reply_to_message
        replied_file = replied.audio or replied.video or replied.document
        if not replied_file:
            return await reply_text(msg, "Input not found")
        if replied.audio:
            setattr(
                replied.audio,
                'file_name',
                replied_file.title or replied_file.file_name or "Song")
            setattr(replied.audio, 'is_video', False)
            setattr(replied.audio, 'quality', 100)
        elif replied.video:
            setattr(replied.video, 'is_video', is_video)
            setattr(replied.video, 'quality', quality)
        elif replied.document and "video" in replied.document.mime_type:
            setattr(replied.document, 'is_video', is_video)
            setattr(replied.document, 'quality', quality)
        else:
            return await reply_text(msg, "Replied media is invalid.")

        if msg.sender_chat:
            setattr(replied, 'sender_chat', msg.sender_chat)
        elif msg.from_user:
            setattr(replied, 'from_user', msg.from_user)
        Vars.CLIENT = msg.client
        if forceplay:
            QUEUE.insert(0, replied)
        else:
            if Dynamic.PLAYING:
                await reply_text(msg, get_scheduled_text(replied_file.file_name, replied.link))
            QUEUE.append(replied)
    else:
        return await reply_text(msg, "Input not found")

    if not Dynamic.PLAYING or forceplay:
        await skip_song()


async def skip_song(clear_queue: bool = False):
    if Dynamic.PLAYING:
        # skip current playing song to play next
        Dynamic.PLAYING = False
        await call.change_stream(
            Vars.CHAT_ID,
            AudioPiped(
                "http://duramecho.com/Misc/SilentCd/Silence{}s.mp3".format(
                    '01' if not QUEUE or clear_queue else '32'
                )
            )
        )

    if CQ_MSG:
        for msg in CQ_MSG:
            await msg.delete()
        CQ_MSG.clear()

    if clear_queue:
        QUEUE.clear()

    if not QUEUE:
        return

    shutil.rmtree("temp_music_dir", ignore_errors=True)
    msg = QUEUE.pop(0)

    try:
        Dynamic.PLAYING = True
        if msg.audio or msg.video or msg.document or hasattr(msg, "file_name"):
            await tg_down(msg)
        else:
            await yt_down(msg)
    except Exception as err:
        Dynamic.PLAYING = False
        out = f'**ERROR:** `{err}`'
        await CHANNEL.log(f"`{format_exc().strip()}`")
        if QUEUE:
            out += "\n\n`Playing next Song.`"
        await Vars.CLIENT.send_message(
            Vars.CHAT_ID,
            out,
            disable_web_page_preview=True
        )
        await skip_song()


async def on_join(group_call: Optional[GroupCall] = None) -> None:
    if group_call:
        LOG.info("Joined group call: [%s], participants: [%s]",
                 group_call.title, group_call.participants_count)
    else:
        LOG.info("Joined group call: [%s] [joinvc]", Vars.CHAT_NAME)
        try:
            GROUP_CALL_PARTICIPANTS.clear()
            for p in await call.get_participants(Vars.CHAT_ID):
                if p.user_id == userge.id:
                    continue
                GROUP_CALL_PARTICIPANTS.append(p.user_id)
        except GroupCallNotFound as err:
            LOG.error(err)


async def on_left(group_call: Optional[GroupCall] = None) -> None:

    if group_call:
        LOG.info("Left group call: [%s], participants: [%s]",
                 group_call.title, group_call.participants_count)
    else:
        LOG.info("Left group call: [%s] [leavevc]", Vars.CHAT_NAME)

    Vars.CHAT_NAME = ""
    Vars.CHAT_ID = 0
    CONTROL_CHAT_IDS.clear()
    QUEUE.clear()
    CURRENT_SONG.clear()
    GROUP_CALL_PARTICIPANTS.clear()
    Dynamic.PLAYING = False
    Vars.BACK_BUTTON_TEXT = ""
    if CQ_MSG:
        for msg in CQ_MSG:
            await msg.delete()
        CQ_MSG.clear()


async def invite_vc_client(msg: Message) -> bool:
    """ Invites the VC_CLIENT to the current chat. """
    invite_link = msg.filtered_input_str
    if not invite_link:
        try:
            link = await msg.client.create_chat_invite_link(msg.chat.id)
        except ChatAdminRequired:
            await reply_text(msg, '`Provide a invite link along command.!!`')
            return False
        else:
            invite_link = link.invite_link
    try:
        await VC_CLIENT.join_chat(invite_link)
    except UserAlreadyParticipant:
        await reply_text(msg, 'User already present in this chat')
    except UserBannedInChannel:
        await reply_text(msg, 'Unable to join this chat since user is banned here.')
    except Exception as e:
        await reply_text(msg, f'**ERROR**: {e}')
    else:
        await reply_text(msg, 'VC_CLIENT Successfully joined.')
        return True
    return False


async def yt_down(msg: Message):
    """ youtube downloader """
    title, url = get_yt_info(msg)
    message = await reply_text(msg, f"`Preparing {title}`")
    stream_link = await get_stream_link(url)

    if not stream_link:
        raise Exception("Song not Downloaded, add again in Queue [your wish]")

    flags = msg.flags
    is_video = "-v" in flags
    duration = int(flags.get("duration"))
    quality = max(min(100, int(flags.get('-q', 100))), 1)
    height, width, has_audio, has_video = await get_file_info(stream_link)

    CURRENT_SONG.update({
        'file': stream_link,
        "height": height,
        "width": width,
        "has_video": has_video,
        "is_video": is_video and has_video,
        "duration": duration,
        "quality": quality,
        "is_live": duration == 0
    })

    if is_video and has_video:
        await play_video(stream_link, height, width, quality)
    elif has_audio:
        await play_audio(stream_link)
    else:
        out = "Invalid media found in queue, and skipped"
        if QUEUE:
            out += "\n\n`Playing next Song.`"
        await reply_text(
            msg,
            out
        )
        return await skip_song()

    await message.delete()

    Vars.BACK_BUTTON_TEXT = (
        f"🎶 **Now playing:** [{title}]({url})\n"
        f"⏳ **Duration:** `{'Live' if not duration else time_formatter(duration)}`\n"
        f"🎧 **Requested By:** {requester(msg)}")

    raw_msg = await reply_text(
        msg,
        Vars.BACK_BUTTON_TEXT,
        markup=default_markup() if userge.has_bot else None,
        to_reply=False
    )
    CQ_MSG.append(raw_msg)

    if msg.from_user and msg.client.id == msg.from_user.id:
        await msg.delete()


async def tg_down(msg: Message):
    """ TG downloader """
    file = msg.audio or msg.video or msg.document or msg
    title = file.file_name
    setattr(msg, '_client', Vars.CLIENT)
    message = await reply_text(
        msg, f"`{'Preparing' if hasattr(msg, 'file_name') else 'Downloading'} {title}`"
    )
    duration = 0
    if not hasattr(msg, "path_to_media"):
        path = await msg.client.download_media(
            message=msg,
            file_name="temp_music_dir/",
            progress=progress,
            progress_args=(message, "Downloading..."))
        filename = os.path.join("temp_music_dir", os.path.basename(path))
        if msg.audio:
            duration = msg.audio.duration
        elif msg.video or msg.document:
            duration = await get_duration(shlex.quote(filename))
    else:
        filename = msg.path_to_media
        duration = await get_duration(shlex.quote(msg.path_to_media))
    if duration > MAX_DURATION:
        await reply_text(msg, "**ERROR:** `Max song duration limit reached!`")
        return await skip_song()
    if hasattr(msg, 'file_info'):
        height, width, has_audio, has_video = msg.file_info
    else:
        height, width, has_audio, has_video = await get_file_info(shlex.quote(filename))

    is_video = file.is_video
    quality = max(min(100, int(getattr(file, 'quality', 100))), 1)

    CURRENT_SONG.update({
        'file': filename,
        "height": height,
        "width": width,
        "has_video": has_video,
        "is_video": is_video and has_video,
        "duration": duration,
        "quality": quality,
        "is_live": duration == 0
    })

    if is_video and has_video:
        await play_video(filename, height, width, quality)
    elif has_audio:
        await play_audio(filename)
    else:
        out = "Invalid media found in queue, and skipped"
        if QUEUE:
            out += "\n\n`Playing next Song.`"
        await reply_text(
            msg,
            out
        )
        return await skip_song()

    await message.delete()

    Vars.BACK_BUTTON_TEXT = (
        f"🎶 **Now playing:** [{title}]({msg.link})\n"
        f"⏳ **Duration:** `{'Live' if not duration else time_formatter(duration)}`\n"
        f"🎧 **Requested By:** {requester(msg)}")

    raw_msg = await reply_text(
        msg,
        Vars.BACK_BUTTON_TEXT,
        markup=default_markup() if userge.has_bot else None,
        to_reply=False
    )
    CQ_MSG.append(raw_msg)


async def seek_music(dur: int, jump: bool = False) -> bool:
    if CURRENT_SONG.get('is_live', False):
        return False
    if jump:
        seek_point = max(0, dur)
        CURRENT_SONG['start'] = time.time() - seek_point
    else:
        seek_point = max(0, (time.time() - CURRENT_SONG['start'] + dur))
        # adjusting seek time in start time
        CURRENT_SONG['start'] -= dur
    if seek_point > CURRENT_SONG['duration']:
        return False
    if CURRENT_SONG['is_video']:
        await play_video(
            CURRENT_SONG['file'],
            CURRENT_SONG['height'],
            CURRENT_SONG['width'],
            CURRENT_SONG['quality'],
            int(float(seek_point))
        )
    else:
        await play_audio(
            CURRENT_SONG['file'],
            seek_point
        )
    return True


async def replay_music(flags: dict = None) -> bool:
    is_video = False
    if flags and '-v' in flags:
        is_video = CURRENT_SONG['has_video']
        CURRENT_SONG['is_video'] = is_video
    elif flags and '-a' in flags:
        is_video = False
    else:
        is_video = CURRENT_SONG['is_video']
    try:
        if is_video:
            await play_video(
                CURRENT_SONG['file'],
                CURRENT_SONG['height'],
                CURRENT_SONG['width'],
                CURRENT_SONG['quality']
            )
        else:
            await play_audio(
                CURRENT_SONG['file']
            )
    except KeyError:
        return False
    return True


async def play_video(file: str, height: int, width: int, quality: int, seek: int = None):
    r_width, r_height = get_quality_ratios(width, height, quality)
    ffmpeg_parm = f'-ss {seek} -atend -to {CURRENT_SONG["duration"]}' if seek else ''

    try:
        await call.change_stream(
            Vars.CHAT_ID,
            AudioVideoPiped(
                file,
                video_parameters=VideoParameters(
                    r_width,
                    r_height,
                    25
                ),
                additional_ffmpeg_parameters=ffmpeg_parm
            )
        )
    except NotInGroupCallError:
        await call.join_group_call(
            Vars.CHAT_ID,
            AudioVideoPiped(
                file,
                video_parameters=VideoParameters(
                    r_width,
                    r_height,
                    25
                ),
                additional_ffmpeg_parameters=ffmpeg_parm
            )
        )
    if not seek:
        CURRENT_SONG['start'] = time.time()


async def play_audio(file: str, seek: int = None):
    ffmpeg_parm = f'-ss {seek} -atend -to {CURRENT_SONG["duration"]}' if seek else ''
    try:
        await call.change_stream(
            Vars.CHAT_ID,
            AudioPiped(
                file,
                additional_ffmpeg_parameters=ffmpeg_parm
            )
        )
    except NotInGroupCallError:
        await call.join_group_call(
            Vars.CHAT_ID,
            AudioPiped(
                file,
                additional_ffmpeg_parameters=ffmpeg_parm
            ),
            stream_type=StreamType().pulse_stream,
        )
    if not seek:
        CURRENT_SONG['start'] = time.time()
