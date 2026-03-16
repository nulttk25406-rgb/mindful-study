
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import Qt, QDate
from trang11 import Ui_NhatKyCamXuc  # Đảm bảo file giao diện .py của bạn tên là ui_design


class NhatKyLogic(QMainWindow, Ui_NhatKyCamXuc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Bỏ khung mặc định của Windows
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Gọi các hàm cấu trúc chuẩn
        self.format()  # Định dạng nền và nút
        self.connect_signals()  # Liên kết các nút bấm

    def format(self):
        """Hàm định dạng nền xanh nhạt và thiết lập text cho 3 nút"""
        # Áp dụng màu nền xanh nhạt từ hình bạn gửi cho phần centralwidget
        self.centralwidget.setStyleSheet("""
            #centralwidget {
                background-color: #F7FDF9;
                border-radius: 20px;
            }
        """)

        # Thiết lập text cho 3 nút điều khiển (lấy từ file UI của bạn)
        self.pushButton_3.setText("–")  # Nút Minimize
        self.pushButton_2.setText("□")  # Nút Maximize/Restore
        self.pushButton.setText("×")  # Nút Close

    def connect_signals(self):
        """Hàm liên kết các nút lệnh với hàm xử lý"""
        # Kết nối 3 nút hệ thống
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_2.clicked.connect(self.toggle_maximize)
        self.pushButton.clicked.connect(self.close)

        # Kết nối các nút chức năng khác
        self.btnSave.clicked.connect(self.save_emotion)
        self.Back.clicked.connect(self.clear_info)

    # --- CÁC HÀM XỬ LÝ CHỨC NĂNG ---

    def toggle_maximize(self):
        """Phóng to hoặc thu về kích thước ban đầu"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def save_emotion(self):
        """Hàm lưu thông tin và hiển thị lên textEdit"""
        ngay = self.dateEdit.date().toString("dd/MM/yyyy")
        cam_xuc = self.progressBar_emotion.value()
        ghi_chu = self.txtNote.toPlainText().strip()

        ket_qua = f"--- DỮ LIỆU ĐÃ LƯU ---\n📅 Ngày: {ngay}\n🎭 Cảm xúc: {cam_xuc}\n📝 Ghi chú: {ghi_chu}"
        self.textEdit.setText(ket_qua)
        QMessageBox.information(self, "Thông báo", "Lưu thành công!")

    def clear_info(self):
        """Hàm xóa thông tin (Nút Quay lại)"""
        self.textEdit.clear()
        self.txtNote.clear()
        self.dateEdit.setDate(QDate.currentDate())

    # --- HÀM DI CHUYỂN CỬA SỔ ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()