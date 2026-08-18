import sys
import logging
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    
    # Forzar tema oscuro nativo si está disponible en el sistema
    app.setApplicationName("TTSApp")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())