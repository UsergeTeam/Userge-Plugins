import os
import shutil
import deezloader
from userge import userge, Message

ARL_TOKEN = os.environ.get("ARL_TOKEN", None)
PATH = 'deezdown_temp/'


@userge.on_cmd("deezload", about={
    'header': "Name's Deez, DeezLoader",
    'description': "Download Songs/Albums/Playlists via "
                   "Sopitfy or Deezer Links. "
                   "\n**NOTE:** Music Quality is optional",
    'flags': {'-stl': "Download a Track via Spotify Link",
              '-dtl': "Download a Track via Deezer Link",
              '-sal': "Download an Album via Spotify Link",
              '-dal': "Download an Album via Deezer Link",
              '-spl': "Download a Playlist via Spotify Link",
              '-dpl': "Download a Playlist via Deezer Link",
              '-dsong': "Download a Song by passing Artist Name and Song Name",
              '-zip': "Get a zip archive for Albums/Playlist Download"},
    'options': "Available Sound Quality: `FLAC` | `MP3_320` | `MP3_256` | `MP3_128`",
    'usage': "{tr}deezload [flag] [link | quality (default MP3_320)]",
    'examples': "{tr}deezload -dtl https://www.deezer.com/track/142750222 \n"
                "{tr}deezload -dtl https://www.deezer.com/track/3824710 FLAC \n"
                "{tr}deezload -dal https://www.deezer.com/album/1240787 FLAC \n"
                "{tr}deezload -dal -zip https://www.deezer.com/album/1240787 \n"
                "{tr}deezload -dsong Ed Sheeran - Shape of You - MP3_256 (quality is optional)"})
async def deezload(message: Message):
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    if not message.flags:
        await message.edit(
            "Check your E-Mail📧 I've sent an invitation to read help for DeezLoader :)")
        return
    await message.edit("Trying to Login 🥴")
    if ARL_TOKEN is None:
        await message.edit(
            "Oops, Time to Help Yourself "
            "\n[Here Help Yourself](https://www.google.com/search?q=how+to+get+deezer+arl+token)"
            "\nAfter getting Arl token Config `ARL_TOKEN` var in heroku"
        )
        return
    try:
        loader = deezloader.Login(ARL_TOKEN)
    except Exception as er:
        await message.edit(er)
        return

    flags = list(message.flags)
    if '-zip' not in flags:
        to_zip = False
    else:
        to_zip = True
    d_quality = "MP3_320"
    if not message.filtered_input_str:
        await message.edit("Bruh, Now I Think how far should we go. Plz Terminate my Session 🥺")
        return
    input_ = message.filtered_input_str
    if '-dsong' not in flags:
        try:
            input_link, quality = input_.split()
        except ValueError:
            if len(input_.split()) == 1:
                input_link = input_
                quality = d_quality
            else:
                await message.edit("🤔 Comedy? You are good at it")
                return
        if '.com' not in input_link:
            await message.edit("Invalid Link")
            return
    elif '-dsong' in flags:
        try:
            artist, song, quality = input_.split('-')
        except ValueError:
            if len(input_.split("-")) == 2:
                artist, song = input_.split('-')
                quality = d_quality
            else:
                await message.edit("WeW, Use that thing which is present on top floor of ur body 🌚")
                return

    if '-stl' in flags:
        await message.edit("Trying to download song via Spotify Link 🥴")
        track = loader.download_trackspo(
            input_link,
            output=PATH,
            quality=quality,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        await message.edit("Now Uploading 📤")
        await userge.send_audio(
            chat_id=message.chat.id,
            audio=track
        )
    elif '-dtl' in flags:
        await message.edit("trying to download song via Deezer Link 🥴")
        track = loader.download_trackdee(
            input_link,
            output=PATH,
            quality=quality,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        await message.edit("Now Uploading 📤")
        await userge.send_audio(
            chat_id=message.chat.id,
            audio=track
        )

    if '-sal' in flags:
        await message.edit("Trying to download album 🤧")
        if to_zip:
            _, zip_ = loader.download_albumspo(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Sending as Zip File 🗜")
            await userge.send_document(
                chat_id=message.chat.id,
                document=zip_
            )
        else:
            album_list = loader.download_albumspo(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip)
            await message.edit("Uploading Tracks 📤")
            for tracks in album_list:
                await userge.send_audio(
                    chat_id=message.chat.id,
                    audio=tracks
                )
    elif '-dal' in flags:
        await message.edit("Trying to download album 🤧")
        if to_zip:
            _, zip_ = loader.download_albumdee(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Uploading as Zip File 🗜")
            await userge.send_document(
                chat_id=message.chat.id,
                document=zip_
            )
        else:
            album_list = loader.download_albumdee(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Uploading Tracks 📤")
            for tracks in album_list:
                await userge.send_audio(
                    chat_id=message.chat.id,
                    audio=tracks
                )

    if '-spl' in flags:
        await message.edit("Trying to download Playlist 🎶")
        if to_zip:
            _, zip_ = loader.download_playlistspo(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Sending as Zip 🗜")
            await userge.send_document(
                chat_id=message.chat.id,
                document=zip_
            )
        else:
            album_list = loader.download_playlistspo(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Uploading Tracks 📤")
            for tracks in album_list:
                await userge.send_audio(
                    chat_id=message.chat.id,
                    audio=tracks
                )
    elif '-dpl' in flags:
        await message.edit("Trying to download Playlist 🎶")
        if to_zip:
            _, zip_ = loader.download_playlistdee(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Sending as Zip File 🗜")
            await userge.send_document(
                chat_id=message.chat.id,
                document=zip_
            )
        else:
            album_list = loader.download_playlistdee(
                input_link,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=to_zip
            )
            await message.edit("Uploading Tracks 📤")
            for tracks in album_list:
                await userge.send_audio(
                    chat_id=message.chat.id,
                    audio=tracks
                )

    if '-dsong' in flags:
        await message.edit("Searching for Song 🔍")
        try:
            track = loader.download_name(
                artist=artist,
                song=song,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True
            )
            await message.edit("Song found, Now Uploading 📤")
            await userge.send_audio(
                chat_id=message.chat.id,
                audio=track
            )
        except:
            await message.edit("Song not Found 🚫")
    await message.delete()
    shutil.rmtree(PATH, ignore_errors=True)
