import os
import re
import shlex
import asyncio

from userge import userge, Message, Config
from userge.utils import progress


@userge.on_cmd("web ?(.+?|) (anonfiles|transfer|filebin|anonymousfiles"
               "|megaupload|bayfiles|vshare|0x0|fileio)",
               about={
                   'header': "upload files to web",
                   'usage': "{tr}web [site name]",
                   'types': [
                       'anonfiles', 'transfer', 'filebin', 'anonymousfiles',
                       'megaupload', 'bayfiles', 'vshare', '0x0', 'fileio']})
async def web(message: Message):
    await message.edit("`Processing ...`")
    input_str = message.matches[0].group(1)
    selected_transfer = message.matches[0].group(2).lower()
    if input_str:
        file_name = input_str
    else:
        file_name = await message.client.download_media(
            message=message.reply_to_message,
            file_name=Config.DOWN_PATH,
            progress=progress,
            progress_args=(message, "trying to download")
        )
        if message.process_is_canceled:
            await message.err("Process Canceled!")
            return
    hosts = {
        "anonfiles": "curl -F \"file=@{}\" https://anonfiles.com/api/upload",
        "transfer": "curl --upload-file \"{}\" https://transfer.sh/" + os.path.basename(file_name),
        "filebin": "curl -X POST --data-binary \"@test.png\" -H \"filename"
                   ": {}\" \"https://filebin.net\"",
        "anonymousfiles": "curl -F file=\"@{}\" https://api.anonymousfiles.io/",
        "megaupload": "curl -F \"file=@{}\" https://megaupload.is/api/upload",
        "bayfiles": "curl -F \"file=@{}\" https://api.bayfiles.com/upload",
        "vshare": "curl -F \"file=@{}\" https://api.vshare.is/upload",
        "0x0": "curl -F \"file=@{}\" https://0x0.st",
        "fileio": "curl -F \"file =@{}\" https://file.io"
    }
    cmd = hosts[selected_transfer].format(file_name)
    await message.edit(f"`now uploading to {selected_transfer} ...`")
    process = await asyncio.create_subprocess_exec(
        *shlex.split(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    response, err = await process.communicate()
    links = '\n'.join(re.findall(r'https?://[^\"\']+', response.decode()))
    if links:
        await message.edit(f"**I found these links** :\n{links}")
    else:
        await message.edit('`' + response.decode() + err.decode() + '`')
