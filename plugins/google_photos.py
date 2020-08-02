#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Telegram UseRGE
#  Copyright (C) 2020 @UniBorg
#
# 0) original: https://github.com/SpEcHiDe/UniBorg/raw/master/stdplugins/google_photos.py
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!


"""Google Photos
"""

import os
import asyncio
from mimetypes import guess_type

import aiohttp
import aiofiles
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client

from userge import userge, Message, Config
from userge.utils import progress


# setup the gPhotos v1 API
OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/photoslibrary",
    "https://www.googleapis.com/auth/photoslibrary.sharing"
]
# Redirect URI for installed apps, can be left as is
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
#
PHOTOS_BASE_URI = "https://photoslibrary.googleapis.com"
G_PHOTOS_CLIENT_ID = os.environ.get("G_PHOTOS_CLIENT_ID", None)
G_PHOTOS_CLIENT_SECRET = os.environ.get("G_PHOTOS_CLIENT_SECRET", None)
TOKEN_FILE_NAME = os.path.join(Config.DOWN_PATH, "gPhoto_credentials_UniBorg.json")
LOG = userge.getLogger(__name__)  # logger object
CHANNEL = userge.getCLogger(__name__)  # channel logger object
G_PHOTOS_AUTH_TOKEN_ID = int(os.environ.get("G_PHOTOS_AUTH_TOKEN_ID", 0))


@userge.on_cmd("gphoto setup", about="no one gonna help you 🤣🤣🤣🤣",
               allow_groups=False, allow_channels=False)
async def setup_google_photos(message: Message):
    creds = await check_creds(message)
    if not creds:
        await create_token_file(message)
        await CHANNEL.log("#GPHOTOS #setup #completed")
        await message.edit("CREDS created. 😕😖😖")
    else:
        await message.edit("CREDS already created. 😕")


async def create_token_file(message):
    # Run through the OAuth flow and retrieve credentials
    flow = client.OAuth2WebServerFlow(
        G_PHOTOS_CLIENT_ID,
        G_PHOTOS_CLIENT_SECRET,
        OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI
    )
    authorize_url = flow.step1_get_authorize_url()
    async with userge.conversation(message.chat.id, timeout=60) as conv:
        await conv.send_message(
            "Go to the following link in "
            f"your browser: {authorize_url} and reply the code"
        )
        response = await conv.get_response(mark_read=True)
        # LOG.info(response.stringify())
        code = response.text.strip()
        credentials = flow.step2_exchange(code)
        storage = file.Storage(TOKEN_FILE_NAME)
        storage.put(credentials)
        imp_gsem = await conv.send_document(document=TOKEN_FILE_NAME)
        await imp_gsem.reply_text(
            "please set <code>G_PHOTOS_AUTH_TOKEN_ID</code> = "
            f"<u>{imp_gsem.message_id}</u> ..!"
            "\n\n<i>This is only required, "
            "if you are running in an ephimeral file-system</i>.",
            parse_mode="html"
        )
        return storage


async def check_creds(message):
    if G_PHOTOS_AUTH_TOKEN_ID:
        confidential_message = await message.client.get_messages(
            chat_id=Config.LOG_CHANNEL_ID,
            message_ids=G_PHOTOS_AUTH_TOKEN_ID,
            replies=0
        )
        if confidential_message and confidential_message.document:
            await confidential_message.download(file_name=TOKEN_FILE_NAME)
    if os.path.exists(TOKEN_FILE_NAME):
        pho_storage = file.Storage(TOKEN_FILE_NAME)
        creds = pho_storage.get()
        if not creds or creds.invalid:
            return None
        creds.refresh(Http())
        return creds
    return None


