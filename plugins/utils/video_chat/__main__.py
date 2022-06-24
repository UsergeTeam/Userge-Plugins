""" Userge Video-Chat Plugin """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved
#
# Author (C) - @Krishna_Singhal (https://github.com/Krishna-Singhal)

import time
import random
import asyncio

from pyrogram import ContinuePropagation
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.errors import ChannelInvalid, ChannelPrivate
from pyrogram.raw.base import Message as BaseMessage
from pyrogram.raw.functions.phone import (GetGroupCall,
                                          GetGroupCallJoinAs,
                                          CreateGroupCall)
from pyrogram.raw.types import UpdateGroupCallParticipants, InputGroupCall
from pyrogram import enums

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import (
    AudioPiped,
    Update,
    StreamAudioEnded,
    JoinedGroupCallParticipant,
    LeftGroupCallParticipant
)
from pytgcalls.exceptions import (
    NodeJSNotInstalled,
    TooOldNodeJSVersion,
    NoActiveGroupCall,
    AlreadyJoinedError,
    NotInGroupCallError
)

from userge import userge, Message, get_collection, config, filters
from userge.utils import time_formatter

from . import (
    QUEUE, GROUP_CALL_PARTICIPANTS, CURRENT_SONG,
    CONTROL_CHAT_IDS, LOG, VC_SESSION, VC_CLIENT, call,
    Dynamic, Vars
)
from .resource import TgResource
from .helpers import (
    skip_song, on_join, on_left, play_music,
    invite_vc_client, seek_music, replay_music
)
from .utils import (
    reply_text, default_markup, vc_chat,
    volume_button_markup, check_enable_for_all
)
from .callbacks import vc_callback, vc_control_callback, vol_callback

VC_DB = get_collection("VC_CMDS_TOGGLE")


@userge.on_start
async def _init():
    data = await VC_DB.find_one({'_id': 'VC_CMD_TOGGLE'})
    if data:
        Dynamic.CMDS_FOR_ALL = bool(data['is_enable'])
    if VC_SESSION:
        await VC_CLIENT.start()
        me = await VC_CLIENT.get_me()
        LOG.info(f"Separate VC CLIENT FOUND - {me.first_name}")


@userge.on_stop
async def stop_vc_client():
    if VC_SESSION:
        await VC_CLIENT.stop()


@userge.on_cmd("joinvc", about={
    'header': "Join Video-Chat",
    'flags': {
        '-as': "Join as any of your public channel.",
        '-at': "Joins vc in a remote chat and control it from saved messages/linked chat"},
    'examples': [
        "{tr}joinvc -as=@TheUserge -at=@UsergeOT - Join VC of @UsergeOT as @TheUserge.",
        "{tr}joinvc -at=-100123456789 - Join VC of any private channel / group."]},
    allow_bots=False)
