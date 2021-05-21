"""PM Logger"""

# Copyright (C) 2020 BY USERGE-X
# All rights reserved.
# Author : GitHub.com/code-rgb [TG - @deleteduser420]


import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait, MessageIdInvalid

from userge import Config, Message, get_collection, userge
from userge.utils import mention_html

SAVED_SETTINGS = get_collection("CONFIGS")
ALLOWED_COLLECTION = get_collection("PM_PERMIT")
NO_PM_LOG = get_collection("NO_PM_LOG")

PM_LOGGER_CACHE = {}


async def _init() -> None:
    data = await SAVED_SETTINGS.find_one({"_id": "PM_LOGGING"})
    if data:
        Config.PM_LOGGING = bool(data["is_active"])


allowPmLoggingFilter = filters.create(lambda _, __, ___: Config.PM_LOGGING)
allowAllFilter = filters.create(lambda _, __, ___: Config.ALLOW_ALL_PMS)


@userge.on_cmd(
    "pm_logger",
    about={
        "header": "enable / disable PM Logger\n\n"
        "Note: Pm logging will only work if Pm Gaurd is Enabled"
    },
    allow_channels=False,
)
async def pm_logger_(message: Message):
    """enable / disable PM Logger"""
    if not Config.PM_LOG_GROUP_ID:
        return await message.edit(
            "Make a Group and add it's ID in Heroku," "\n Var: '`PM_LOG_GROUP_ID`' ",
            del_in=5,
        )
    if Config.PM_LOGGING:
        Config.PM_LOGGING = False
        await message.edit("`PM Logger disabled !`", del_in=3)
    else:
        Config.PM_LOGGING = True
        await message.edit("`PM Logger enabled !`", del_in=3)
    await SAVED_SETTINGS.update_one(
        {"_id": "PM_LOGGING"}, {"$set": {"is_active": Config.PM_LOGGING}}, upsert=True
    )


@userge.on_message(
    filters.private
    & filters.incoming
    & ~filters.me
    & ~filters.user(Config.TG_IDS)
    & ~filters.service
    & ~filters.bot
    & ~filters.edited
    & ~allowAllFilter
    & allowPmLoggingFilter,
    group=2,
)
async def pm_logger(_, message: Message):
    u_id = message.from_user.id
    u_name = message.from_user.first_name
    found = await NO_PM_LOG.find_one({"user_id": u_id})
    if found:
        return
    pm_logger_msg = "<b><i>ID</i></b> : <code>{}</code>\n👤 {} sent"
    new_pm_logger = pm_logger_msg + " a new message."
    if len(PM_LOGGER_CACHE) == 0:  # First Pm
        logger_msg_count = await userge.send_message(
            Config.PM_LOG_GROUP_ID,
            new_pm_logger.format(u_id, mention_html(u_id, u_name)),
            disable_notification=True,
        )
        PM_LOGGER_CACHE[u_id] = {
            "name": u_name,
            "msg_count": 1,
            "logger_msg_id": logger_msg_count.message_id,
        }
    # either it can be the same user or a new user
    elif len(PM_LOGGER_CACHE) == 1:
        if u_id in PM_LOGGER_CACHE:  # if same person just updating the count
            PM_LOGGER_CACHE[u_id]["msg_count"] += 1
        else:
            u_info_id = list(PM_LOGGER_CACHE)[0]
            u_mention = mention_html(u_info_id, PM_LOGGER_CACHE[u_info_id]["name"])
            edit_pm_logger = pm_logger_msg + " <code>{}</code> messages."
            try:
                await userge.edit_message_text(
                    Config.PM_LOG_GROUP_ID,
                    PM_LOGGER_CACHE[u_info_id]["logger_msg_id"],
                    edit_pm_logger.format(
                        u_info_id, u_mention, PM_LOGGER_CACHE[u_info_id]["msg_count"]
                    ),
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)

            PM_LOGGER_CACHE.clear()
            try:
                logger_msg_count = await userge.send_message(
                    Config.PM_LOG_GROUP_ID,
                    new_pm_logger.format(u_id, mention_html(u_id, u_name)),
                    disable_notification=True,
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            PM_LOGGER_CACHE[u_id] = {
                "name": u_name,
                "msg_count": 1,
                "logger_msg_id": logger_msg_count.message_id,
            }
    else:  # Just in Case
        PM_LOGGER_CACHE.clear()
    try:
        await message.forward(Config.PM_LOG_GROUP_ID, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
    except MessageIdInvalid:
        pass


@userge.on_cmd(
    "pmlog",
    about={
        "header": "Enable / Disable PM Logging For a specific User",
        "description": "Stop logging incomming pms from a user"
        " USERGE-X will not interfere or handle such private chats",
        "usage": "{tr}pmlog [username | userID]\nreply {tr}pmlog to a message,"
        " do {tr}pmlog in the private chat",
    },
    allow_channels=False,
    allow_via_bot=False,
)
async def pm_user_log_(message: Message):
    """disable pm logger for a user"""
    user_id = await get_id(message)
    if not user_id:
        return await message.err("See Help", del_in=5)
    user_data = await userge.get_user_dict(user_id)
    found = await NO_PM_LOG.find_one({"user_id": user_id})
    if found:
        await asyncio.gather(
            NO_PM_LOG.delete_one({"user_id": user_id}),
            message.edit(
                f"Now Logging PM for user: {user_data['mention']}",
                del_in=3,
                log=__name__,
            ),
        )
        return
    await asyncio.gather(
        NO_PM_LOG.insert_one(
            {
                "firstname": user_data["fname"],
                "user_id": user_id,
            }
        ),
        message.edit(
            f"PM Logging turned off for user: {user_data['mention']}",
            del_in=3,
            log=__name__,
        ),
    )


@userge.on_cmd(
    "pmloglist",
    about={
        "header": "Get a List of Users Excluded from PM Logging",
        "examples": "{tr}pmloglist",
    },
    allow_channels=False,
)
async def list_no_pm_log_users(message: Message):
    """pm log user list"""
    msg = ""
    async for c in NO_PM_LOG.find():
        msg += (
            "**User** : "
            + str(c["firstname"])
            + "-> with **User ID** -> "
            + str(c["user_id"])
            + "\n\n"
        )

    await message.edit_or_send_as_file(
        ("**PM Logging Disabled For :**\n\n" + msg) if msg else "`Logging All PMS`"
    )


async def get_id(message: Message, userid=None):
    if message.chat.type in ["private", "bot"]:
        userid = message.chat.id
    if message.reply_to_message:
        userid = message.reply_to_message.from_user.id
    if message.input_str:
        user = message.input_str.lstrip("@")
        try:
            userid = (await userge.get_users(user)).id
        except Exception as e:
            await message.err(str(e))
    return userid
