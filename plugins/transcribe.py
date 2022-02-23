import io
import os
import re
import traceback
from asyncio import sleep

from aiohttp import ClientSession
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from userge import userge, Message, Config
from userge.utils import get_media_path_and_name

logger = userge.getLogger(__name__)


class WitAiAPI:
    """
    A class to interact with Wit.ai API
    Based on https://github.com/charslab/TranscriberBot work
    """

    def __init__(self, lang):
        self.api_keys = {}
        for i in filter(lambda x: x.startswith('WIT_AI_API_'), os.environ):
            self.api_keys.update({i.split('WIT_AI_API_')[1].lower(): os.environ.get(i)})
        self.api_url = "https://api.wit.ai"
        self.lang = lang
        self.chunks = None
        self.text = ""

    def has_api_key(self):
        return self.api_keys.get(self.lang)

    async def __transcribe_chunk(self, chunk, lang='ar') -> (str, str):
        """
        Based on https://github.com/charslab/TranscriberBot/blob/
        823b1423832b7117ad41c83abb3e25d58dd9e789/src/audiotools/
        speech.py#L13
        """
        text = ""
        error = ""
        headers = {
            'authorization': f'Bearer {self.api_keys[lang]}',
            'accept': 'application/vnd.wit.20200513+json',
            'content-type': 'audio/raw;encoding=signed-integer;bits=16;rate=8000;endian=little',
        }
        try:
            async with ClientSession() as session, session.post(
                f"{self.api_url}/speech", headers=headers,
                data=io.BufferedReader(io.BytesIO(chunk.raw_data))
            ) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    text = response['_text'] if '_text' in response else response['text']
        except Exception as e:
            error = f"Could not transcribe chunk: {e}\n{traceback.format_exc()}"

        return text, error

    @staticmethod
    async def __generate_chunks(segment, length=20000 / 1001):
        """
        Based on https://github.com/charslab/TranscriberBot/blob/
        823b1423832b7117ad41c83abb3e25d58dd9e789/
        src/audiotools/speech.py#L49
        """
        return [segment[i:i + int(length * 1000)]
                for i in range(0, len(segment), int(length * 1000))]

    @staticmethod
    async def __preprocess_audio(audio):
        """
        From https://github.com/charslab/TranscriberBot/blob/
        823b1423832b7117ad41c83abb3e25d58dd9e789/
        src/audiotools/speech.py#L67
        """
        return audio.set_sample_width(2).set_channels(1).set_frame_rate(8000)

    async def transcribe(self, path):
        """
        Based on https://github.com/charslab/TranscriberBot/blob/
        823b1423832b7117ad41c83abb3e25d58dd9e789/
        src/audiotools/speech.py#L70
        """
        logger.info("Transcribing file %s", path)
        try:
            audio = AudioSegment.from_file(path)
            chunks = await self.__generate_chunks(await self.__preprocess_audio(audio))
            self.chunks = len(chunks)
            logger.info("Got %d chunks", len(chunks))

            for i, chunk in enumerate(chunks):
                logger.info("Transcribing chunk %d", i)
                text, error = await self.__transcribe_chunk(chunk, self.lang)
                self.text += text
                yield text, error

        except CouldntDecodeError:
            yield None, "`Error decoding the audio file. " \
                        "Ensure that the provided audio is a valid audio file!`"


@userge.on_cmd("stt", about={
    'header': "transcribe a file (speech to text)",
    'options': {'-t': 'send text to telegram as well as the transcription file'},
    'usage': "{tr}stt lang [file / folder path | direct link | reply to telegram file]",
    'examples': ['{tr}stt en link', '{tr}stt ar -t link']
}, check_downpath=True, del_pre=True)
async def stt_(message: Message):
    """ Speech to text using Wit.ai """
    send_text = bool('t' in message.flags)
    replied = message.reply_to_message
    message_id = replied.message_id if replied else message.message_id
    regex = re.compile(r'([\S]*)(?: |)([\s\S]*)')
    match = regex.search(message.filtered_input_str)
    if not match:
        await message.edit("`Please read .help stt`")
        return
    lang = match.group(1).lower()
    api = WitAiAPI(lang)
    if not api.has_api_key():
        await message.edit(f'`Please set WIT_AI_API_{lang.upper()} variable first!`')
        return
    data = await get_media_path_and_name(message)
    if not data:
        return
    file_path, file_name = data
    await message.edit("`Starting transcribing...`")
    processed = 0
    async for _, error in api.transcribe(file_path):
        if error:
            await message.edit(error)
            return
        processed += 1
        await message.edit(f"`Processed chunk {processed} of {api.chunks}`")
    if send_text:
        text_chunks = [api.text[i:i + Config.MAX_MESSAGE_LENGTH] for i in
                       range(0, len(api.text), Config.MAX_MESSAGE_LENGTH)]
        if len(text_chunks) == 1:
            await message.edit(text_chunks[0])
        else:
            await message.edit(text_chunks[0])
            for chunk in text_chunks[1:]:
                await message.reply(chunk)
                await sleep(2)
    # send transcription text file
    await message.client.send_as_file(
        chat_id=message.chat.id, reply_to_message_id=message_id,
        text=api.text, filename=f"{file_name}_{lang}_transcription.txt")