@userge.on_cmd("gphoto upload", about="no one gonna help you 🤣🤣🤣🤣")
async def upload_google_photos(message: Message):
    if not message.reply_to_message:
        await message.edit_text(
            "©️ <b>[Forwarded from utubebot]</b>\nno one gonna help you 🤣🤣🤣🤣", parse_mode="html")
        return
    creds = await check_creds(message)
    if not creds:
        await message.edit_text("😏 <code>gphoto setup</code> first 😡😒😒", parse_mode="html")
        return
    await message.edit("`proccesing ...`")
    service = build("photoslibrary", "v1", http=creds.authorize(Http()))
    # create directory if not exists
    if not os.path.isdir(Config.DOWN_PATH):
        os.makedirs(Config.DOWN_PATH)
    file_path = None
    vid = await message.reply_to_message.download(
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(message, "downloading🧐?")
    )
    file_path = os.path.join(Config.DOWN_PATH, os.path.basename(vid))
    # LOG.info(file_path)
    if not file_path:
        await message.edit_text("<b>[stop spamming]</b>", parse_mode="html")
        return
    file_name, mime_type, file_size = file_ops(file_path)
    await message.edit_text("file downloaded, gathering upload informations ")
    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Length": "0",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Content-Type": mime_type,
            "X-Goog-Upload-File-Name": file_name,
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Raw-Size": str(file_size),
            "Authorization": "Bearer " + creds.access_token,
        }
        # Step 1: Initiating an upload session
        step_one_response = await session.post(f"{PHOTOS_BASE_URI}/v1/uploads", headers=headers)
        if step_one_response.status != 200:
            await message.edit_text((await step_one_response.text()))
            return
        step_one_resp_headers = step_one_response.headers
        # LOG.info(step_one_resp_headers)
        # Step 2: Saving the session URL
        real_upload_url = step_one_resp_headers.get("X-Goog-Upload-URL")
        # LOG.info(real_upload_url)
        upload_granularity = int(step_one_resp_headers.get("X-Goog-Upload-Chunk-Granularity"))
        # LOG.info(upload_granularity)
        # https://t.me/c/1279877202/74
        number_of_req_s = int(file_size / upload_granularity)
        # LOG.info(number_of_req_s)
        loop = asyncio.get_event_loop()
        async with aiofiles.open(file_path, mode="rb") as f_d:
            for i in range(number_of_req_s):
                current_chunk = await f_d.read(upload_granularity)
                offset = i * upload_granularity
                part_size = len(current_chunk)
                headers = {
                    "Content-Length": str(part_size),
                    "X-Goog-Upload-Command": "upload",
                    "X-Goog-Upload-Offset": str(offset),
                    "Authorization": "Bearer " + creds.access_token,
                }
                # LOG.info(i)
                # LOG.info(headers)
                response = await session.post(real_upload_url, headers=headers, data=current_chunk)
                loop.create_task(progress(offset + part_size, file_size,
                                          message, "uploading(gphoto)🧐?"))
                # LOG.info(response.headers)
                # https://github.com/SpEcHiDe/UniBorg/commit/8267811b1248c00cd1e34041e2ae8c82b207970f
                # await f_d.seek(upload_granularity)
            # await f_d.seek(upload_granularity)
            current_chunk = await f_d.read(upload_granularity)
            # https://t.me/c/1279877202/74
            # LOG.info(number_of_req_s)
            headers = {
                "Content-Length": str(len(current_chunk)),
                "X-Goog-Upload-Command": "upload, finalize",
                "X-Goog-Upload-Offset": str(number_of_req_s * upload_granularity),
                "Authorization": "Bearer " + creds.access_token,
            }
            # LOG.info(headers)
            response = await session.post(real_upload_url, headers=headers, data=current_chunk)
            # LOG.info(response.headers)
        final_response_text = await response.text()
        # LOG.info(final_response_text)
    await message.edit_text("uploaded to Google Photos, getting FILE URI 🤔🤔")
    response_create_album = service.mediaItems().batchCreate(
        body={
            "newMediaItems": [{
                "description": "uploaded using @UniBorg v7",
                "simpleMediaItem": {
                    "fileName": file_name,
                    "uploadToken": final_response_text
                }
            }]
        }
    ).execute()
    # LOG.info(response_create_album)
    try:
        photo_url = response_create_album.get(
            "newMediaItemResults")[0].get("mediaItem").get("productUrl")
        await message.edit_text(photo_url)
    except Exception as e:  # pylint: disable=broad-except
        await message.edit_text(str(e))


# Get mime type and name of given file
def file_ops(file_path):
    file_size = os.stat(file_path).st_size
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type, file_size
