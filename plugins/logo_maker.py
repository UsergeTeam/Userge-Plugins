# © JigarVarma2005
# Logo maker using brandcrowd.com
# Moded from @JVToolsBot by @UniversalBotsUpdate

import os
import random
import requests
from bs4 import BeautifulSoup
from pyrogram import filters
from userge import userge, Message, Config


def download_images(images):
    count = 0
    print(f"Total {len(images)} Image Found!")
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_link = image["data-srcset"]
            except:
                try:
                    image_link = image["data-src"]
                except:
                    try:
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            image_link = image["src"]
                        except:

                            pass
            try:
                r = requests.get(image_link).content
                try:
                    r = str(r, "utf-8")
                except UnicodeDecodeError:
                    with open(f"{Config.DOWN_PATH}/logo.jpg", "wb+") as f:
                        f.write(r)
                    count += 1
            except:
                pass


def main_logo(type_text, type_keyword):
    url = f"https://www.brandcrowd.com/maker/logos?text={type_text}&searchtext={type_keyword}&searchService="
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.findAll("img")
    random.shuffle(images)
    download_images(images)
    
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
  main_logo(type_text, type_keyword)
  logo_path = f"{Config.DOWN_PATH}/logo.jpg"
  await message.client.send_photo(message.chat.id, logo_path)
  await message.delete()
  try:
    os.remove(logo_path)
  except:
    pass
    
