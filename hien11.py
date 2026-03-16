import sys
from PyQt6 import QtWidgets
from main11 import NhatKyLogic

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Khởi tạo class Logic
    window = NhatKyLogic()
    window.show()

    sys.exit(app.exec())