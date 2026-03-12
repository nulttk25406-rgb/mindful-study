import sys
import json
import random
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtCore import QDate
from trang4 import Ui_MainWindow


# ===== LỚP AI ĐƠN GIẢN =====
class AI:
    """AI phân tích cảm xúc"""

    def analyze(self, data_trang1, data_trang2, data_trang3):
        """Phân tích dữ liệu từ 3 trang"""

        # Lấy dữ liệu từ trang 1 (cảm xúc hằng ngày)
        values = [item['value'] for item in data_trang1]

        if not values:
            return "Không có dữ liệu"

        # Tính toán cơ bản
        avg = sum(values) / len(values)
        buon = len([v for v in values if v <= 2])
        binhthuong = len([v for v in values if 3 <= v <= 4])
        vui = len([v for v in values if v >= 5])

        # AI đưa ra nhận xét
        if vui > buon and vui > binhthuong:
            status = "Tích cực 🌟"
            advice = "Tinh thần tốt! Hãy duy trì."
        elif buon > vui and buon > binhthuong:
            status = "Cần quan tâm 💙"
            advice = "Có nhiều ngày buồn. Hãy nghỉ ngơi."
        else:
            status = "Ổn định 🌱"
            advice = "Cảm xúc cân bằng."

        # Dự đoán đơn giản
        last_week = values[-7:] if len(values) >= 7 else values
        next_week_avg = sum(last_week) / len(last_week)

        return {
            'avg': round(avg, 1),
            'buon': buon,
            'binhthuong': binhthuong,
            'vui': vui,
            'total': len(values),
            'status': status,
            'advice': advice,
            'next_week': round(next_week_avg, 1)
        }


