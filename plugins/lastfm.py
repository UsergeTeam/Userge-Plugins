""" last.fm module """

# By @Krishna_Singhal

import os
import wget
import pylast
import asyncio

from typing import Optional
from urllib.parse import unquote

from pyrogram.errors import ChatWriteForbidden, ChannelPrivate, ChatIdInvalid
from userge import userge, Message, Config, pool, get_collection
from userge.utils import time_formatter

API_KEY = os.environ.get("FM_API")
API_SECRET = os.environ.get("FM_SECRET")
USERNAME = os.environ.get("FM_USERNAME")
PASSWORD = pylast.md5(os.environ.get("FM_PASSWORD"))
CHAT_IDS = [
    int(x) for x in os.environ.get("LASTFM_CHAT_ID", str(Config.LOG_CHANNEL_ID)).split()
]

LASTFM_DB = get_collection("LASTFM")
NOW_PLAYING = [False, None]


async def _init():
    global NOW_PLAYING  # pylint: disable=global-statement
    k = await LASTFM_DB.find_one({'_id': "LASTFM"})
    if k:
        NOW_PLAYING[0] = bool(k['data'])


def check_creds(func):
    """ decorator for checking creds """
    async def checker(msg: Message):
        if _check_creds():
            await func(msg)
        else:
            await msg.edit(
                "`This plugins needs environmental variables,"
                " For more info see` "
                "[this post](https://t.me/UnofficialPluginsHelp/123).",
                disable_web_page_preview=True
            )
    return checker


@check_creds
@userge.on_cmd("lastfm", about={
    'header': "see current playing song and "
              "allow bot to send regular updates of song.",
    'flags': {'-on': "allow bot to send regular updation of songs",
              '-off': "disallow bot to send updates"},
    'usage': "{tr}lastfm\n{tr}lastfm [flags]"})
async def _lastfm(msg: Message):
    """ see current playing song """
    global NOW_PLAYING  # pylint: disable=global-statement
    if msg.flags and '-on' in msg.flags:
        NOW_PLAYING[0] = True
        await LASTFM_DB.update_one(
            {'_id': "LASTFM"}, {"$set": {'data': True}}
        )
        await msg.edit("`Auto updates Started.`")
    elif msg.flags and '-off' in msg.flags:
        NOW_PLAYING[0] = False
        await LASTFM_DB.update_one(
            {'_id': "LASTFM"}, {"$set": {'data': False}}
        )
        await msg.edit("`Auto updates Stopped.`")
    else:
        track = await LastFm(msg).now_playing()
        if not track:
            return await msg.edit("`Currently you are not listening to any Song...`")
        if NOW_PLAYING[1] != track.get_name():
            NOW_PLAYING[1] = track.get_name()

        out = f"{USERNAME} __is currently Listening to:__\n\n"
        k = get_track_info(track)
        if not k:
            return await msg.err("Track Not found...")
        await msg.edit(out + k, disable_web_page_preview=True)


@check_creds
@userge.on_cmd("getuser", about={
    'header': "Get user of lastfm.",
    'usage': "{tr}getuser\n{tr}getuser [username]"})
async def get_user(msg: Message):
    """ get last.fm user """
    await msg.edit("`checking user...`")
    if msg.input_str:
        user = LastFm(msg).get_user(msg.input_str)
    else:
        user = LastFm(msg).get_user()

    out = f'''
__Name:__ [{user.get_name()}]({unquote(user.get_url())})
__Country:__ `{user.get_country()}`
'''
    if user.get_loved_tracks():
        out += '__GetLovedTracks:__\n'
        out += "\n".join(
            [
                f"    `{i}. {a[0]} 😘`"
                for i, a in enumerate(user.get_loved_tracks(15), start=1)]
        )
    else:
        out += '__GetLovedTracks:__ `No tracks found.`\n'

    if bool(user.get_now_playing()):
        out += '__NowPlaying:__ `True`\n'
        out += f'    __● SongName:__ `{user.get_now_playing()}`'
    else:
        out += '__NowPlaying:__ `False`'

    if user.get_image():
        path = os.path.join(Config.DOWN_PATH, f"{user.get_name()}.png")
        if not os.path.exists(path):
            await pool.run_in_thread(wget.download)(user.get_image(), path)
    else:
        path = "resources/no_image.png"

    await asyncio.gather(
        msg.delete(),
        msg.client.send_photo(
            chat_id=msg.chat.id,
            photo=path,
            caption=out
        )
    )


