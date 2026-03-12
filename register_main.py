import sys
from PyQt6.QtWidgets import QApplication, QDialog
from registerEx import  RegisterEx

app = QApplication(sys.argv)

dialog = QDialog()
ui = RegisterEx()

ui.show()

sys.exit(app.exec())