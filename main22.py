from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from trang22 import Ui_MainWindow  # File UI của bạn
from bieu_do import BieuDoProcessor


class ChartLogic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 1. Cấu hình Frameless & Nền (Màu nền nhạt chuẩn trang 1)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 2. Khởi tạo Processor biểu đồ
        self.processor = BieuDoProcessor(self.widget)

        # 3. Chạy thiết lập
        self.format()
        self.connect_signals()
        self.update_view("7 Ngày")

    def format(self):
        """Thiết lập màu nền nhạt hơn và 3 nút hệ thống"""
        # Màu nền nhạt hơn xíu (#F8FCFA) để nổi bật các khung bên trong
        self.centralwidget.setStyleSheet("""
            #centralwidget {
                background-color: #F8FCFA; 
                border-radius: 20px;
                border: 1px solid #E0E0E0;
            }
        """)

        # Thiết lập 3 nút hệ thống
        self.pushButton.setText("×")
        self.pushButton_2.setText("□")
        self.pushButton_3.setText("–")

        # ComboBox
        self.comboBox.clear()
        self.comboBox.addItems(["7 Ngày", "30 Ngày", "3 Tháng", "1 Năm"])

    def connect_signals(self):
        """Kết nối các nút bấm"""
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.toggle_maximize)  # Nút Max/Restore
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.comboBox.currentTextChanged.connect(self.update_view)

        if hasattr(self, 'btnBack'):
            self.btnBack.clicked.connect(self.close)

    def toggle_maximize(self):
        """Hàm thông minh: Phóng to nếu đang nhỏ, Thu nhỏ nếu đang to"""
        if self.isMaximized():
            self.showNormal()  # Thu nhỏ về ban đầu
        else:
            self.showMaximized()  # Phóng to toàn màn hình

    def update_view(self, text):
        """Cập nhật thống kê vào textEdit và mốc thời gian vào lineEdit"""
        # Giả lập dữ liệu thống kê
        data = self.processor.get_statistics(text)

        # Hiện vào ô Thống kê (textEdit)
        stats_text = (f"BÁO CÁO: {text.upper()}\n"
                      f"----------------------\n"
                      f"⭐ Ngày vui nhất: {data['vui']}\n"
                      f"🌙 Ngày buồn nhất: {data['buon']}\n"
                      f"📊 Tổng số bản ghi: {data['tong']}\n"
                      f"----------------------")
        self.textEdit.setText(stats_text)

        # Hiện mốc thời gian vào ô lineEdit nằm trên Graph
        if hasattr(self, 'lineEdit'):
            self.lineEdit.setText(f"Dữ liệu: {text}")
            self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Vẽ lại biểu đồ
        self.processor.create_chart(text)

    def reposition_buttons(self):
        """Đảm bảo 3 nút bám sát rìa phải khi kích thước cửa sổ thay đổi"""
        w = self.width()
        # Điều chỉnh tọa độ x dựa trên chiều rộng hiện tại của cửa sổ
        self.pushButton.move(w - 40, 5)
        self.pushButton_2.move(w - 75, 5)
        self.pushButton_3.move(w - 110, 5)

    def resizeEvent(self, event):
        """Tự động nhảy nút khi phóng to/thu nhỏ"""
        self.reposition_buttons()
        super().resizeEvent(event)

    # Mouse drag logic (để có thể kéo app khi ở chế độ Normal)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.isMaximized() and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()