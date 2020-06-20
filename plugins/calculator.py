"""enjoy calculator"""

# by krishna

import math
import asyncio

from userge import userge, Message


@userge.on_cmd("add", about={
    'header': "Returns the addition of given numbers.",
    'usage': "{tr}add [ X + Y ]\n\n{tr}add 6969 + 6969"})
async def add_(message: Message):
    """Use to add numbers"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "+" not in message.input_str:
        await message.err("```both numbers required in the form of X + Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('+', maxsplit=1)
    if not number_2:
        await message.err("```Second number required for add```")
        return
    try:

        result = (int(number_1.strip()) + int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("subtract", about={
    'header': "Returns the Subtraction of given numbers.",
    'usage': "{tr}subtract [ X - Y ]\n\n{tr}subtract 6969 - 6969"})
async def subtract_(message: Message):
    """Use to subtract numbers"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "-" not in message.input_str:
        await message.err("```both numbers required in the form of X - Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('-', maxsplit=1)
    if not number_2:
        await message.err("```Second number required for subtract```")
        return
    try:

        result = (int(number_1.strip()) - int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("multiply", about={
    'header': "Returns the Multiplication of given numbers.",
    'usage': "{tr}multiply [ X * Y ]\n\n{tr}multiply 6969 * 6969"})
async def multiply_(message: Message):
    """Use to multiply numbers"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "*" not in message.input_str:
        await message.err("```both numbers required in the form of X * Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('*', maxsplit=1)
    if not number_2:
        await message.err("```Second number required for multiplication```")
        return
    try:
        result = (int(number_1.strip()) * int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("divide", about={
    'header': "Returns the division of given numbers.",
    'usage': "{tr}divide [ X / Y ]\n\n{tr}divide 6969 / 6969"})
async def divide_(message: Message):
    """Use to divide numbers"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "/" not in message.input_str:
        await message.err("```both numbers required in the form of X / Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('/', maxsplit=1)
    if not number_2:
        await message.err("```Second number required for division```")
        return
    try:
        result = (int(number_1.strip()) / int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("fdivide", about={
    'header': "Dividing two integers to get only Quotient known as floor division.",
    'usage': "{tr}fdivide [ X / Y ]\n\n{tr}fdivide 6969 / 6969"})
async def fdivide_(message: Message):
    """Use to get only quotient of two numbers"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "/" not in message.input_str:
        await message.err("```both numbers required in the form of X / Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('/', maxsplit=1)
    if not number_2:
        await message.err("```Second number required to get quotient of two numbers```")
        return
    try:
        result = (int(number_1.strip()) // int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("modulo", about={
    'header': "Modulo operation finds the\n"
    "remainder or signed remainder after\n"
    "division of one number by another.",
    'usage': "{tr}modulo [ X % Y ]\n\n{tr}modulo 6969 % 6969"})
async def modulo_(message: Message):
    """Use to get only remainder of two numbers"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "%" not in message.input_str:
        await message.err("```both numbers required in the form of X % Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('%', maxsplit=1)
    if not number_2:
        await message.err("```Second number required to get modulo of two numbers```")
        return
    try:
        result = (int(number_1.strip()) % int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("factorial", about={
    'header': "Returns the factorial of X number.",
    'usage': "{tr}factorial [ X number ]\n\n{tr}factorial 6969"})
async def factorial_(message: Message):
    """Use to get factorial of a number"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.factorial(int(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("power", about={
    'header': "Returns X raised to the power Y.",
    'usage': "{tr}power [ X ^ Y ]\n\n{tr}power 6969 ^ 6969"})
async def power_(message: Message):
    """Use to get result of exponential power of number"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    if "^" not in message.input_str:
        await message.err("```both numbers required in the form of X ^ Y```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    number_1, number_2 = message.input_str.split('^', maxsplit=1)
    if not number_2:
        await message.err("```Exponential power required```")
        return
    try:

        result = math.pow(int(number_1.strip()), int(number_2.strip()))

        await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
        parse_mode='html')
    except Exception as e:
        await message.err(e)


@userge.on_cmd("sqrt", about={
    'header': "Returns the sqaure root of X number.",
    'usage': "{tr}sqrt [ X number ]\n\n{tr}sqrt 6969"})
async def sqrt_(message: Message):
    """Use to get square root of a number"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.sqrt(int(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("sin", about={
    'header': "Returns the SINE function(x)",
    'usage': "{tr}sin [ X number ]\n\n{tr}sin 69"})
async def sin_(message: Message):
    """SINE function(x)"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.sin(float(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("cos", about={
    'header': "Returns the COSINE function(x)",
    'usage': "{tr}cos [ X number ]\n\n{tr}cos 69"})
async def cos_(message: Message):
    """COSINE function(x)"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.cos(float(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("tan", about={
    'header': "Returns the TANGENT(x)",
    'usage': "{tr}tan [ X number ]\n\n{tr}tan 69"})
async def tan_(message: Message):
    """TANGENT function(x)"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.tan(float(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("deg", about={
    'header': "Converts angle X from radians to degrees",
    'usage': "{tr}deg [ X number ]\n\n{tr}deg 69"})
async def deg_(message: Message):
    """Use to convert from degrees to radians"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.degrees(float(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("rad", about={
    'header': "Converts angle X from degrees to radians",
    'usage': "{tr}rad [ X number ]\n\n{tr}rad 69"})
async def rad_(message: Message):
    """Use to convert from radians to degrees"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.radians(float(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
    parse_mode='html')


@userge.on_cmd("log", about={
    'header': "Returns the logarithm of X to the base",
    'usage': "{tr}log [ X number ]\n\n{tr}log 69"})
async def log_(message: Message):
    """Use to returns the logarithm of X to the base"""

    number = message.input_str
    if not number:
        await message.err("```input not found!```")
        return

    await message.edit("```processing...```")
    await asyncio.sleep(1)

    result = math.degrees(float(number))
    await message.edit("<b>OUTPUT:</b>\n<code>{}</code>".format(result),
parse_mode='html')
