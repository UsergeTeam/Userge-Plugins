import asyncio
from userge import userge, Message
#by Alone
@userge.on_cmd("hack$", about={'header': "kensar hacking animation"})
async def hack_func(message):
  animation_chars = [          
              "```Connecting To Private Server...```",
              "```Target Selected```",
              "```Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
              "```Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
              "```Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",    
              "```Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
              "```Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒```",
              "```Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒```",
              "```Hacking... 70%\n█████████████████▒▒▒▒▒```",
              "```Hacking... 88%\n█████████████████████▒```",
              "```Hacking... 100%\n███████████████████████```",
              "```Preparing Data... 1%\n▒██████████████████████```",
              "```Preparing Data... 14%\n████▒██████████████████```",
              "```Preparing Data... 30%\n████████▒██████████████```",
              "```Preparing Data... 55%\n████████████▒██████████```",
              "```Preparing Data... 72%\n████████████████▒██████```",
              "```Preparing Data... 88%\n████████████████████▒██```",
              "```Prepared Data... 100%\n███████████████████████```",
              "```Uploading Data to Server... 12%\n███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
              "```Uploading Data to Server... 44%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
              "```Uploading Data to Server... 68%\n███████████████▒▒▒▒▒▒▒▒```",
              "```Uploading Data to Server... 89%\n████████████████████▒▒▒```",
              "```Uploaded Data to Server... 100%\n███████████████████████```",
              "**Targeted Account Hacked**\n\n```Pay 69$ To Remove This Hack```"
          ]
  for i in range(24):
    await asyncio.sleep(2)
    await message.edit(animation_chars[i % 24])