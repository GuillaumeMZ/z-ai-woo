"""The UI."""
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QFileDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QWidget
from ultralytics import YOLO

from . import window, zaiwoo

class ZAIWooUI(QMainWindow):
    """The UI."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("zAIwoo")

        self.setMaximumSize(300, 100)

        self._setup_widgets()

        self._csgo_handle: window.Handle = self._find_csgo()

        self._zaiwoo_model: YOLO | None = None

        # zAIwoo "thread"
        self._zaiwoo_timer = QTimer(self)

    def _setup_widgets(self) -> None:
        model_path_label = QLabel("Model path:")
        self._model_path_edit = QLineEdit()
        self._model_path_edit.setEnabled(False)
        self._model_path_select = QPushButton("...")
        self._model_path_select.clicked.connect(self._select_model)

        sensitivity_label = QLabel("In-game sensitivity:")
        self._sensitivity_box = QDoubleSpinBox()
        self._sensitivity_box.setRange(0.0001, 10_000_000)
        self._sensitivity_box.setSingleStep(0.01)
        self._sensitivity_box.setValue(1)

        threshold_label = QLabel("Confidence threshold:")
        self._threshold_box = QDoubleSpinBox()
        self._threshold_box.setRange(0, 1)
        self._threshold_box.setSingleStep(0.01)
        self._threshold_box.setValue(0.75)

        self._start_button = QPushButton("Start zAIwoo")
        self._start_button.clicked.connect(self._start)
        self._stop_button = QPushButton("Stop zAIwoo")
        self._stop_button.setEnabled(False)
        self._stop_button.clicked.connect(self._stop)

        layout = QGridLayout()
        layout.addWidget(model_path_label, 0, 0, 1, 3)
        layout.addWidget(self._model_path_edit, 0, 3, 1, 4)
        layout.addWidget(self._model_path_select, 0, 7, 1, 1)
        layout.addWidget(sensitivity_label, 1, 0, 1, 3)
        layout.addWidget(self._sensitivity_box, 1, 3, 1, 5)
        layout.addWidget(threshold_label, 2, 0, 1, 3)
        layout.addWidget(self._threshold_box, 2, 3, 1, 5)
        layout.addWidget(self._start_button, 4, 0, 2, 4)
        layout.addWidget(self._stop_button, 4, 4, 2, 4)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def _select_model(self) -> None:
        model_path, _ = QFileDialog.getOpenFileName(self, "Select the zAIwoo model...", "C:\\", "YOLO model (*.pt)")

        if model_path == "":
            self._zaiwoo_model = None
            self._model_path_edit.setText("")
            return

        self._zaiwoo_model = YOLO(model_path)
        self._model_path_edit.setText(model_path)

    def _start(self) -> None:
        if self._zaiwoo_model is None:
            QMessageBox.critical(self, "Error", "Please select a model first.")
            return

        self._model_path_select.setEnabled(False)
        self._sensitivity_box.setEnabled(False)
        self._threshold_box.setEnabled(False)
        self._start_button.setEnabled(False)

        self._zaiwoo_timer.timeout.connect(zaiwoo.run(zaiwoo.Settings(
            self._csgo_handle,
            self._zaiwoo_model,
            self._sensitivity_box.value(),
            self._threshold_box.value()
        )))
        self._zaiwoo_timer.start(1000)

        self._stop_button.setEnabled(True)

    def _stop(self) -> None:
        self._model_path_select.setEnabled(True)
        self._sensitivity_box.setEnabled(True)
        self._threshold_box.setEnabled(True)
        self._stop_button.setEnabled(False)

        self._zaiwoo_timer.stop()

        self._start_button.setEnabled(True)

    def _find_csgo(self) -> window.Handle:
        csgo = window.find("Counter-Strike: Global Offensive")
        if csgo is None:
            QMessageBox.critical(self, "Error", "Could not find CS:GO. Are you sure it is launched?")
            sys.exit() # QApplication.exit/.quit doesn't work

        return csgo
