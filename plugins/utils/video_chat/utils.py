import re
import os
import json
import time
import math
from json.decoder import JSONDecodeError
from typing import List, Tuple, Optional

from youtubesearchpython import VideosSearch

from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            CallbackQuery)
from pyrogram import enums

from userge import userge, Message, pool
from userge.utils import runcmd, time_formatter, get_custom_import_re
from . import (QUEUE, LOG,
               CURRENT_SONG,
               CONTROL_CHAT_IDS,
               GROUP_CALL_PARTICIPANTS,
               MAX_DURATION,
               YTDL_PATH,
               Dynamic, Vars)
ytdl = get_custom_import_re(YTDL_PATH)

_SCHEDULED = "[{title}]({link}) Scheduled to QUEUE on #{position} position"
yt_regex = re.compile(
    r'(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%?]{11})'
)


def is_yt_url(url: str) -> Optional[re.Match]:
    return yt_regex.match(url)


async def reply_text(
    msg: Message,
    text: str,
    markup=None,
    to_reply: bool = True,
    parse_mode: enums.ParseMode = None,
    del_in: int = -1
) -> Message:
    kwargs = {
        'chat_id': msg.chat.id,
        'text': text,
        'del_in': del_in,
        'reply_to_message_id': msg.id if to_reply else None,
        'reply_markup': markup,
        'disable_web_page_preview': True
    }
    if parse_mode:
        kwargs['parse_mode'] = parse_mode
    new_msg = await msg.client.send_message(**kwargs)
    if to_reply and not isinstance(new_msg, bool):
        new_msg.reply_to_message = msg
    return new_msg


def get_scheduled_text(title: str, link: str = None) -> str:
    return _SCHEDULED.format(title=title, link=link, position=len(QUEUE) + 1)


def vc_chat(func):
    """ decorator for Video-Chat chat """

    async def checker(msg: Message):
        if Vars.CHAT_ID and msg.chat.id in ([Vars.CHAT_ID] + CONTROL_CHAT_IDS):
            await func(msg)
        elif Vars.CHAT_ID and msg.outgoing:
            await msg.edit("You can't access video_chat from this chat.")
        elif msg.outgoing:
            await msg.edit("`Haven't join any Video-Chat...`")

    checker.__doc__ = func.__doc__

    return checker


def check_enable_for_all(func):
    """ decorator to check cmd is_enable for others """

    async def checker(msg: Message):
        is_self = msg.from_user and msg.from_user.id == userge.id
        user_in_vc = msg.from_user and msg.from_user.id in GROUP_CALL_PARTICIPANTS
        sender_chat_in_vc = msg.sender_chat and msg.sender_chat.id in GROUP_CALL_PARTICIPANTS

        if is_self or (Dynamic.CMDS_FOR_ALL and (user_in_vc or sender_chat_in_vc)):
            await func(msg)

    checker.__doc__ = func.__doc__

    return checker


def check_cq_for_all(func):
    """ decorator to check CallbackQuery users """

    async def checker(_, cq: CallbackQuery):
        is_self = cq.from_user and cq.from_user.id == userge.id
        user_in_vc = cq.from_user and cq.from_user.id in GROUP_CALL_PARTICIPANTS

        if is_self or (Dynamic.CMDS_FOR_ALL and user_in_vc):
            await func(cq)
        else:
            await cq.answer(
                "⚠️ You don't have permission to use me", show_alert=True)

    checker.__doc__ = func.__doc__

    return checker


def default_markup() -> InlineKeyboardMarkup:
    """ default markup for playing text """

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=get_player_string(), callback_data='player')
            ],
            [
                InlineKeyboardButton(
                    text="⏩ Skip", callback_data="skip"),
                InlineKeyboardButton(
                    text="🗒 Queue", callback_data="queue")
            ]
        ])


