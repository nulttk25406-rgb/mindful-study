from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt, QMargins
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter, QColor


class BieuDoProcessor:
    def __init__(self, chart_container):
        self.chart_container = chart_container
        self.chart_view = None

    def get_statistics(self, time_range):
        """Hàm giả lập tính toán thống kê dựa trên thời gian"""
        # Sau này bạn sẽ thay bằng dữ liệu từ database
        stats = {
            "7 Ngày": {"vui": "Thứ 2", "buon": "Thứ 5", "tong": 7},
            "30 Ngày": {"vui": "Ngày 15", "buon": "Ngày 2", "tong": 30},
            "3 Tháng": {"vui": "Tháng 1", "buon": "Tháng 2", "tong": 90},
            "1 Năm": {"vui": "Tháng 12", "buon": "Tháng 6", "tong": 365}
        }
        return stats.get(time_range, stats["7 Ngày"])

    def create_chart(self, time_range):
        buon, binh_thuong, vui = 3, 5, 8
        if self.chart_view: self.chart_view.deleteLater()

        chart = QChart()
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(0, 0, 0, 0))

        series = QBarSeries()
        data = [(buon, "#ADD8E6", "Buồn"), (binh_thuong, "#6495ED", "Thường"), (vui, "#00008B", "Vui")]
        for v, c, n in data:
            bar = QBarSet(n)
            bar.append(v)
            bar.setColor(QColor(c))
            series.append(bar)

        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent;")

        layout = self.chart_container.layout() or QVBoxLayout(self.chart_container)
        layout.addWidget(self.chart_view)