import asyncio
from userge import userge, Message
from PyLyrics import *


@userge.on_cmd("lyrics", about={
    'header': "Get Lyrics of a Song",
    'usage': "{tr}lyrics Singer Name - Song Name",
    'examples': "{tr}lyrics ROXXANNE - Arizona Zervas"})
async def lyrics(message: Message):
    i = 0

    args = message.input_str
    if not args:
        await message.edit("Bruh, Give some input.\nDo .help lyrics plox")
    try:
        song = args.split("-")
        if len(song) == 1:
            await message.edit("Do .help lyrics")
        else:
            await message.edit("ðï¸Searching lyrics")
            lyrics = PyLyrics.getLyrics(song[0].strip(), song[1].strip()).split("\n")
            lyric_message = f"Lyrics {song[0].strip()} from {song[1].strip()} ð"
            lyric_message += "\n\n" + "\n".join(lyrics)
            try:
                await message.edit_or_send_as_file(lyric_message)
            except Exception as e:
                 LOG.exception('Received exception during gbannedList')
                 await message.edit("Error: "+str(e))
    except ValueError:
        await message.edit("Song not found")
