from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt, QDate, QMargins
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter, QFont, QColor


class BieuDoProcessor:
    def __init__(self, chart_container):
        self.chart_container = chart_container
        self.chart_view = None

    def get_sample_data(self, days):
        """Tạo dữ liệu mẫu - thay bằng database thực tế"""
        import random
        data = []
        today = QDate.currentDate()

        for i in range(days):
            date = today.addDays(-i)
            value = random.randint(1, 6)
            data.append((date, value))

        # Sắp xếp theo ngày tăng dần
        data.sort(key=lambda x: x[0])
        return data

    def create_chart(self, time_range):
        """Tạo biểu đồ 3 cột theo khoảng thời gian"""
        # Xác định số ngày
        if "7 Ngày" in time_range:
            days = 7
            title = "BIỂU ĐỒ CẢM XÚC 7 NGÀY"
        elif "30 Ngày" in time_range:
            days = 30
            title = "BIỂU ĐỒ CẢM XÚC 30 NGÀY"
        elif "3 Tháng" in time_range:
            days = 90
            title = "BIỂU ĐỒ CẢM XÚC 3 THÁNG"
        else:  # 1 Năm
            days = 365
            title = "BIỂU ĐỒ CẢM XÚC 1 NĂM"

        # Lấy dữ liệu
        data = self.get_sample_data(days)
        values = [v for _, v in data]

        # Đếm số ngày theo 3 mức
        buon = len([v for v in values if v <= 2])
        binh_thuong = len([v for v in values if 3 <= v <= 4])
        vui = len([v for v in values if v >= 5])

        # Xóa chart cũ
        if self.chart_view:
            self.chart_view.deleteLater()

        # Tạo chart mới
        chart = QChart()
        chart.setTitle(title)
        chart.setTitleFont(QFont("Avenir Next", 18, QFont.Weight.Bold))  # Font to hơn
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(10, 10, 10, 10))

        # Tạo 3 bar set cho 3 cột
        series = QBarSeries()

        # Cột Buồn
        bar_buon = QBarSet("Buồn (1-2)")
        bar_buon.append(buon)
        bar_buon.setColor(QColor(173, 216, 230))  # Xanh nhạt
        bar_buon.setLabelFont(QFont("Avenir Next", 12))
        series.append(bar_buon)

        # Cột Bình thường
        bar_binhthuong = QBarSet("Bình thường (3-4)")
        bar_binhthuong.append(binh_thuong)
        bar_binhthuong.setColor(QColor(100, 149, 237))  # Xanh vừa
        bar_binhthuong.setLabelFont(QFont("Avenir Next", 12))
        series.append(bar_binhthuong)

        # Cột Vui
        bar_vui = QBarSet("Vui (5-6)")
        bar_vui.append(vui)
        bar_vui.setColor(QColor(0, 0, 139))  # Xanh đậm
        bar_vui.setLabelFont(QFont("Avenir Next", 12))
        series.append(bar_vui)

        chart.addSeries(series)

        # Trục X - chỉ có 1 category
        axis_x = QBarCategoryAxis()
        axis_x.append([time_range])
        axis_x.setLabelsFont(QFont("Avenir Next", 14, QFont.Weight.Bold))
        axis_x.setTitleText("Thời gian")
        axis_x.setTitleFont(QFont("Avenir Next", 14, QFont.Weight.Bold))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        # Trục Y - số ngày
        axis_y = QValueAxis()
        max_value = max(buon, binh_thuong, vui) + 1
        axis_y.setRange(0, max_value)
        axis_y.setTickCount(min(max_value + 1, 10))
        axis_y.setLabelsFont(QFont("Avenir Next", 12))
        axis_y.setTitleText("Số ngày")
        axis_y.setTitleFont(QFont("Avenir Next", 14, QFont.Weight.Bold))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Tạo chart view
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background-color: white; border-radius: 15px;")

        # Thêm vào container
        layout = self.chart_container.layout()
        if layout is None:
            layout = QVBoxLayout(self.chart_container)
            self.chart_container.setLayout(layout)

        # Xóa layout cũ
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        layout.addWidget(self.chart_view)