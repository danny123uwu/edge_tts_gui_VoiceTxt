import logging
from app.workers import TTSWorker, VoiceFetcherWorker
from core.tts_base import TTSParams

class TTSController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tts_worker = None
        self.voices = []

    def fetch_voices(self, callback, error_callback):
        self.worker = VoiceFetcherWorker()
        self.worker.voices_fetched.connect(callback)
        self.worker.error_occurred.connect(error_callback)
        self.worker.start()

    def generate_audio(self, text: str, voice_id: str, params: dict, callback, status_callback, error_callback):
        if self.tts_worker and self.tts_worker.isRunning():
            self.tts_worker.quit()
            self.tts_worker.wait()

        tts_params = TTSParams(
            rate=params.get("rate", "+0%"),
            pitch=params.get("pitch", "+0Hz"),
            volume=params.get("volume", "+0%")
        )

        self.tts_worker = TTSWorker(text, voice_id, tts_params)
        self.tts_worker.status_update.connect(status_callback)
        self.tts_worker.finished_audio.connect(callback)
        self.tts_worker.error_occurred.connect(error_callback)
        self.tts_worker.start()

    def cancel_generation(self):
        if self.tts_worker and self.tts_worker.isRunning():
            self.logger.info("Cancelando generación de audio...")
            # En el futuro implementaremos cancelación segura a nivel de asyncio
            self.tts_worker.terminate() 
            self.tts_worker.wait()