""" enjoy word_emoji """

# by @krishna_bolte
# little help given by @gotstc thanx sir... 🙂

from userge import userge, Message


@userge.on_cmd("hii", about={
    'header': "Use HI to greet someone.\nplugin - @krishna_bolte",
    'flags': {'-bnw': "Show as black and white as background.",
              '-wnb': "Show as white and black as background.",
              '-dnb': "Show as drops and black as background.",
              '-mnb': "Show as monster and black as background.",
              '-fns': "Show as flower and shine as background."},
    'usage': "{tr}hii [emoji]\n{tr}hii [flags]"})
async def hii_(message: Message):
    """hii"""
    if '-bnw' in message.flags:
        paytext = '⬛️'
        filler = '⬜️'
    elif '-wnb' in message.flags:
        paytext = '⬜️'
        filler = '⬛️'
    elif '-dnb' in message.flags:
        paytext = '💦'
        filler = '⬛️'
    elif '-mnb' in message.flags:
        paytext = '🐲'
        filler = '⬛️'
    elif '-fns' in message.flags:
        paytext = '🌺'
        filler = '✨'
    elif message.input_str:
        args = message.input_str.split()
        if len(args) == 2:
            paytext, filler = args
        else:
            paytext = args[0]
            filler = '✨'
    else:
        await message.edit(
            "`Don't feel bad. A lot of people have no brain! and they blame to others.`")
        await message.reply_sticker(sticker="CAADAgADEAADTLa2EO03s8D-kSlOFgQ")
        return
    pay = "{}\n{}\n{}\n{}\n{}".format(
        paytext + filler * 2 + paytext +
        filler + paytext * 3,
        paytext + filler * 2 + paytext +
        filler * 2 + paytext + filler,
        paytext * 4 + filler * 2 + paytext + filler,
        paytext + filler * 2 + paytext +
        filler * 2 + paytext + filler,
        paytext + filler * 2 + paytext +
        filler + paytext * 3)
    await message.edit(pay)


@userge.on_cmd("lol", about={
    'header': "Lol also known as lots of laugh used to indicate "
              "smiling or slight amusement.\nplugin - @krishna_bolte",
    'flags': {'-bnw': "Show as black and white as background.",
              '-wnb': "Show as white and black as background.",
              '-dnb': "Show as drops and black as background.",
              '-mnb': "Show as monster and black as background.",
              '-fns': "Show as flower and shine as background."},
    'usage': "{tr}lol [emoji]\n{tr}lol [flags]"})
async def lol_(message: Message):
    """lol"""
    if '-bnw' in message.flags:
        paytext = '⬛️'
        filler = '⬜️'
    elif '-wnb' in message.flags:
        paytext = '⬜️'
        filler = '⬛️'
    elif '-dnb' in message.flags:
        paytext = '💦'
        filler = '⬛️'
    elif '-mnb' in message.flags:
        paytext = '🐲'
        filler = '⬛️'
    elif '-fns' in message.flags:
        paytext = '🌺'
        filler = '✨'
    elif message.input_str:
        args = message.input_str.split()
        if len(args) == 2:
            paytext, filler = args
        else:
            paytext = args[0]
            filler = '✨'
    else:
        await message.edit(
            "`Don't feel bad. A lot of people have no brain! and they blame to others.`")
        await message.reply_sticker(sticker="CAADAgADEAADTLa2EO03s8D-kSlOFgQ")
        return
    pay = "{}\n{}\n{}\n{}".format(
        paytext + filler * 3 +
        paytext * 3 + filler + paytext + filler * 2,
        paytext + filler * 3 +
        paytext + filler + paytext + filler +
        paytext + filler * 2,
        paytext + filler * 3 + paytext + filler +
        paytext + filler + paytext + filler * 2,
        paytext * 3 + filler + paytext * 3 + filler + paytext * 3)
    await message.edit(pay)


@userge.on_cmd("wtf", about={
    'header': "WTF Generally stands for 'What the fuck'.\nplugin - @krishna_bolte",
    'flags': {'-bnw': "Show as black and white as background.",
              '-wnb': "Show as white and black as background.",
              '-dnb': "Show as drops and black as background.",
              '-mnb': "Show as monster and black as background.",
              '-fns': "Show as flower and shine as background."},
    'usage': "{tr}wtf [emoji]\n{tr}wtf [flags]"})
async def wtf_(message: Message):
    """wtf"""
    if '-bnw' in message.flags:
        paytext = '⬛️'
        filler = '⬜️'
    elif '-wnb' in message.flags:
        paytext = '⬜️'
        filler = '⬛️'
    elif '-dnb' in message.flags:
        paytext = '💦'
        filler = '⬛️'
    elif '-mnb' in message.flags:
        paytext = '🐲'
        filler = '⬛️'
    elif '-fns' in message.flags:
        paytext = '🌺'
        filler = '✨'
    elif message.input_str:
        args = message.input_str.split()
        if len(args) == 2:
            paytext, filler = args
        else:
            paytext = args[0]
            filler = '✨'
    else:
        await message.edit(
            "`Don't feel bad. A lot of people have no brain! and they blame to others.`")
        await message.reply_sticker(sticker="CAADAgADEAADTLa2EO03s8D-kSlOFgQ")
        return
    pay = "{}\n{}\n{}\n{}".format(
        paytext + filler * 3 + paytext +
        filler + paytext * 3 + filler + paytext * 3,
        paytext + filler + paytext + filler + paytext +
        filler * 2 + paytext + filler * 2 + paytext + filler * 2,
        paytext * 2 + filler + paytext * 2 + filler * 2 + paytext +
        filler * 2 + paytext * 2 + filler,
        paytext + filler * 3 + paytext + filler * 2 + paytext + filler * 2 + paytext + filler * 2)
    await message.edit(pay)