@check_creds
@userge.on_cmd("lovesong", about={
    'header': "Love any track.",
    'description': "Specify which track you wanna love\n"
                   "if track will not specify then it will "
                   "take current listening track, if any.",
    'usage': "{tr}lovesong (if listening any song)\n{tr}lovesong Artist - Title"})
async def love_track(msg: Message):
    """ love any last.fm song """
    await LastFm(msg).love()


@check_creds
@userge.on_cmd("unlove", about={
    'header': "UnLove any track.",
    'description': "Specify which track you wanna Unlove\n"
                   "if track will not specify then it will "
                   "take current listening track, if any.",
    'usage': "{tr}unlove (if listening any song)\n{tr}unlove Artist - Title"})
async def unlove_track(msg: Message):
    """ remove loved song from loved list """
    await LastFm(msg).rmlove()


@check_creds
@userge.on_cmd("getloved", about={
    'header': "Get list of all loved tracks.",
    'usage': "{tr}getloved\n{tr}getloved 20"})
async def get_loved(msg: Message):
    """ get list of loved song """
    await LastFm(msg).get_loved()


@check_creds
@userge.on_cmd("getrack", about={
    'header': "Get track of lastfm.",
    'usage': "{tr}getrack\n{tr} getrack Artist - Title"})
async def get_track(msg: Message):
    """ get pylast.Track info """
    await msg.edit('`getting info...`')
    track = await LastFm(msg).get_track()
    if not track:
        return await msg.edit("Please see `.help getrack`")
    out = get_track_info(track)
    if not out:
        return await msg.err("Track not found...")
    await msg.edit(out, disable_web_page_preview=True)


@check_creds
@userge.on_cmd(
    "getrecent", about={
        'header': "Get recent tracks of Users or Myself.",
        'flags': {'-l': "specify limit"},
        'usage': "{tr}getrecent\n{tr}getrecent -l5",
        'example': [
            "{tr}getrecent", "{tr}getrecent -l5", "{tr}getrecent Krishna_69"
        ]
    }
)
async def get_last_played(msg: Message):
    """ get list of played song of any user """
    await LastFm(msg).get_last_played()


@userge.add_task
async def lastfm_worker():
    global NOW_PLAYING  # pylint: disable=global-statement

    user = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=USERNAME,
        password_hash=PASSWORD
    ).get_user(USERNAME)
    while NOW_PLAYING[0] is True and await _get_now_playing(user) is not None:
        song = await _get_now_playing(user)
        if NOW_PLAYING[1] != song.get_name():
            NOW_PLAYING[1] = song.get_name()
            for chat_id in CHAT_IDS:
                out = f"{USERNAME} __is currently Listening to:__\n\n"
                k = get_track_info(song)
                if not k:
                    NOW_PLAYING[0] = False
                    return
                out += k
                if userge.has_bot:
                    try:
                        await userge.bot.send_message(
                            chat_id, out, disable_web_page_preview=True
                        )
                    except (ChatWriteForbidden, ChannelPrivate, ChatIdInvalid):
                        await userge.send_message(
                            chat_id, out, disable_web_page_preview=True
                        )
                else:
                    await userge.send_message(
                        chat_id, out, disable_web_page_preview=True
                    )
    NOW_PLAYING[0] = False  # Should not update to DB ig ?


#########################################################################


def _check_creds() -> bool:
    """ check creds """
    if API_KEY and API_SECRET and USERNAME and PASSWORD:
        return True
    return False


