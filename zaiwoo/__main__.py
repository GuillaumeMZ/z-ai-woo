from PySide6.QtWidgets import QApplication

from .ui import ZAIWooUI

app = QApplication()

window = ZAIWooUI()
window.show()

app.exec()
