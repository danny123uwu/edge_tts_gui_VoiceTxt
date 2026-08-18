from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
import asyncio

@dataclass
class VoiceInfo:
    id: str
    name: str
    locale: str
    language: str
    country: str
    gender: Optional[str]
    engine_name: str

    @property
    def display_name(self) -> str:
        gender_icon = "👩" if self.gender == "Female" else "👨" if self.gender == "Male" else "🎙️"
        return f"{gender_icon} {self.name} — {self.language} ({self.country})"

@dataclass
class TTSParams:
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "+0%"

class BaseTTSEngine(ABC):
    def __init__(self, name: str, is_remote: bool):
        self.name = name
        self.is_remote = is_remote

    @abstractmethod
    async def fetch_voices(self) -> List[VoiceInfo]:
        pass

    @abstractmethod
    async def synthesize(self, text: str, voice_id: str, params: TTSParams) -> bytes:
        pass
