""" Mentions alerter Plugin """

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import PeerIdInvalid
from userge import userge, Message, Config, filters, get_collection

SAVED_SETTINGS = get_collection("CONFIGS")
TOGGLE = False


async def _init():
    global TOGGLE  # pylint: disable=global-statement
    if data:= await SAVED_SETTINGS.find_one({"_id": "MENTION_TOGGLE"}):
        TOGGLE = bool(data["data"])


@userge.on_cmd(
    "mentions",
    about="Toggles Mentions, "
          "if enabled Bot will send Message if anyone mention you."
)
async def toggle_mentions(msg: Message):
    """ toggle mentions """
    global TOGGLE  # pylint: disable=global-statement
    if TOGGLE:
        TOGGLE = False
    else:
        TOGGLE = True
    await SAVED_SETTINGS.update_one(
        {"_id": "MENTION_TOGGLE"}, {"$set": {"data": TOGGLE}}, upsert=True
    )
    await msg.edit(f"Mentions Alerter **{'enabled' if TOGGLE else 'disabled'}** Successfully.")


@userge.on_filters(
    ~filters.me & ~filters.bot & ~filters.edited & ~filters.service
    & (filters.mentioned | filters.private), group=1, allow_via_bot=False)
async def handle_mentions(msg: Message):

    if TOGGLE is False:
        return

    if not msg.from_user or msg.from_user.is_verified:
        return

    if msg.chat.type == "private":
        link = f"tg://openmessage?user_id={msg.chat.id}&message_id={msg.message_id}"
        text = f"{msg.from_user.mention} 💻 sent you a **Private message.**"
    else:
        link = msg.link
        text = f"{msg.from_user.mention} 💻 tagged you in **{msg.chat.title}.**"
    text += f"\n\n[Message]({link}):" if not userge.has_bot else "\n\n**Message:**"
    if msg.text:
        text += f"\n`{msg.text}`"

    button = InlineKeyboardButton(text="📃 Message Link", url=link)

    client = userge.bot if userge.has_bot else userge
    try:
        await client.send_message(
            chat_id=userge.id if userge.has_bot else Config.LOG_CHANNEL_ID,
            text=text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[button]])
        )
    except PeerIdInvalid:
        if userge.dual_mode:
            await userge.send_message(userge.id, "/start")
            await client.send_message(
                chat_id=userge.id if userge.has_bot else Config.LOG_CHANNEL_ID,
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        else:
            raise
