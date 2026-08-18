import edge_tts
from core.tts_base import BaseTTSEngine, VoiceInfo, TTSParams
from typing import List
import logging

class EdgeTTSEngine(BaseTTSEngine):
    def __init__(self):
        super().__init__(name="Edge TTS", is_remote=True)
        self.logger = logging.getLogger(__name__)

    async def fetch_voices(self) -> List[VoiceInfo]:
        voices_data = await edge_tts.list_voices()
        voices = []
        
        lang_map = {"es": "Español", "en": "English", "pt": "Português", "fr": "Français", "de": "Deutsch", "it": "Italiano"}
        
        country_map = {
            "MX": "México", "ES": "España", "US": "Estados Unidos", "GB": "Reino Unido", 
            "AR": "Argentina", "CO": "Colombia", "CL": "Chile", "PE": "Perú", "VE": "Venezuela",
            "GT": "Guatemala", "EC": "Ecuador", "BO": "Bolivia", "CR": "Costa Rica",
            "CU": "Cuba", "DO": "Rep. Dominicana", "PR": "Puerto Rico", "PY": "Paraguay",
            "UY": "Uruguay", "NI": "Nicaragua", "HN": "Honduras", "SV": "El Salvador", "PA": "Panamá"
        }

        for v in voices_data:
            locale = v.get("Locale", "")
            lang_parts = locale.split("-")
            language_code = lang_parts[0] if lang_parts else ""
            country = lang_parts[1] if len(lang_parts) > 1 else ""
            
            language = lang_map.get(language_code, language_code.upper())
            country_name = country_map.get(country, country)

            gender = v.get("Gender")
            friendly_name = v.get("FriendlyName", "").split("-")[-1].strip()

            voices.append(VoiceInfo(
                id=v.get("ShortName", ""),
                name=friendly_name,
                locale=locale,
                language=language,
                country=country_name,
                gender=gender,
                engine_name=self.name
            ))
            
        # Ordenar por idioma, luego país, luego nombre
        voices.sort(key=lambda x: (x.language, x.country, x.name))
        self.logger.info(f"Obtenidas {len(voices)} voces de Edge TTS.")
        return voices

    async def synthesize(self, text: str, voice_id: str, params: TTSParams) -> bytes:
        communicate = edge_tts.Communicate(
            text, 
            voice_id, 
            rate=params.rate, 
            pitch=params.pitch, 
            volume=params.volume
        )
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
                
        if not audio_data:
            raise RuntimeError("No se recibió audio desde el servidor.")
            
        self.logger.info(f"Audio generado para voz {voice_id}. Tamaño: {len(audio_data)} bytes.")
        return audio_data