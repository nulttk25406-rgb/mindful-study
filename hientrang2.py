import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt, QDate
from trang2 import Ui_MainWindow
from bieu_do import BieuDoProcessor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Chỉ đổi màu nền xanh lá nhạt
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E8F5E9;
            }
            QWidget#centralwidget {
                background-color: #E8F5E9;
            }
        """)

        # Ẩn Lb không cần thiết
        self.ui.Lb.hide()

        # Đổi tên widget thành chartContainer
        self.ui.chartContainer = self.ui.widget
        self.ui.widget.setObjectName("chartContainer")

        # Khởi tạo processor cho biểu đồ
        self.chart_processor = BieuDoProcessor(self.ui.chartContainer)

        # Thiết lập combo box
        self.setup_combo_box()

        # Kết nối các nút
        self.connect_buttons()

        # Vẽ biểu đồ mặc định (7 ngày)
        self.ui.comboBox.setCurrentText("7 Ngày")
        self.chart_processor.create_chart("7 Ngày")
        self.update_statistics("7 Ngày")
        self.update_time_display("7 Ngày")

    def setup_combo_box(self):
        """Thiết lập các lựa chọn cho combo box"""
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["7 Ngày", "30 Ngày", "3 Tháng", "1 Năm"])
        self.ui.comboBox.currentTextChanged.connect(self.on_time_range_changed)

    def connect_buttons(self):
        """Kết nối các nút bấm"""
        self.ui.btnExport.clicked.connect(self.export_report)
        self.ui.btnBack.clicked.connect(self.close)

    def on_time_range_changed(self, time_range):
        """Xử lý khi thay đổi combo box"""
        if time_range:
            self.chart_processor.create_chart(time_range)
            self.update_statistics(time_range)
            self.update_time_display(time_range)

    def update_time_display(self, time_range):
        """Cập nhật hiển thị thông tin thời gian trên lineEdit"""
        today = QDate.currentDate()

        if "7 Ngày" in time_range:
            start_date = today.addDays(-6)
            info = f"📅 {start_date.toString('dd/MM')} - {today.toString('dd/MM/yyyy')}"
        elif "30 Ngày" in time_range:
            start_date = today.addDays(-29)
            info = f"📅 {start_date.toString('dd/MM/yyyy')} - {today.toString('dd/MM/yyyy')}"
        elif "3 Tháng" in time_range:
            start_date = today.addMonths(-2)
            info = f"📅 {start_date.toString('MM/yyyy')} - {today.toString('MM/yyyy')}"
        else:  # 1 Năm
            start_date = today.addYears(-1)
            info = f"📅 {start_date.toString('MM/yyyy')} - {today.toString('MM/yyyy')}"

        self.ui.lineEdit.setText(info)

    def update_statistics(self, time_range):
        """Cập nhật thống kê"""
        # Lấy số ngày từ time_range
        if "7 Ngày" in time_range:
            days = 7
        elif "30 Ngày" in time_range:
            days = 30
        elif "3 Tháng" in time_range:
            days = 90
        else:
            days = 365

        # Lấy dữ liệu từ processor
        data = self.chart_processor.get_sample_data(days)

        if not data:
            return

        values = [v for _, v in data]

        # Phân loại theo 3 mức
        buon = len([v for v in values if v <= 2])
        binh_thuong = len([v for v in values if 3 <= v <= 4])
        vui = len([v for v in values if v >= 5])

        # Phần trăm
        total = len(values)
        buon_percent = (buon / total) * 100
        binh_thuong_percent = (binh_thuong / total) * 100
        vui_percent = (vui / total) * 100

        stats = f"📊 THỐNG KÊ {time_range}\n\n"
        stats += f"💙 Buồn (xanh nhạt): {buon} ngày ({buon_percent:.1f}%)\n"
        stats += f"💚 Bình thường (xanh vừa): {binh_thuong} ngày ({binh_thuong_percent:.1f}%)\n"
        stats += f"💚 Vui (xanh đậm): {vui} ngày ({vui_percent:.1f}%)\n\n"

        stats += "📋 CHI TIẾT 10 NGÀY GẦN NHẤT:\n"

        # Hiển thị 10 ngày gần nhất
        recent_data = data[-10:] if len(data) > 10 else data
        for date, value in reversed(recent_data):
            if value <= 2:
                emotion = "💙 Buồn"
            elif value <= 4:
                emotion = "💚 Bình thường"
            else:
                emotion = "💚 Vui"
            stats += f"   {date.toString('dd/MM')}: {emotion}\n"

        self.ui.textEdit.setText(stats)

    def export_report(self):
        """Xuất báo cáo"""
        time_range = self.ui.comboBox.currentText()
        stats = self.ui.textEdit.toPlainText()
        time_info = self.ui.lineEdit.text()

        # Tạo nội dung báo cáo
        report = f"BÁO CÁO CẢM XÚC - {time_range}\n"
        report += f"{time_info}\n"
        report += f"Ngày xuất: {QDate.currentDate().toString('dd/MM/yyyy')}\n"
        report += "=" * 50 + "\n\n"
        report += stats

        # Lưu ra file
        filename = f"bao_cao_cam_xuc_{time_range.replace(' ', '_')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            QMessageBox.information(self, "Thông báo",
                                    f"✅ Đã xuất báo cáo {time_range} thành công!\n📁 File: {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể xuất báo cáo: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())