# ===== GIAO DIỆN CHÍNH =====
class Trang4Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Màu nền xanh lá
        self.setStyleSheet("""
            QMainWindow { background-color: #E8F5E9; }
            QWidget#centralwidget { background-color: #E8F5E9; }
        """)

        # Khởi tạo AI
        self.ai = AI()

        # Dữ liệu từ các trang (giả lập)
        self.data_trang1 = self.load_trang1()
        self.data_trang2 = self.load_trang2()
        self.data_trang3 = self.load_trang3()

        # Kết nối nút
        self.ui.pushButton.clicked.connect(self.refresh)  # REFRESH
        self.ui.pushButton_2.clicked.connect(self.export)  # EXPORT
        self.ui.pushButton_3.clicked.connect(self.close)  # BACK

        # Hiển thị phân tích
        self.update_analysis()

    def load_trang1(self):
        """Giả lập dữ liệu từ trang 1"""
        data = []
        for i in range(30):
            data.append({
                'date': QDate.currentDate().addDays(-i).toString('dd/MM'),
                'value': random.randint(1, 6)
            })
        return data

    def load_trang2(self):
        """Giả lập dữ liệu từ trang 2"""
        return {
            '7ngay': random.randint(3, 5),
            '30ngay': random.randint(3, 5),
            '3thang': random.randint(3, 5)
        }

    def load_trang3(self):
        """Giả lập dữ liệu từ trang 3"""
        return {
            'total': 30,
            'buon': random.randint(5, 10),
            'binhthuong': random.randint(10, 15),
            'vui': random.randint(5, 10)
        }

    def update_analysis(self):
        """Cập nhật phân tích AI lên các tab"""

        # AI phân tích
        result = self.ai.analyze(self.data_trang1, self.data_trang2, self.data_trang3)

        # ===== TAB 1: TỔNG QUAN =====
        tongquan = "📊 TỔNG QUAN\n"
        tongquan += "=" * 30 + "\n\n"
        tongquan += f"📈 Trung bình: {result['avg']}/6\n"
        tongquan += f"📝 Tổng số: {result['total']} ngày\n\n"
        tongquan += f"😢 Buồn: {result['buon']} ngày\n"
        tongquan += f"😐 Bình thường: {result['binhthuong']} ngày\n"
        tongquan += f"😊 Vui: {result['vui']} ngày\n\n"
        tongquan += f"🎯 Đánh giá: {result['status']}\n"
        tongquan += f"💡 Lời khuyên: {result['advice']}"

        self.ui.textEdit.setText(tongquan)

        # ===== TAB 2: XU HƯỚNG =====
        xuhuong = "📈 XU HƯỚNG\n"
        xuhuong += "=" * 30 + "\n\n"
        xuhuong += f"📊 7 ngày: {self.data_trang2['7ngay']}/6\n"
        xuhuong += f"📊 30 ngày: {self.data_trang2['30ngay']}/6\n"
        xuhuong += f"📊 3 tháng: {self.data_trang2['3thang']}/6\n\n"

        if self.data_trang2['7ngay'] > self.data_trang2['30ngay']:
            xuhuong += "✅ Xu hướng: Đang cải thiện"
        else:
            xuhuong += "📉 Xu hướng: Đang giảm"

        self.ui.textEdit_2.setText(xuhuong)

        # ===== TAB 3: DỰ ĐOÁN =====
        dudoan = "🔮 DỰ ĐOÁN\n"
        dudoan += "=" * 30 + "\n\n"
        dudoan += f"📅 Tuần tới: {result['next_week']}/6\n\n"

        # Dự đoán 7 ngày
        for i in range(7):
            pred = result['next_week'] + random.uniform(-0.5, 0.5)
            pred = max(1, min(6, pred))
            if pred <= 2:
                icon = "😢"
            elif pred <= 4:
                icon = "😐"
            else:
                icon = "😊"
            dudoan += f"Ngày {i + 1}: {icon} {int(pred)}\n"

        self.ui.textEdit_3.setText(dudoan)

    def refresh(self):
        """Làm mới dữ liệu"""
        self.data_trang1 = self.load_trang1()
        self.data_trang2 = self.load_trang2()
        self.data_trang3 = self.load_trang3()
        self.update_analysis()
        QMessageBox.information(self, "AI", "✅ Đã cập nhật dữ liệu mới!")

    def export(self):
        """Xuất báo cáo"""
        # Hỏi người dùng chọn định dạng
        msg = QMessageBox()
        msg.setWindowTitle("Xuất báo cáo")
        msg.setText("Chọn định dạng xuất:")
        msg.addButton("PDF", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("TXT", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("JSON", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Hủy", QMessageBox.ButtonRole.RejectRole)

        result = msg.exec()

        # Lấy nội dung từ các tab
        content = {
            'tongquan': self.ui.textEdit.toPlainText(),
            'xuhuong': self.ui.textEdit_2.toPlainText(),
            'dudoan': self.ui.textEdit_3.toPlainText(),
            'date': QDate.currentDate().toString('dd/MM/yyyy')
        }

        # Xuất theo định dạng
        filename, _ = QFileDialog.getSaveFileName(
            self, "Lưu file", f"baocao_{QDate.currentDate().toString('ddMM')}"
        )

        if filename:
            if 'PDF' in msg.buttonText(msg.clickedButton()):
                with open(filename + '.txt', 'w', encoding='utf-8') as f:
                    f.write("BÁO CÁO PHÂN TÍCH CẢM XÚC\n")
                    f.write(f"Ngày: {content['date']}\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(content['tongquan'] + "\n\n")
                    f.write(content['xuhuong'] + "\n\n")
                    f.write(content['dudoan'])
                QMessageBox.information(self, "AI", f"✅ Đã xuất file TXT: {filename}.txt")

            elif 'TXT' in msg.buttonText(msg.clickedButton()):
                with open(filename + '.txt', 'w', encoding='utf-8') as f:
                    f.write("BÁO CÁO PHÂN TÍCH CẢM XÚC\n")
                    f.write(f"Ngày: {content['date']}\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(content['tongquan'] + "\n\n")
                    f.write(content['xuhuong'] + "\n\n")
                    f.write(content['dudoan'])
                QMessageBox.information(self, "AI", f"✅ Đã xuất TXT: {filename}.txt")

            elif 'JSON' in msg.buttonText(msg.clickedButton()):
                with open(filename + '.json', 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "AI", f"✅ Đã xuất JSON: {filename}.json")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Trang4Window()
    window.show()
    sys.exit(app.exec())