"""Fake Action"""

# by JerryJ1127


import random, asyncio
from userge import userge, Message


@userge.on_cmd("fake", about={
    'header': "Sends fake action to a chat",
    'usage': """{tr}fa :sends fake actions for the default 2 minutes 
                \n\n{tr}fa 5 :sends fake actions for a specified 5 minutes"""})

async def fakeaction(message: Message):
    """Use to send fake action"""

    actions = ['typing', 'upload_photo', 'record_video', 'upload_video', 
                'record_audio', 'upload_audio', 'upload_document', 'find_location', 
                'record_video_note', 'upload_video_note','choose_contact','playing']
                        #unfortunately 'speeking' isn't wokring anymore

    sleep_time = 5      # Should be >=5
    default_time_limit = 2   # In minutes


    if message.input_str:
        time = int(message.input_str)
    else:
        time=default_time_limit
    
    
    limit= (time*60)//sleep_time
    
    await message.delete()

    for i in range(limit):
        await userge.send_chat_action(message.chat.id, random.choice(actions))
        await asyncio.sleep(sleep_time)
    