def get_track_info(track: pylast.Track) -> Optional[str]:
    try:
        duration = time_formatter(int(track.get_duration()) / 1000)
        _tags = track.get_tags()
        tags = " ".join([f'`{i}`' for i in _tags]) if len(_tags) > 0 else '`None`'
        out = f'''__LastFm's__ [{track.get_correction()}]({unquote(track.get_url())})

__Duration:__ `{duration if duration else None}`
__Is_Loved:__ `{bool(track.get_userloved())}`
__Is_Streamable:__ `{bool(track.is_streamable())}`
__Tags:__ {tags}
'''
    except pylast.WSError:
        return None
    else:
        return out


@pool.run_in_thread
def _get_now_playing(user: pylast.User) -> Optional[pylast.Track]:
    return user.get_now_playing()


#########################################################################


class LastFm:
    """ custom class for last.fm 😉 """

    def __init__(self, msg: Message) -> None:
        self.msg = msg

    @staticmethod
    def _network() -> pylast.LastFMNetwork:
        return pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            username=USERNAME,
            password_hash=PASSWORD
        )

    @staticmethod
    def _format_track(track: pylast.Track) -> str:
        return f"`{track.track} - {track.playback_date}`"

    def get_user(self, username: str = USERNAME) -> pylast.User:
        return (self._network()).get_user(username)

    async def now_playing(self, username: str = USERNAME) -> Optional[pylast.Track]:
        user = self.get_user(username)
        playing = await _get_now_playing(user)
        return playing

    async def love(self) -> None:
        track = await self.get_track()
        if not track:
            return await self.msg.err("Sorry, track not found.")
        await self.msg.edit("`Loving this Track.`")
        try:
            track.love()
            await asyncio.sleep(3)
            if track.get_userloved():
                await self.msg.edit("`💕 Loved this track...`")
        except Exception as err:
            await self.msg.err(str(err))

    async def rmlove(self) -> None:
        track = await self.get_track()
        if not track:
            return await self.msg.err("Sorry, track not found.")
        await self.msg.edit("`UnLoving this Track.`")
        try:
            track.unlove()
            await asyncio.sleep(3)
            if not track.get_userloved():
                await self.msg.edit("`🖤 UnLoved this track...`")
        except Exception as err:
            await self.msg.err(str(err))

    async def get_loved(self) -> None:
        await self.msg.edit("`Getting your loved tracks...`")
        limit = 20
        if self.msg.input_str and self.msg.input_str.is_numeric():
            limit = int(self.msg.input_str)
        tracks = (self.get_user()).get_loved_tracks(limit=limit)
        out = ""
        for i, track in enumerate(tracks, start=1):
            out += f"`{i}.` `{str(track[0])}` 💕\n"
        if out:
            return await self.msg.edit(out)
        await self.msg.err("No loved tracks found.")

    async def get_track(self) -> Optional[pylast.Track]:
        if self.msg.input_str and '-' in self.msg.input_str:
            artist, title = self.msg.input_str.split('-', maxsplit=1)
            artist = artist.strip()
            title = title.strip()
            track = pylast.Track(artist, title, self._network())
        else:
            track = await self.now_playing()
        if not track:
            return None
        return track

    def _get_tracks(self, user: pylast.User, limit: int) -> Optional[str]:
        recent_tracks = user.get_recent_tracks(limit=limit)

        out = ""
        for i, t in enumerate(recent_tracks, start=1):
            track = self._format_track(t)
            out += f"\n{i}. {track}"
            if track.get_userloved():
                out += " 💕"
        if not out:
            return None
        return out

    async def get_last_played(self) -> None:
        await self.msg.edit("`getting tracks...`")
        limit = int(self.msg.flags.get('-l', 10))
        if self.msg.filtered_input_str:
            user = self.get_user(self.msg.filtered_input_str)
        else:
            user = self.get_user()
        out = f"Last played tracks of {user.get_name()}:\n"
        try:
            get_tracks = self._get_tracks(user, limit)
            if not get_tracks:
                return await self.msg.err("Tracks not found")
            out += get_tracks
            await self.msg.edit(out)
        except pylast.WSError as e:
            await self.msg.edit(f"**Soemthing went worng**\n\n`{str(e)}`")


##########################################################################
