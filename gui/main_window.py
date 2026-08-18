import tempfile
import os
import logging
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QComboBox, QSlider, QLabel, QPushButton, 
    QGroupBox, QFileDialog
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from app.controller import TTSController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TTS Application - Linux")
        self.resize(850, 550)
        self.controller = TTSController()
        self.all_voices = []
        
        # Audio Player Setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.9)
        
        self.current_audio_path = None
        self.init_ui()
        self.load_voices()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Text Input Area
        text_layout = QHBoxLayout()
        text_label = QLabel("Texto:")
        self.btn_import = QPushButton("📂 Importar TXT")
        self.btn_import.clicked.connect(self.on_import_txt)
        text_layout.addWidget(text_label)
        text_layout.addStretch()
        text_layout.addWidget(self.btn_import)
        main_layout.addLayout(text_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Escribe aquí o importa un archivo...")
        main_layout.addWidget(self.text_edit)

        # Controls Layout
        controls_layout = QHBoxLayout()
        
        # Voice Selection (Idioma + Voz)
        voice_group = QGroupBox("Selección de Voz")
        voice_layout = QVBoxLayout()
        
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Idioma:")
        self.language_combo = QComboBox()
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo, 1) # Estira para llenar espacio
        voice_layout.addLayout(lang_layout)
        
        voice_sub_layout = QHBoxLayout()
        voice_label = QLabel("Voz:")
        self.voice_combo = QComboBox()
        voice_sub_layout.addWidget(voice_label)
        voice_sub_layout.addWidget(self.voice_combo, 1)
        voice_layout.addLayout(voice_sub_layout)
        
        voice_group.setLayout(voice_layout)
        controls_layout.addWidget(voice_group, 2) # Ocupa más espacio

        # Parameters
        params_group = QGroupBox("Parámetros")
        params_layout = QVBoxLayout()
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setRange(-100, 100)
        self.rate_slider.setValue(0)
        self.rate_label = QLabel("Velocidad: +0%")
        self.rate_slider.valueChanged.connect(lambda v: self.rate_label.setText(f"Velocidad: {'+' if v>=0 else ''}{v}%"))
        
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setRange(-100, 100)
        self.pitch_slider.setValue(0)
        self.pitch_label = QLabel("Tono: +0Hz")
        self.pitch_slider.valueChanged.connect(lambda v: self.pitch_label.setText(f"Tono: {'+' if v>=0 else ''}{v}Hz"))

        self.vol_slider = QSlider(Qt.Horizontal)
        self.vol_slider.setRange(-100, 100)
        self.vol_slider.setValue(0)
        self.vol_label = QLabel("Volumen: +0%")
        self.vol_slider.valueChanged.connect(lambda v: self.vol_label.setText(f"Volumen: {'+' if v>=0 else ''}{v}%"))

        params_layout.addWidget(self.rate_label)
        params_layout.addWidget(self.rate_slider)
        params_layout.addWidget(self.pitch_label)
        params_layout.addWidget(self.pitch_slider)
        params_layout.addWidget(self.vol_label)
        params_layout.addWidget(self.vol_slider)
        params_group.setLayout(params_layout)
        controls_layout.addWidget(params_group, 3)
        
        main_layout.addLayout(controls_layout)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        self.btn_generate = QPushButton("GENERAR")
        self.btn_generate.clicked.connect(self.on_generate)
        
        self.btn_play = QPushButton("▶ REPRODUCIR")
        self.btn_play.clicked.connect(self.on_play)
        self.btn_play.setEnabled(False)
        
        self.btn_stop = QPushButton("■ DETENER")
        self.btn_stop.clicked.connect(self.on_stop)
        self.btn_stop.setEnabled(False)
        
        self.btn_save = QPushButton("💾 GUARDAR")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_save.setEnabled(False)

        buttons_layout.addWidget(self.btn_generate)
        buttons_layout.addWidget(self.btn_play)
        buttons_layout.addWidget(self.btn_stop)
        buttons_layout.addWidget(self.btn_save)
        main_layout.addLayout(buttons_layout)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Estado: Listo")

    def on_import_txt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importar archivo de texto", "", "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_edit.setPlainText(content)
                    self.status_bar.showMessage(f"Estado: Archivo importado {os.path.basename(file_path)}")
            except Exception as e:
                self.status_bar.showMessage(f"Estado: Error al leer el archivo - {e}")

    def load_voices(self):
        self.status_bar.showMessage("Estado: Cargando voces...")
        self.controller.fetch_voices(
            callback=self.on_voices_loaded,
            error_callback=self.on_error
        )

    def on_voices_loaded(self, voices):
        self.all_voices = voices
        
        # Extraer idiomas únicos y ordenarlos
        languages = sorted(list(set(v.language for v in voices)))
        self.language_combo.clear()
        self.language_combo.addItems(languages)
        
        # Seleccionar Español por defecto si existe
        idx = self.language_combo.findText("Español")
        if idx != -1:
            self.language_combo.setCurrentIndex(idx)
        
        self.status_bar.showMessage("Estado: Listo")

    def on_language_changed(self):
        selected_lang = self.language_combo.currentText()
        self.voice_combo.clear()
        
        # Filtrar voces por el idioma seleccionado
        filtered_voices = [v for v in self.all_voices if v.language == selected_lang]
        
        for voice in filtered_voices:
            # Mostrar solo el nombre y la región en la lista de voz
            gender_icon = "👩" if voice.gender == "Female" else "👨" if voice.gender == "Male" else "🎙️"
            display = f"{gender_icon} {voice.name} — {voice.country}"
            self.voice_combo.addItem(display, userData=voice.id)

    def on_generate(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            self.status_bar.showMessage("Estado: Error - El texto no puede estar vacío")
            return

        voice_id = self.voice_combo.currentData()
        if not voice_id:
            self.status_bar.showMessage("Estado: Error - Selecciona una voz")
            return

        params = {
            "rate": f"{'+' if self.rate_slider.value() >= 0 else ''}{self.rate_slider.value()}%",
            "pitch": f"{'+' if self.pitch_slider.value() >= 0 else ''}{self.pitch_slider.value()}Hz",
            "volume": f"{'+' if self.vol_slider.value() >= 0 else ''}{self.vol_slider.value()}%"
        }

        self.btn_generate.setEnabled(False)
        self.status_bar.showMessage("Estado: Iniciando...")

        self.controller.generate_audio(
            text=text,
            voice_id=voice_id,
            params=params,
            callback=self.on_audio_generated,
            status_callback=self.on_status_update,
            error_callback=self.on_error
        )

    def on_status_update(self, status):
        self.status_bar.showMessage(f"Estado: {status}")

    def on_audio_generated(self, audio_bytes: bytes):
        self.btn_generate.setEnabled(True)
        self.btn_play.setEnabled(True)
        self.btn_save.setEnabled(True)
        
        # Guardar bytes temporalmente para QtMediaPlayer
        if self.current_audio_path and os.path.exists(self.current_audio_path):
            os.remove(self.current_audio_path)
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_bytes)
            self.current_audio_path = temp_file.name
            
        self.player.setSource(QUrl.fromLocalFile(self.current_audio_path))
        self.status_bar.showMessage("Estado: Audio generado correctamente")

    def on_play(self):
        if self.current_audio_path:
            self.player.play()
            self.btn_stop.setEnabled(True)
            self.btn_play.setEnabled(False)
            self.status_bar.showMessage("Estado: Reproduciendo...")

    def on_stop(self):
        self.player.stop()
        self.btn_stop.setEnabled(False)
        self.btn_play.setEnabled(True)
        self.status_bar.showMessage("Estado: Detenido")

    def on_save(self):
        if not self.current_audio_path:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Audio", "audio_generado.mp3", "Audio MP3 (*.mp3)"
        )
        if file_path:
            import shutil
            shutil.copy(self.current_audio_path, file_path)
            self.status_bar.showMessage(f"Estado: Guardado en {file_path}")

    def on_error(self, error_msg):
        self.btn_generate.setEnabled(True)
        self.status_bar.showMessage(f"Estado: Error - {error_msg}")