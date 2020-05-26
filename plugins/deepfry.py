import os
import time
import random

from PIL import Image, ImageEnhance, ImageOps

from userge import userge, Message, Config
from userge.utils import progress, take_screen_shot, runcmd


@userge.on_cmd("deepfry", about={
    'header': "Deep Fryer",
    'description': "Well deepfy any image/sticker/gif and make it look ugly",
    'usage': "{tr}deepfry [fry count] as a reply.",
    'examples': "{tr}deepfry 1"})
async def deepfryer(message: Message):
    replied = message.reply_to_message
    if not (replied or message.input_str):
        await message.err("LMAO no one's gonna help you, if u use .help now then u **Gey**")
        await message.reply_sticker(sticker="CAADAQADhAAD3gkwRviGxMVn5813FgQ")
        return
    if not (replied.photo or replied.sticker or replied.animation):
        await message.err("Bruh, U Comedy me? Can you deepfry rocks?")
        return
    try:
        fry_c = int(message.input_str)
    except ValueError:
        fry_c = 1
    if not os.path.isdir(Config.DOWN_PATH):
        os.makedirs(Config.DOWN_PATH)
    await message.edit("*turns on fryer*")
    c_time = time.time()
    dls = await userge.download_media(
        message=message.reply_to_message,
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(
            "Lemme add some seasonings", userge, message, c_time
        )
    )
    dls_loc = os.path.join(Config.DOWN_PATH, os.path.basename(dls))
    if replied.sticker and replied.sticker.file_name.endswith(".tgs"):
        await message.edit("wait fryer is cold naw")
        png_file = os.path.join(Config.DOWN_PATH, "meme.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {png_file}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(dls_loc)
        if not os.path.lexists(png_file):
            await message.err("*boom* fryer exploded, can't deepfry this")
            raise Exception(stdout + stderr)
        dls_loc = png_file
    elif replied.animation:
        await message.edit("wait putting some more oil in fryer")
        jpg_file = os.path.join(Config.DOWN_PATH, "meme.jpg")
        await take_screen_shot(dls_loc, 0, jpg_file)
        os.remove(dls_loc)
        if not os.path.lexists(jpg_file):
            await message.err("someone took my oil can't deepfry it.")
            return
        dls_loc = jpg_file

    await message.edit("time to put this in fryer 🔥")
    fried_file = await deepfry(dls_loc)
    if fry_c > 1:
        for _ in range(fry_c):
            fried_file = await deepfry(fried_file)

    await userge.send_photo(chat_id=message.chat.id,
                            photo=fried_file,
                            reply_to_message_id=replied.message_id)
    await message.delete()
    os.remove(fried_file)


async def deepfry(img):

    img = Image.open(img)
    colours = ((random.randint(50, 200), random.randint(40, 170),
                random.randint(40, 190)), (random.randint(190, 255),
                                           random.randint(170, 240),
                                           random.randint(180, 250)))

    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize((int(width**random.uniform(
        0.8, 0.9)), int(height**random.uniform(0.8, 0.9))),
                     resample=Image.LANCZOS)
    img = img.resize((int(width**random.uniform(
        0.85, 0.95)), int(height**random.uniform(0.85, 0.95))),
                     resample=Image.BILINEAR)
    img = img.resize((int(width**random.uniform(
        0.89, 0.98)), int(height**random.uniform(0.89, 0.98))),
                     resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, random.randint(3, 7))

    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(random.uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(random.uniform(
        1.0, 2.0))

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    img = Image.blend(img, overlay, random.uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(random.randint(5, 300))

    image_name = "deepfried.jpeg"
    fried_file = os.path.join(Config.DOWN_PATH, image_name)
    img.save(fried_file, "JPEG")
    return fried_file
