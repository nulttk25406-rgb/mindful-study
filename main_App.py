from PyQt6.QtWidgets import QApplication
from main_Ext import main_Ext
import sys

app = QApplication(sys.argv)
w = main_Ext()
w.show()

sys.exit(app.exec())
