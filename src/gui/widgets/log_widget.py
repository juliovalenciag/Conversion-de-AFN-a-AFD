from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def log(self, message: str):
        self.text.append(message)
        self.text.ensureCursorVisible()

    def clear(self):
        self.text.clear()