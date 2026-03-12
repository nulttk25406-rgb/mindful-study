import sys
from PyQt6.QtWidgets import QApplication
from loginEx import LoginEx

app = QApplication(sys.argv)

window = LoginEx()
window.show()

sys.exit(app.exec())