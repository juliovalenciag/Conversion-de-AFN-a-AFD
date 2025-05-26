import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1024, 768)
    win.setWindowTitle("AFN → AFD")
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
