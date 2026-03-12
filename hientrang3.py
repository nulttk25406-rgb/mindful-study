import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor, QFont, QPainter
from PyQt6.QtPrintSupport import QPrinter
from trang3 import Ui_MainWindow


class LichCamXucWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set màu nền xanh lá nhạt
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E8F5E9;
            }
            QWidget#centralwidget {
                background-color: #E8F5E9;
            }
            QCalendarWidget QWidget {
                background-color: white;
            }
        """)

        # Dữ liệu cảm xúc mẫu (giả lập từ trang 1)
        self.emotion_data = self.load_emotion_from_trang1()

        # Thiết lập calendar
        self.setup_calendar()

        # Thiết lập combo box tháng và năm
        self.setup_month_year_combos()

        # Tô màu lịch theo cảm xúc
        self.color_calendar_by_emotion()

        # Kết nối các nút
        self.connect_buttons()

    def load_emotion_from_trang1(self):
        """Giả lập dữ liệu cảm xúc từ trang 1"""
        data = {}
        today = QDate.currentDate()
        icons = ["😢", "😞", "😐", "🙂", "😊", "😍"]

        # Tạo dữ liệu cho 60 ngày
        for i in range(60):
            date = today.addDays(-i)
            # Random cảm xúc từ 1-6
            value = random.randint(1, 6)
            data[date.toString("yyyy-MM-dd")] = {
                'value': value,
                'icon': icons[value - 1],
                'note': f"Cảm xúc ngày {date.toString('dd/MM/yyyy')}"
            }
        return data

    def setup_calendar(self):
        """Cấu hình calendar"""
        self.ui.calendarWidget.setGridVisible(True)
        self.ui.calendarWidget.setVerticalHeaderFormat(
            self.ui.calendarWidget.VerticalHeaderFormat.ISOWeekNumbers
        )
        self.ui.calendarWidget.clicked.connect(self.show_date_detail)

    def setup_month_year_combos(self):
        """Thiết lập combo box chọn tháng và năm"""
        # Tháng
        self.ui.comboBox.clear()
        for i in range(1, 13):
            self.ui.comboBox.addItem(f"Tháng {i}")
        current_month = QDate.currentDate().month()
        self.ui.comboBox.setCurrentIndex(current_month - 1)

        # Năm (từ 2020 đến 2026)
        self.ui.comboBox_2.clear()
        for year in range(2020, 2027):
            self.ui.comboBox_2.addItem(str(year))
        current_year = QDate.currentDate().year()
        self.ui.comboBox_2.setCurrentText(str(current_year))

        # Kết nối sự kiện
        self.ui.comboBox.currentIndexChanged.connect(self.change_month_year)
        self.ui.comboBox_2.currentIndexChanged.connect(self.change_month_year)

    def change_month_year(self):
        """Đổi tháng và năm trên lịch"""
        month = self.ui.comboBox.currentIndex() + 1
        year = int(self.ui.comboBox_2.currentText())
        self.ui.calendarWidget.setCurrentPage(year, month)

    def get_color_by_emotion(self, value):
        """Lấy màu sắc theo giá trị cảm xúc"""
        if value <= 2:  # Buồn
            return QColor(173, 216, 230)  # Xanh nhạt
        elif value <= 4:  # Bình thường
            return QColor(100, 149, 237)  # Xanh vừa
        else:  # Vui
            return QColor(0, 0, 139)  # Xanh đậm

    def color_calendar_by_emotion(self):
        """Tô màu các ô lịch theo cảm xúc"""
        for date_str, info in self.emotion_data.items():
            year, month, day = map(int, date_str.split("-"))
            qdate = QDate(year, month, day)

            # Tạo format cho ô
            format_ = QTextCharFormat()

            # Màu nền theo cảm xúc
            format_.setBackground(self.get_color_by_emotion(info['value']))

            # Màu chữ tương phản
            if info['value'] >= 5:
                format_.setForeground(QColor(255, 255, 255))  # Trắng
            else:
                format_.setForeground(QColor(0, 0, 0))  # Đen

            # Tooltip hiển thị icon
            format_.setToolTip(f"{info['icon']} - {info['note']}")

            # Áp dụng format
            self.ui.calendarWidget.setDateTextFormat(qdate, format_)

    def show_date_detail(self, date):
        """Hiển thị chi tiết khi click vào ngày"""
        date_str = date.toString("yyyy-MM-dd")

        if date_str in self.emotion_data:
            info = self.emotion_data[date_str]
            msg = f"📅 Ngày: {date.toString('dd/MM/yyyy')}\n"
            msg += f"😊 Cảm xúc: {info['icon']} (mức {info['value']}/6)\n"
            msg += f"📝 Ghi chú: {info['note']}"
            QMessageBox.information(self, "Chi tiết cảm xúc", msg)
        else:
            QMessageBox.information(self, "Thông báo",
                                    "Chưa có dữ liệu cảm xúc cho ngày này")

    def connect_buttons(self):
        """Kết nối các nút bấm"""
        self.ui.pushButton.clicked.connect(self.export_pdf)  # IN PDF
        self.ui.pushButton_2.clicked.connect(self.close)  # BACK

    def export_pdf(self):
        """Xuất lịch cảm xúc ra PDF"""
        # Chọn nơi lưu file
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Xuất PDF",
            f"lich_cam_xuc_{QDate.currentDate().toString('MM_yyyy')}.pdf",
            "PDF Files (*.pdf)"
        )

        if not filename:
            return

        try:
            # Tạo printer
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)

            # Bắt đầu vẽ
            painter = QPainter()
            painter.begin(printer)

            # Vẽ tiêu đề
            font = QFont("Arial", 24, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(100, 100, "LỊCH CẢM XÚC")

            # Vẽ tháng năm
            font = QFont("Arial", 16)
            painter.setFont(font)
            month = self.ui.comboBox.currentText()
            year = self.ui.comboBox_2.currentText()
            painter.drawText(100, 150, f"{month} {year}")

            # Vẽ chú thích màu sắc
            font = QFont("Arial", 12)
            painter.setFont(font)
            y = 200

            # Xanh nhạt - Buồn
            painter.setBrush(QColor(173, 216, 230))
            painter.drawRect(120, y - 15, 20, 20)
            painter.drawText(150, y, "Mức 1-2: Buồn")
            y += 25

            # Xanh vừa - Bình thường
            painter.setBrush(QColor(100, 149, 237))
            painter.drawRect(120, y - 15, 20, 20)
            painter.drawText(150, y, "Mức 3-4: Bình thường")
            y += 25

            # Xanh đậm - Vui
            painter.setBrush(QColor(0, 0, 139))
            painter.drawRect(120, y - 15, 20, 20)
            painter.drawText(150, y, "Mức 5-6: Vui")

            # Thống kê
            if self.emotion_data:
                values = [info['value'] for info in self.emotion_data.values()]
                buon = len([v for v in values if v <= 2])
                binh_thuong = len([v for v in values if 3 <= v <= 4])
                vui = len([v for v in values if v >= 5])
                total = len(values)

                y += 50
                painter.drawText(100, y, f"Tổng số ngày có dữ liệu: {total}")
                y += 25
                painter.drawText(120, y, f"😢 Buồn (xanh nhạt): {buon} ngày")
                y += 20
                painter.drawText(120, y, f"😐 Bình thường (xanh): {binh_thuong} ngày")
                y += 20
                painter.drawText(120, y, f"😊 Vui (xanh đậm): {vui} ngày")

            painter.end()

            QMessageBox.information(self, "Thông báo",
                                    f"✅ Đã xuất PDF thành công!\n📁 {filename}")

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể xuất PDF: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LichCamXucWindow()
    window.show()
    sys.exit(app.exec())