def volume_button_markup() -> InlineKeyboardMarkup:
    """ volume buttons markup """

    buttons = [
        [
            InlineKeyboardButton(text="🔈 50", callback_data="vol(50)"),
            InlineKeyboardButton(text="🔉 100", callback_data="vol(100)")
        ],
        [
            InlineKeyboardButton(text="🔉 150", callback_data="vol(150)"),
            InlineKeyboardButton(text="🔊 200", callback_data="vol(200)")
        ],
        [
            InlineKeyboardButton(text="🖌 Enter Manually", callback_data="vol(custom)"),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def get_player_string() -> str:
    current_dur = CURRENT_SONG.get('pause', time.time())
    played_duration = round(current_dur - CURRENT_SONG['start'])
    duration = played_duration if CURRENT_SONG.get('is_live', False) else CURRENT_SONG['duration']
    try:
        percentage = played_duration * 100 / duration
    except ZeroDivisionError:
        percentage = 100
    player_string = "▷ {0}◉{1}".format(
        ''.join(["━" for _ in range(math.floor(percentage / 6.66))]),
        ''.join(["─" for _ in range(15 - math.floor(percentage / 6.66))])
    )
    return f"{time_formatter(played_duration)}   {player_string}    {time_formatter(duration)}"


@pool.run_in_thread
def get_song(name: str) -> Tuple[str, str]:
    results: List[dict] = VideosSearch(name, limit=1).result()['result']
    if results:
        return results[0].get('title', name), results[0].get('link')
    return name, ""


@pool.run_in_thread
def get_song_info(url: str) -> Tuple[str, int]:
    ydl_opts = {}

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = info.get("duration") or 0

        if duration > MAX_DURATION:
            duration = -1
    return info.get("title"), duration if duration else 0


async def get_stream_link(link: str) -> str:
    yt_dl = (os.environ.get("YOUTUBE_DL_PATH", "yt_dlp")).replace("_", "-")
    cmd = yt_dl + \
        " --geo-bypass -g -f best[height<=?720][width<=?1280] " + link
    out, err, _, _ = await runcmd(cmd)
    if err:
        LOG.error(err)
    return out or False


async def get_duration(file: str) -> int:
    cmd = "ffprobe -i {file} -v error -show_entries format=duration -of json -select_streams v:0"
    out, _, _, _ = await runcmd(cmd.format(file=file))

    try:
        out = json.loads(out)
    except JSONDecodeError:
        return 0

    dur = int(float((out.get("format", {})).get("duration", 0)))
    return dur


async def get_file_info(file) -> Tuple[int, int, bool, bool]:
    cmd = "ffprobe -v error -show_entries stream=width,height,codec_type,codec_name -of json {file}"
    out, _, _, _ = await runcmd(cmd.format(file=file))
    try:
        output = json.loads(out) or {}
    except JSONDecodeError:
        output = {}
    streams = output.get('streams', [])
    width, height, have_audio, have_video = 0, 0, False, False
    for stream in streams:
        if (
            stream.get('codec_type', '') == 'video'
            and stream.get('codec_name', '') not in ['png', 'jpeg', 'jpg']
        ):
            width = int(stream.get('width', 0))
            height = int(stream.get('height', 0))
            if width and height:
                have_video = True
        elif stream.get('codec_type', '') == "audio":
            have_audio = True
    return height, width, have_audio, have_video


def requester(msg: Message):
    if not msg.from_user:
        if msg.sender_chat:
            return msg.sender_chat.title
        return None
    replied = msg.reply_to_message
    if replied and msg.client.id == msg.from_user.id:
        if not replied.from_user:
            if replied.sender_chat:
                return replied.sender_chat.title
            return None
        return replied.from_user.mention
    return msg.from_user.mention


def get_quality_ratios(w: int, h: int, q: int) -> Tuple[int, int]:
    rescaling = min(w, 1280) * 100 / w if w > h else min(h, 720) * 100 / h
    h = round((h * rescaling) / 100 * (q / 100))
    w = round((w * rescaling) / 100 * (q / 100))
    return w - 1 if w % 2 else w, h - 1 if h % 2 else h