async def joinvc(msg: Message):
    """ join video chat """
    await msg.delete()
    if Vars.CHAT_NAME:
        return await reply_text(msg, f"`Already joined in {Vars.CHAT_NAME}`")

    flags = msg.flags
    join_as = flags.get('-as')
    chat = flags.get('-at')

    if not chat and msg.chat.type == enums.ChatType.PRIVATE:
        return await msg.err("Invalid chat, either use in group / channel or use -at flag.")
    if chat:
        if chat.strip("-").isnumeric():
            chat = int(chat)
        try:
            _chat = await VC_CLIENT.get_chat(chat)
        except Exception as e:
            return await reply_text(msg, f'Invalid Join In Chat Specified\n{e}')
        Vars.CHAT_ID = _chat.id
        Vars.CHAT_NAME = _chat.title
        # Joins video_chat in a remote chat and control it from Saved Messages
        # / Linked Chat
        CONTROL_CHAT_IDS.append(userge.id)
        if _chat.linked_chat:
            CONTROL_CHAT_IDS.append(_chat.linked_chat.id)
    else:
        chat_id_ = msg.chat.username or msg.chat.id
        try:
            # caching the peer in case of public chats to play without joining
            # for VC_SESSION_STRING
            await VC_CLIENT.get_chat(chat_id_)
        except (ChannelInvalid, ChannelPrivate):
            msg_ = await reply_text(
                msg,
                'You are using VC_SESSION_STRING and it seems that user is '
                'not present in this group.\ntrying to join group.')
            join = await invite_vc_client(msg)
            await msg_.delete()
            if not join:
                return
        Vars.CHAT_ID = msg.chat.id
        Vars.CHAT_NAME = msg.chat.title
    if join_as:
        if join_as.strip("-").isnumeric():
            join_as = int(join_as)
        try:
            join_as = (await VC_CLIENT.get_chat(join_as)).id
        except Exception as e:
            Vars.CHAT_ID, Vars.CHAT_NAME = 0, ''
            CONTROL_CHAT_IDS.clear()
            return await reply_text(msg, f'Invalid Join As Chat Specified\n{e}')
        join_as_peers = await VC_CLIENT.invoke(GetGroupCallJoinAs(
            peer=(
                await VC_CLIENT.resolve_peer(Vars.CHAT_ID)
            )
        ))
        raw_id = int(str(join_as).replace("-100", ""))
        if raw_id not in [
            getattr(peers, "user_id", None)
            or getattr(peers, "channel_id", None)
            for peers in join_as_peers.peers
        ]:
            Vars.CHAT_ID, Vars.CHAT_NAME = 0, ''
            CONTROL_CHAT_IDS.clear()
            return await reply_text(msg, "You cant join the video chat as this channel.")

    if join_as:
        peer = await VC_CLIENT.resolve_peer(join_as)
    else:
        peer = await VC_CLIENT.resolve_peer('me')
    try:
        if not call.is_connected:
            await call.start()
        await call.join_group_call(
            Vars.CHAT_ID,
            AudioPiped(
                'http://duramecho.com/Misc/SilentCd/Silence01s.mp3'
            ),
            join_as=peer,
            stream_type=StreamType().pulse_stream
        )
    except NoActiveGroupCall:
        try:
            peer = await VC_CLIENT.resolve_peer(Vars.CHAT_ID)
            await VC_CLIENT.invoke(
                CreateGroupCall(
                    peer=peer, random_id=2
                )
            )
            await asyncio.sleep(3)
            Vars.CHAT_ID, Vars.CHAT_NAME = 0, ''
            CONTROL_CHAT_IDS.clear()
            return await joinvc(msg)
        except Exception as err:
            Vars.CHAT_ID, Vars.CHAT_NAME = 0, ''
            CONTROL_CHAT_IDS.clear()
            return await reply_text(msg, str(err))
    except (NodeJSNotInstalled, TooOldNodeJSVersion):
        return await reply_text(msg, "NodeJs is not installed or installed version is too old.")
    except AlreadyJoinedError:
        await call.leave_group_call(Vars.CHAT_ID)
        await asyncio.sleep(3)
        Vars.CHAT_ID, Vars.CHAT_NAME = 0, ''
        CONTROL_CHAT_IDS.clear()
        return await joinvc(msg)
    except Exception as e:
        Vars.CHAT_ID, Vars.CHAT_NAME = 0, ''
        CONTROL_CHAT_IDS.clear()
        return await reply_text(msg, f'Error during Joining the Call\n`{e}`')

    await on_join()
    await reply_text(msg, "`Joined VideoChat Successfully`", del_in=5)


@userge.on_cmd("leavevc", about={
    'header': "Leave Video-Chat",
    'usage': "{tr}leavevc"})
async def leavevc(msg: Message):
    """ leave video chat """
    await msg.delete()
    if Vars.CHAT_NAME:
        try:
            await call.leave_group_call(Vars.CHAT_ID)
        except (NotInGroupCallError, NoActiveGroupCall):
            pass
        await on_left()
        await reply_text(msg, "`Left Videochat`", del_in=5)
    else:
        await reply_text(msg, "`I didn't find any Video-Chat to leave`")


@userge.on_cmd("vcmode", about={
    'header': "Toggle to enable or disable play and queue commands for all users"})
async def toggle_vc(msg: Message):
    """ toggle enable/disable vc cmds """
    await msg.delete()
    Dynamic.CMDS_FOR_ALL = not Dynamic.CMDS_FOR_ALL

    await VC_DB.update_one(
        {'_id': 'VC_CMD_TOGGLE'},
        {"$set": {'is_enable': Dynamic.CMDS_FOR_ALL}},
        upsert=True
    )

    text = (
        "**Enabled**" if Dynamic.CMDS_FOR_ALL else "**Disabled**"
    ) + " commands Successfully"

    await reply_text(msg, text, del_in=5)


