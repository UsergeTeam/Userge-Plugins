import os
from userge import userge, Message
from lyrics_extractor import Song_Lyrics

GCS_ENGINE_ID = os.environ.get("GCS_ENGINE_ID", None) 
GCS_API_KEY = os.environ.get("GCS_API_KEY", None)

@userge.on_cmd("glyrics", about={
    'header': "GCS Lyrics",
    'description': "Scrape Song Lyrics from various websites"
                   " using your Custom Search Engine.",
    'usage': "{tr}glyrics [Song Name]",
    'examples': "`{tr}glyrics Swalla Nicki Minaj`"})
async def glyrics(message: Message):
    if (GCS_ENGINE_ID and GCS_API_KEY) is None:
        await message.edit(
            "**Requirements Missing**\n\n"
            "Please Configure `GCS_ENGINE_ID` & `GCS_API_KEY`\n\n"
            "**More Info on How to Configure:**\n"
            "[NOTE: Read all Steps First, Coz No one's gonna help ya]\n"
            "1. Create your new Custom Search Engine here to get your Engine ID: "
            "https://cse.google.com/cse/create/new"
            "2. Add any of the following or all (adding all is recommended) "
            "websites as per your choice in your Custom Search Engine:\n"
            " » `https://genius.com/` \n"
            " » `http://www.lyricsted.com/` \n"
            " » `http://www.lyricsbell.com/` \n"
            " » `https://www.glamsham.com/` \n"
            " » `http://www.lyricsoff.com/` \n"
            " » `http://www.lyricsmint.com/` \n"
            "**NOTE:** Please **don't turn on** the '**Search the entire Web**'"
            " feature as it is currently not possible to scrape from any random"
            " sites appearing in the search results.\n"
            "3. Visit here to get your API key: https://developers.google.com/custom-search/v1/overview"
            "\n4. Finally Add following in Heroku Config vars:\n"
            "**Key:** `GCS_ENGINE_ID` \n**Value:** Engine ID of CSE (got in Step 1)\n"
            "**Key:** `GCS_API_KEY`\n**Value:** API Token (got in Step 3)")
        return

    if not message.input_str:
        await message.edit("Give Song Name Peru Uzer")
        return

    song = message.input_str
    try:
        gcsl = Song_Lyrics(GCS_API_KEY, GCS_ENGINE_ID)
        song_title, song_lyrics = gcsl.get_lyrics(song)
        if song_lyrics:
            out = f"**Here is {song_title}**\n\n\n__{song_lyrics}__"
        else:
            out = f"**{song_title}**\n ┐(´д｀)┌"
        await message.edit(out)
    except Exception as e:
        await message.err(e)
