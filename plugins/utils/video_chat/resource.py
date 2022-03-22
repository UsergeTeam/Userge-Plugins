from typing import Tuple

from userge import Message


class TgResource:
    def __init__(self,
                 message: Message,
                 name: str,
                 duration: int,
                 path: str = "",
                 quality: int = 80,
                 is_video: bool = False) -> None:
        self.message = message
        self.name = name
        self.path = path
        self.duration = duration
        self.quality = quality
        self.is_video = is_video

    @classmethod
    def parse(cls,
              message: Message,
              name: str,
              path: str = "",
              duration: int = 0) -> 'TgResource':
        is_video = '-v' in message.flags
        quality = message.flags.get('-q', 80)
        return cls(message, name, duration, path, quality, is_video)

    def __repr__(self) -> str:
        return "<{} name={} duration={}>".format(self.__class__.__name__,
                                                 self.name,
                                                 self.duration)

    def __str__(self) -> str:
        return self.name


class UrlResource:
    def __init__(self,
                 message: Message,
                 name: str,
                 url: str,
                 duration: int,
                 quality: int = 80,
                 is_video: bool = False,
                 file_info: Tuple[int, int, bool, bool] = None) -> None:
        self.message = message
        self.name = name
        self.url = url
        self.duration = duration
        self.quality = quality
        self.is_video = is_video
        self.file_info = file_info

    @classmethod
    def parse(cls,
              message: Message,
              name: str,
              url: str,
              duration: int,
              file_info: Tuple[int, int, bool, bool] = None) -> 'UrlResource':
        is_video = '-v' in message.flags
        quality = message.flags.get('-q', 80)
        return cls(message, name, url, duration, quality, is_video, file_info)

    def __repr__(self) -> str:
        return "<{} name={} duration={}>".format(self.__class__.__name__,
                                                 self.name,
                                                 self.duration)

    def __str__(self) -> str:
        return self.name
