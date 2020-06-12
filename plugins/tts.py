import os
from gtts import gTTS
from hachoir.metadata import extractMetadata as XMan
from hachoir.parser import createParser as CPR

from userge import userge, Message


@userge.on_cmd("tts", about={
    'header': "Text To Speech",
    'examples': "{tr}tts en|Userge"})
async def text_to_speech(message: Message):
    req_file_name = "gtts.mp3"
    inp_text = message.input_str
    if ("|" not in inp_text) or not inp_text:
        await message.edit("Pathetic")
        return
    await message.edit("Processing.")
    def_lang = "en"
    def_lang, text = inp_text.split("|")
    try:
        await message.edit("Processing..")
        speeched = gTTS(text, lang=def_lang.strip())
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
