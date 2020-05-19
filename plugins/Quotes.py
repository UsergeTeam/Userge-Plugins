# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.


from random import choice
import requests
from userge import userge, Message


QUOTE_STRINGS = (
    ".advice - I'm not great at advice. Can I interest you in a sarcastic comment?",
    ".love - Until I was 25, I thought that the only response to ‘I love you’ was ‘Oh, crap!",
    ".stupid - Okay, You Have To Stop The Q-Tip When There Is Resistance.",
    ".stuck - Dear God! This Parachute Is A Knapsack!",
    ".despo - I'm Hopeless And Awkward And Desperate For Love!",
    ".dumb - Hey, Come On, I Say More Dumb Things Before 9 A.M. Than Most People Say All Day.",
    ".dumber - Yes, on a scale from one to 10, 10 being the dumbest a person can look, you are definitely 19.",
    ".shutup - SHUT UP. SHUT UP. SHUT UUPPPP.",
    ".sleep - I Just Realises i can sleep with my eyes open.",
    ".mail - ...tell him to e-mail me at www.hahahanotsomuch.com!",
    ".want - Oh, I wish I could, but I don’t want to.",
    ".line - You’re so far past the line, you can’t even see the line. The line is a dot to you.",
    ".welcome - Welcome to the real world. It sucks. You’re gonna love it.",
    ".smart - Why don’t you stop worrying about sounding smart and just be yourself?",
    ".doin - How you doin’?",
    ".moo - It’s a moo point. It’s like a cow’s opinion; it doesn’t matter. It’s moo.",
    ".sad - When I get sad, I stop being sad and be awesome instead.True story",
    ".lie - A lie is just a great story that someone ruined with the truth.",
    ".legendary - It's going to be legen...wait for it...and I hope you're not lactose-intolerant cause the second half of that word is...dairy!",
    ".awesome - Believe it or not, I was not always as awesome as I am today.",
    ".sarcasm - When people ask me stupid questions, it is my legal obligation to give a sarcastic remark.",
    ".taste - It’s okay if you don’t like me. Not everyone has good taste.",
    ".eyes - You look good when your eyes are closed, but you look the best when my eyes closed.",
    ".poor -If had a dollar for every smart thing you say. I’ll be poor.",
    ".plastic - I don’t believe in plastic surgery. But in your case, go ahead.",
    ".stupd - Are you always so stupid or is today a special ocassion.",
    ".ego - If I wanted to kill myself I would climb your ego and jump to your IQ.",
    ".sarcasm - I love sarcasm. It’s like punching people in the face but with words.",
    ".hurt - I’m sorry I hurt your feelings when I called you stupid. I really thought you already knew.",
    ".know - Unless your name is Google stop acting like you know everything.",
    ".hell - I’d tell you to go to hell, but I work there and don’t want to see your ugly mug every day.",
    ".face - I never forget a face, but in your case, I’ll be glad to make an exception.",
    ".stupider - Everyone has the right to be stupid, but you are abusing the privilege.",
    ".bleed - I’m not replying, but keep writing. I enjoy the way your words makes my eyes bleed.",
    ".life - Life’s good, you should get one.",
    ".repeat - No, you don’t have to repeat yourself. I was ignoring you the first time."
)



@userge.on_cmd("quote$", about="__Check yourself ;)__")
async def quote_(message: Message):
    """quote"""
    await message.edit(choice(QUOTE_STRINGS), parse_mode="html")

