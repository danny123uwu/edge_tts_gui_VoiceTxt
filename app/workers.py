import asyncio
import logging
from PySide6.QtCore import QThread, Signal
from core.tts_base import TTSParams
from engines.edge_tts_engine import EdgeTTSEngine

class TTSWorker(QThread):
    status_update = Signal(str)
    finished_audio = Signal(bytes)
    error_occurred = Signal(str)

    def __init__(self, text: str, voice_id: str, params: TTSParams):
        super().__init__()
        self.text = text
        self.voice_id = voice_id
        self.params = params
        self.engine = EdgeTTSEngine()
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.status_update.emit("Conectando...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.status_update.emit("Generando audio...")
            audio_bytes = loop.run_until_complete(
                self.engine.synthesize(self.text, self.voice_id, self.params)
            )
            self.status_update.emit("Audio generado correctamente")
            self.finished_audio.emit(audio_bytes)
        except Exception as e:
            self.logger.error(f"Error en TTSWorker: {e}")
            self.error_occurred.emit(str(e))
            self.status_update.emit("Error al generar audio")
        finally:
            loop.close()

class VoiceFetcherWorker(QThread):
    voices_fetched = Signal(list)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.engine = EdgeTTSEngine()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            voices = loop.run_until_complete(self.engine.fetch_voices())
            self.voices_fetched.emit(voices)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            loop.close()