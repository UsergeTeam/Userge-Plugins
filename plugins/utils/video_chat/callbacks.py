import re

from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            CallbackQuery,
                            Message as RawMessage)
from pyrogram.errors import MessageNotModified, QueryIdInvalid

from userge import userge, filters, config
from userge.utils.exceptions import StopConversation
from . import call, CQ_MSG, QUEUE, Vars
from .resource import TgResource
from .utils import (check_cq_for_all,
                    default_markup,
                    get_player_string)
from .helpers import skip_song, replay_music, seek_music


@check_cq_for_all
async def vc_callback(cq: CallbackQuery):
    await cq.answer()
    if not Vars.CHAT_NAME:
        await cq.edit_message_text("`Already Left Video-Chat`")
        return

    if "skip" in cq.data:
        text = f"{cq.from_user.mention} Skipped the Song."
        pattern = re.compile(r'\[(.*)\]')
        name = None
        for match in pattern.finditer(Vars.BACK_BUTTON_TEXT):
            name = match.group(1)
            break
        if name:
            text = f"{cq.from_user.mention} Skipped `{name}`."

        if CQ_MSG:
            for i, msg in enumerate(CQ_MSG):
                if msg.id == cq.message.id:
                    CQ_MSG.pop(i)
                    break

        await cq.edit_message_text(text, disable_web_page_preview=True)
        await skip_song()

    elif "queue" in cq.data:
        if not QUEUE:
            out = "`Queue is empty.`"
        else:
            out = f"**{len(QUEUE)} Song"
            out += f"{'s' if len(QUEUE) > 1 else ''} in Queue:**\n"
            for i, r in enumerate(QUEUE, start=1):
                if len(out) > config.MAX_MESSAGE_LENGTH - 100:
                    out += ('\nQueue too Long, '
                            'can not display more songs because of telegram restrictions.')
                    break
                if isinstance(r, TgResource) and r.path:
                    out = f"\n{i}. {r}"
                elif isinstance(r, TgResource):
                    out += f"\n{i}. [{r}]({r.message.link})"
                else:
                    out += f"\n{i}. [{r}]({r.url})"

        out += f"\n\n**Clicked by:** {cq.from_user.mention}"
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="back")]]
        )

        await cq.edit_message_text(
            out,
            disable_web_page_preview=True,
            reply_markup=button
        )

    elif cq.data == "back":
        if Vars.BACK_BUTTON_TEXT:
            await cq.edit_message_text(
                Vars.BACK_BUTTON_TEXT,
                disable_web_page_preview=True,
                reply_markup=default_markup()
            )
        else:
            await cq.message.delete()


@check_cq_for_all
async def vol_callback(cq: CallbackQuery):
    await cq.answer()
    arg = cq.matches[0].group(1)
    volume = 0

    if arg.isnumeric():
        volume = int(arg)

    elif arg == "custom":

        try:
            async with userge.conversation(cq.message.chat.id, user_id=cq.from_user.id) as conv:
                await cq.edit_message_text("`Now Input Volume`")

                def _filter(_, __, m: RawMessage) -> bool:
                    r = m.reply_to_message
                    return r and r.id == cq.message.id

                response = await conv.get_response(mark_read=True,
                                                   filters=filters.create(_filter))
        except StopConversation:
            await cq.edit_message_text("No arguments passed!")
            return

        if response.text.isnumeric():
            volume = int(response.text)
        else:
            await cq.edit_message_text("`Invalid Arguments!`")
            return

    if 200 >= volume > 0:
        await call.change_volume_call(Vars.CHAT_ID, volume)
        await cq.edit_message_text(f"Successfully set volume to {volume}")
    else:
        await cq.edit_message_text("`Invalid Range!`")


@check_cq_for_all
async def vc_control_callback(cq: CallbackQuery):
    if not Vars.CHAT_NAME:
        await cq.answer()
        return await cq.edit_message_text("`Already Left Video-Chat`")

    if cq.data in ("seek", "rewind"):
        dur = 15 if cq.data == "seek" else -15
        seek = await seek_music(dur)
        try:
            if seek:
                await cq.answer(f'Seeked 15 sec {"forward" if dur > 0 else "backward"}')
            else:
                return await cq.answer(
                    'This stream is either live stream /'
                    'seeked duration exceeds duration of file.',
                    show_alert=True)
        except QueryIdInvalid:
            pass

    elif cq.data == "replay":
        replay = await replay_music()
        if replay:
            await cq.answer("Replaying song from beggining.")
        else:
            return await cq.answer('No song found to play!', show_alert=True)

    try:
        await cq.edit_message_reply_markup(InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=get_player_string(), callback_data='back')
                ],
                [
                    InlineKeyboardButton(text="⏪ Rewind", callback_data='rewind'),
                    InlineKeyboardButton(text="🔄 Replay", callback_data='replay'),
                    InlineKeyboardButton(text="⏩ Seek", callback_data='seek')
                ]
            ]
        )
        )
    except MessageNotModified:
        pass
