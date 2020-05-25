import asyncio
from userge import userge, Message
#by the unknown
@userge.on_cmd("spam$", about={'header': "THE SPAMMER"})
async def brain_func(message):
  animation_chars = [          
              "YOU",
              "ARE",
              "A",
              "REAL",
              "SPAMMER",
              "THAT",
              "I",
              "HAVE",
              "SEEN",
              "YOU ARE A REAL SPAMMER THAT I HAVE",
              "SEEN",
          ]
  for i in range(11):
    await asyncio.sleep(0.3)
    await message.edit(animation_chars[i % 11])
