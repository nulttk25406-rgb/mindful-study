import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt, QDate
from trang1 import Ui_NhatKyCamXuc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NhatKyCamXuc()
        self.ui.setupUi(self)

        # Set ngày hiện tại
        self.ui.dateEdit.setDate(QDate.currentDate())

        # Set màu nền xanh nhạt
        self.set_background_color()

        # Kết nối các nút
        self.connect_buttons()

        # Kết nối thanh trượt với hiển thị cảm xúc
        self.ui.progressBar_emotion.valueChanged.connect(self.show_emotion)

    def set_background_color(self):
        """Thiết lập màu nền xanh lá nhạt"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E8F5E9;
            }
            QWidget#centralwidget {
                background-color: #E8F5E9;
            }
            QTextEdit, QDateEdit {
                background-color: white;
                border: 2px solid #A5D6A7;
                border-radius: 10px;
                padding: 5px;
                font-family: "Avenir Next", Arial, sans-serif;
            }
            QSlider::groove:horizontal {
                border: 1px solid #A5D6A7;
                height: 30px;
                background: white;
                border-radius: 15px;
            }
            QSlider::handle:horizontal {
                background: #7FBF9F;
                border: 2px solid #5FA382;
                width: 25px;
                margin: -5px 0;
                border-radius: 12px;
            }
            QSlider::sub-page:horizontal {
                background: #A5D6A7;
                border-radius: 15px;
            }
        """)

    def show_emotion(self):
        """Hiển thị cảm xúc khi kéo thanh trượt"""
        value = self.ui.progressBar_emotion.value()
        emotions = ["😢 RẤT BUỒN", "😞 BUỒN", "😐 BÌNH THƯỜNG", "🙂 TỐT", "😊 RẤT TỐT", "😍 TUYỆT VỜI"]

        # Hiển thị lên thanh trượt (tooltip)
        self.ui.progressBar_emotion.setToolTip(emotions[value - 1])

    def connect_buttons(self):
        """Kết nối các nút bấm"""
        self.ui.btnSave.clicked.connect(self.save_emotion)
        self.ui.btnToPage2.clicked.connect(lambda: self.show_message("LỊCH CẢM XÚC"))
        self.ui.btnToPage3.clicked.connect(lambda: self.show_message("BIỂU ĐỒ CẢM XÚC"))
        self.ui.btnToPage4.clicked.connect(lambda: self.show_message("PHÂN TÍCH AI"))
        self.ui.Back.clicked.connect(self.close)

    def save_emotion(self):
        """Lưu cảm xúc"""
        date = self.ui.dateEdit.date().toString("dd/MM/yyyy")
        value = self.ui.progressBar_emotion.value()
        emotions = ["😢 RẤT BUỒN", "😞 BUỒN", "😐 BÌNH THƯỜNG", "🙂 TỐT", "😊 RẤT TỐT", "😍 TUYỆT VỜI"]
        emotion = emotions[value - 1]
        note = self.ui.txtNote.toPlainText()

        # Hiển thị thông tin đã lưu
        saved_info = f"✅ ĐÃ LƯU: {date}\n{emotion}\n📝 {note}"
        self.ui.textEdit.setText(saved_info)

        QMessageBox.information(self, "Thông báo", "Đã lưu cảm xúc thành công!")

    def show_message(self, page_name):
        """Hiển thị thông báo chuyển trang"""
        QMessageBox.information(self, "Thông báo", f"Đang chuyển đến trang: {page_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())