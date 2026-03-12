from PyQt6.QtWidgets import QApplication, QMainWindow

from loginEx import LoginEx

app=QApplication([])
myWindow=LoginEx()

myWindow.show()
app.exec()