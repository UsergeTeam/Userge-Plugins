import os

from hachoir.metadata import extractMetadata as XMan
from hachoir.parser import createParser as CPR
from gtts import gTTS

from userge import userge, Message


@userge.on_cmd("tts", about={
    'header': "Text To Speech",
    'examples': [
        "{tr}tts Userge", "{tr}tts en | Userge", "{tr}tts [reply to message]"
    ]
})
async def text_to_speech(message: Message):
    req_file_name = "gtts.mp3"
    replied = message.reply_to_message
    def_lang = "en"
    if replied and replied.text:
        text = replied.text
        if message.input_str:
            def_lang = message.input_str
    elif message.input_str:
        if '|' in message.input_str:
            def_lang, text = message.input_str.split("|", maxsplit=1)
        else:
            text = message.input_str
    else:
        return await message.err("Input not found!")
    await message.edit("Processing.")
    try:
        await message.edit("Processing..")
        speeched = gTTS(text.strip(), lang=def_lang.strip())
        speeched.save(req_file_name)
        await message.edit("Processing...")
        meta = XMan(CPR(req_file_name))
        a_len = 0
        a_title = "Text To Speech"
        a_perf = "Google"
        a_cap = f"Language Code: {def_lang}"
        if meta and meta.has("duration"):
            a_len = meta.get("duration").seconds
        await message.edit("Uploading...")
        await message.reply_audio(
            audio=req_file_name,
            caption=a_cap,
            duration=a_len,
            performer=a_perf,
            title=a_title
        )
        os.remove(req_file_name)
        await message.delete()
    except Exception as err:
        await message.edit(err)
