# © JigarVarma2005
# Logo maker using brandcrowd.com
# Moded from @JVToolsBot by @UniversalBotsUpdate

import os
import requests
from bs4 import BeautifulSoup
from userge import userge, Message, Config


@userge.on_cmd("logo", about={
    'header': "Get a logo from brandcrowd",
    'usage': "{tr}logo text:keyword"})
async def jv_logo_maker(message: Message):

    jv_text = message.input_str
    await message.edit("Please wait...")

    if ':' not in jv_text:

        type_keyword = "name"
        type_text = jv_text

    else:

        jv = jv_text.split(":", 1)
        type_keyword = jv[1]
        type_text = jv[0]

    images = main_logo(type_text, type_keyword)
    image_list = download_images(images)

    if not image_list:
        return await message.err("Images not Found!")

    for i in image_list:
        if os.path.exists(i):
            await message.client.send_photo(message.chat.id, i)
            os.remove(i)
    await message.delete()


def main_logo(type_text, type_keyword):

    url = "https://www.brandcrowd.com/maker/logos?" \
          f"text={type_text}&searchtext={type_keyword}&searchService="
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.findAll("img")
    return images


def download_images(images):

    image_link = None
    return_list = []

    if len(images) > 0:

        for i, image in enumerate(images):

            if image.get("data-srcset"):
                image_link = image.get("data-srcset")

            elif image.get("data-src"):
                image_link = image["data-src"]

            elif image.get("data-fallback-src"):
                image_link = image.get("data-fallback-src")

            elif image.get("src"):
                image_link = image.get("src")

            if not image_link:
                return None

            try:
                r = requests.get(image_link).content

                try:
                    r = str(r, "utf-8")
                except UnicodeDecodeError:
                    with open(f"{Config.DOWN_PATH}/logo_{i}.jpg", "wb+") as f:
                        f.write(r)

                return_list.append(f"{Config.DOWN_PATH}/logo_{i}.jpg")

            except Exception:
                pass

        return return_list

    return None
