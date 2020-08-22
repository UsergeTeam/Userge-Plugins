""" ASCII Sticker """

# Copyright 2017, Shanshan Wang, MIT license
# (C) Author: Krishna-Singhal < https://github.com/krishna-singhal >  <@Krishna_Singhal>
#
# All Rights Reserved.

import os
import numpy as np
import random

from PIL import Image, ImageFont, ImageDraw
from colour import Color

from userge.utils import take_screen_shot, runcmd

from userge import userge, Config, Message


@userge.on_cmd("ascii", about={
    'header': "Reply media to convert Ascii Sticker",
    'usage': " {tr}ascii [reply to media]"})
async def ascii_(message: Message):
    """ Convert media to ascii sticker """
    replied = message.reply_to_message
    if not (replied and (
            replied.photo or replied.sticker or replied.video or replied.animation)):
        await message.edit("```Media not found...```")
        await message.reply_sticker('CAADBQADVAUAAjZgsCGE7PH3Wt1wSRYE')
        return
    if not os.path.isdir(Config.DOWN_PATH):
        os.makedirs(Config.DOWN_PATH)
    await message.edit("```Let me Convert your media...```")
    dls = await message.client.download_media(
        replied,
        file_name=Config.DOWN_PATH)
    dls_loc = os.path.join(Config.DOWN_PATH, os.path.basename(dls))
    ascii_file = None
    if replied.sticker and replied.sticker.file_name.endswith(".tgs"):
        file_1 = os.path.join(Config.DOWN_PATH, "ascii.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {file_1}"
        stdout, stderr = (await runcmd(cmd))[:2]
        if not os.path.lexists(file_1):
            await message.err("```Sticker not found...```")
            raise Exception(stdout + stderr)
        ascii_file = file_1
    elif replied.animation or replied.video:
        file_2 = os.path.join(Config.DOWN_PATH, "ascii.png")
        await take_screen_shot(dls_loc, 0, file_2)
        if not os.path.lexists(file_2):
            await message.err("```Sticker not found...```")
            return
        ascii_file = file_2
    if ascii_file is None:
        ascii_file = dls_loc
    c_list = random_color()
    color1 = c_list[0]
    color2 = c_list[1]
    bgcolor = "black"
    converted = Config.DOWN_PATH + "ascii.webp"
    asciiart_(ascii_file, 0.1, 1.8, converted, color1, color2, bgcolor)
    await message.client.send_sticker(
        message.chat.id,
        converted,
        reply_to_message_id=replied.message_id)
    await message.delete()
    for files in (dls_loc, ascii_file, converted):
        if files and os.path.exists(files):
            os.remove(files)


def asciiart_(in_f, SC, GCF, out_f, color1, color2, bgcolor):

    chars = np.asarray(list(' .,:irs?@9B&#'))
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    WCF = letter_height / letter_width

    img = Image.open(in_f)

    widthByLetter = round(img.size[0] * SC * WCF)
    heightByLetter = round(img.size[1] * SC)

    S = (widthByLetter, heightByLetter)
    img = img.resize(S)
    img = np.sum(np.asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max())**GCF * (chars.size - 1)

    lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")

    nbins = len(lines)
    colorRange = list(Color(color1).range_to(Color(color2), nbins))

    newImg_width = letter_width * widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
    draw = ImageDraw.Draw(newImg)

    leftpadding = 0
    y = 0
    lineIdx = 0
    for line in lines:
        color = colorRange[lineIdx]
        lineIdx += 1
        draw.text((leftpadding, y), line, color.hex, font=font)
        y += letter_height

    ASCII_FILE = newImg.save(out_f)
    return ASCII_FILE


def random_color():
    color = ["#" + ''.join([
        random.choice('0123456789ABCDEF') for k in range(6)]) for i in range(2)]
    return color