@userge.on_cmd("play", about={
    'header': "play or add songs to queue",
    'flags': {
        '-v': "Stream as video.",
        '-q': "Quality of video stream (1-100)"}},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@check_enable_for_all
@vc_chat
async def _play(msg: Message):
    """ play music in video chat """
    return await play_music(msg, False)


@userge.on_cmd("forceplay", about={
    'header': "Force play with skip the current song and "
              "Play your song on #1 Position",
    'flags': {
        '-v': "Stream as video.",
        '-q': "Quality of video stream (1-100)"}})
@vc_chat
async def _forceplay(msg: Message):
    """ forceplay music in video chat """
    return await play_music(msg, True)


@userge.on_cmd("helpvc",
               about={'header': "help for video chat plugin"},
               trigger=config.PUBLIC_TRIGGER,
               allow_private=False,
               check_client=True,
               filter_me=False,
               allow_bots=False)
@vc_chat
@check_enable_for_all
async def _help(msg: Message):
    """ help commands of this plugin for others """
    commands = userge.manager.loaded_plugins["video_chat"].loaded_commands
    key = msg.input_str.lstrip(config.PUBLIC_TRIGGER)
    cmds = []
    raw_cmds = []

    for i in commands:
        if i.name.startswith(config.PUBLIC_TRIGGER):
            cmds.append(i)
            raw_cmds.append(i.name)

    if not key:
        out_str = f"""⚔ <b><u>(<code>{len(cmds)}</code>) Command(s) Available</u></b>

🔧 <b>Plugin:</b>  <code>video_chat</code>
📘 <b>Doc:</b>  <code>Userge Video-Chat Plugin</code>\n\n"""
        for i, cmd in enumerate(cmds, start=1):
            out_str += (
                f"    🤖 <b>cmd(<code>{i}</code>):</b>  <code>{cmd.name}</code>\n"
                f"    📚 <b>info:</b>  <i>{cmd.doc}</i>\n\n")
        return await reply_text(msg, out_str, parse_mode=enums.ParseMode.HTML)

    key = config.PUBLIC_TRIGGER + key
    if key in raw_cmds:
        for cmd in cmds:
            if cmd.name == key:
                out_str = f"<code>{key}</code>\n\n{cmd.about}"
                await reply_text(msg, out_str, parse_mode=enums.ParseMode.HTML)
                break


@userge.on_cmd("current", about={
    'header': "View Current playing Song.",
    'usage': "{tr}current"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def current(msg: Message):
    """ View current playing song """
    if not Vars.BACK_BUTTON_TEXT:
        return await reply_text(msg, "No song is playing!")
    await reply_text(
        msg, Vars.BACK_BUTTON_TEXT, markup=default_markup() if userge.has_bot else None
    )


@userge.on_cmd("queue", about={
    'header': "View Queue of Songs",
    'usage': "{tr}queue"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def view_queue(msg: Message):
    """ View Queue """
    if not QUEUE:
        await reply_text(msg, "`Queue is empty`")
    else:
        list_out = []
        out = f"**{len(QUEUE)} Songs in Queue:**\n"

        for i, r in enumerate(QUEUE, start=1):
            if len(out) > config.MAX_MESSAGE_LENGTH:
                list_out.append(out)
                out = ''
            if isinstance(r, TgResource) and r.path:
                out += f"\n{i}. {r}"
            elif isinstance(r, TgResource):
                out += f"\n{i}. [{r}]({r.message.link})"
            else:
                out += f"\n{i}. [{r}]({r.url})"

        list_out.append(out)

        for m in list_out:
            await reply_text(msg, m)


@userge.on_cmd("volume", about={
    'header': "Set volume",
    'usage': "{tr}volume\n{tr}volume 69"})
@vc_chat
async def set_volume(msg: Message):
    """ change volume """
    await msg.delete()

    if msg.input_str:
        if msg.input_str.isnumeric():
            if 200 >= int(msg.input_str) > 0:
                await call.change_volume_call(Vars.CHAT_ID, int(msg.input_str))
                await reply_text(msg, f"Successfully set volume to __{msg.input_str}__")
            else:
                await reply_text(msg, "Invalid Range!")
        else:
            await reply_text(msg, "Invalid Arguments!")
    else:
        try:
            await userge.bot.send_message(
                msg.chat.id,
                "**🎚 Volume Control**\n\n`Click on the button to change volume"
                " or Click last option to Enter volume manually.`",
                reply_markup=volume_button_markup()
            )
        except Exception:
            await reply_text(msg, "Input not found!")


@userge.on_cmd("skip", about={
    'header': "Skip Song",
    'usage': "{tr}skip\n{tr}skip 2"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def skip_music(msg: Message):
    """ skip music in vc """
    await msg.delete()
    if not QUEUE and not Dynamic.PLAYING:
        return
    if (
        msg.input_str
        and msg.input_str.isnumeric()
        and (len(QUEUE) >= int(msg.input_str) > 0)
    ):
        r = QUEUE.pop(int(msg.input_str) - 1)
        if isinstance(r, TgResource) and r.path:
            out = f"`Skipped` {r}"
        elif isinstance(r, TgResource):
            out = f"`Skipped` [{r}]({r.message.link})"
        else:
            out = f"`Skipped` [{r}]({r.url})"
        await reply_text(msg, out)
        return
    await reply_text(msg, "`Skipped`")
    await skip_song()


@userge.on_cmd("pause", about={
    'header': "Pause Song.",
    'usage': "{tr}pause"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def pause_music(msg: Message):
    """ pause music in vc """
    await msg.delete()
    await call.pause_stream(Vars.CHAT_ID)
    CURRENT_SONG['pause'] = time.time()
    await reply_text(msg, "⏸️ **Paused** Music Successfully")


@userge.on_cmd("seek", about={
    'header': "Seek Song x sec forward / backward.",
    'flags': {
        '-to': "To jump to a specific timestamp"},
    'examples': [
        "{tr}seek 10 - To seek 10 sec forward.",
        "{tr}seek -10 - To seek 10 sec backward.",
        "{tr}seek -to 60 - To play from 60th sec onwards."]},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def seek_music_player(msg: Message):
    """ seek music x sec forward or -x sec backward """
    flags = msg.flags
    dur = msg.filtered_input_str or flags.get('-to', "0")

    try:
        dur = int(dur)
    except ValueError:
        return await reply_text(msg, "Invalid Seek time specified.")

    if '-to' in flags:
        seek = await seek_music(dur, True)
        to_reply = f"Jumped to {time_formatter(dur)}."
    else:
        to_reply = f"Seeked {dur} sec {'backward' if dur < 0 else 'forward'}"
        seek = await seek_music(dur)

    if seek:
        await reply_text(msg, to_reply)
    else:
        await reply_text(
            msg,
            "Sorry i can't do that.\n"
            "Either this is a live stream / seeked duration exceeds maximum duration of file."
        )


@userge.on_cmd("replay", about={
    'header': "replay the current song from beginning.",
    'flags': {
        '-v': "To force play the current song as video",
        '-a': "To force play the current song as audio."},
    'usage': "{tr}replay"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def replay_song_(msg: Message):
    """ replay current song from beginning """
    replay = await replay_music(flags=msg.flags)
    if replay:
        Dynamic.PLAYING = True
        await reply_text(msg, 'Replaying current song from beginning.')
    else:
        await reply_text(msg, 'No songs found to play.')


@userge.on_cmd("resume", about={
    'header': "Resume Song.",
    'usage': "{tr}resume"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def resume_music(msg: Message):
    """ resume music in vc """
    await msg.delete()
    if not CURRENT_SONG.get('pause'):
        return await reply_text(msg, "Nothing paused to resume.")
    await call.resume_stream(Vars.CHAT_ID)
    # adjusting paused duration in start time
    CURRENT_SONG['start'] = CURRENT_SONG['start'] + \
        time.time() - CURRENT_SONG['pause']
    del CURRENT_SONG['pause']
    await reply_text(msg, "◀️ **Resumed** Music Successfully")


@userge.on_cmd("shuffle", about={
    'header': "Shuffle songs in queue.",
    'usage': "{tr}shuffle"},
    trigger=config.PUBLIC_TRIGGER, check_client=True,
    filter_me=False, allow_bots=False)
@vc_chat
@check_enable_for_all
async def shuffle_queue(msg: Message):
    if QUEUE:
        random.shuffle(QUEUE)
    await view_queue(msg)


@userge.on_cmd("stopvc", about={
    'header': "Stop vc and clear Queue.",
    'usage': "{tr}stopvc"})
@vc_chat
async def stop_music(msg: Message):
    """ stop music in vc """
    await msg.delete()
    await skip_song(True)
    await reply_text(msg, "`Stopped Userge-Music.`", del_in=5)


@VC_CLIENT.on_raw_update()
async def _on_raw(_, m: BaseMessage, *__) -> None:
    if isinstance(m, UpdateGroupCallParticipants):
        # TODO: chat_id
        for participant in m.participants:
            if participant.is_self:
                group_call = await VC_CLIENT.invoke(
                    GetGroupCall(call=InputGroupCall(
                        access_hash=m.call.access_hash,
                        id=m.call.id), limit=1)
                )
                if participant.just_joined:
                    await on_join(group_call.call)
                elif participant.left:
                    await on_left(group_call.call)
                break
    raise ContinuePropagation


@call.on_stream_end()
async def _stream_end_handler(_: PyTgCalls, update: Update):
    if isinstance(update, StreamAudioEnded):
        Dynamic.PLAYING = False
        await skip_song()


@call.on_participants_change()
async def _participants_change_handler(_: PyTgCalls, update: Update):
    if isinstance(update, JoinedGroupCallParticipant):
        GROUP_CALL_PARTICIPANTS.append(update.participant.user_id)
    elif isinstance(update, LeftGroupCallParticipant) \
            and update.participant.user_id in GROUP_CALL_PARTICIPANTS:
        GROUP_CALL_PARTICIPANTS.remove(update.participant.user_id)


if userge.has_bot:
    userge.bot.add_handler(
        CallbackQueryHandler(
            vc_callback,
            filters.regex("(skip|queue|back$)")
        )
    )
    userge.bot.add_handler(
        CallbackQueryHandler(
            vol_callback,
            filters.regex(r"vol\((.+)\)")
        )
    )
    userge.bot.add_handler(
        CallbackQueryHandler(
            vc_control_callback,
            filters.regex("(player|seek|rewind|replay)")
        )
    )
