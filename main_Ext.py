from PyQt6.QtWidgets import QApplication, QMainWindow
from main import Ui_MainWindow
from report import export_report
from PyQt6.QtCore import QTime, QTimer, Qt
import json
import os


class main_Ext(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.format()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.is_running = False
        self.is_paused = False
        self.total_seconds = 0

        self.resetBtn_2.clicked.connect(self.reset_timer)

        self.focusBtn.clicked.connect(self.toggle_timer)

        self.focusBtn.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self.focusBtn.setStyleSheet("""
QPushButton {
    background-color: #F8BBD0;   
    color: green;
    font-size: 30px;
    font-weight: bold;
    border-radius: 125px;
}

QPushButton:hover {
    background-color: #F48FB1; 
}
""")

        self.initial_seconds = 0
        self.reportBtn_2.clicked.connect(lambda: export_report(self.sessions))
        self.sessions = []
        self.load_sessions()

    def toggle_timer(self):  # Bấm nút
        if not self.is_running:
            if self.total_seconds == 0:
                time = self.timeEdit_2.time()
                hours = time.hour()
                minutes = time.minute()
                seconds = time.second()

                self.total_seconds = hours * 3600 + minutes * 60 + seconds

            if self.total_seconds > 0:
                self.initial_seconds = self.total_seconds
                self.timer.start(1000)
                self.is_running = True
                self.timeEdit_2.setEnabled(False)
                self.focusBtn.setText("PAUSE")

        else:
            self.timer.stop()
            self.is_running = False
            self.focusBtn.setText("RESUME")

    def update_timer(self):
        if self.total_seconds > 0:
            self.total_seconds -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.is_running = False
            self.focusBtn.setText("FOCUS")
            self.timeEdit_2.setEnabled(True)
            QApplication.beep()

            minutes = self.initial_seconds / 60
            self.sessions.append(minutes)
            self.save_sessions()

            print("Sessions:", self.sessions)

        if self.total_seconds <= 10 and self.total_seconds > 0:  # Đổi màu khi còn 10s
            self.focusBtn.setStyleSheet("""
    QPushButton {
        background-color: #F8BBD0;
        color: green;
        font-size: 30px;
        font-weight: bold;
        border-radius: 125px;
    }

    QPushButton:hover {
        background-color: #F48FB1;
    }
    """)

    def update_display(self):
        hours = self.total_seconds // 3600
        minutes = (self.total_seconds % 3600) // 60
        seconds = self.total_seconds % 60

        self.timeEdit_2.setTime(QTime(hours, minutes, seconds))

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.total_seconds = 0
        self.timeEdit_2.setTime(QTime(0, 0, 0))
        self.timeEdit_2.setEnabled(True)
        self.focusBtn.setText("FOCUS")

        self.focusBtn.setStyleSheet("""
    QPushButton {
        background-color: #F8BBD0;
        color: green;
        font-size: 30px;
        font-weight: bold;
        border-radius: 125px;
    }

    QPushButton:hover {
        background-color: #F48FB1;
    }
    """)

    def stop_timer(self):  # Dừng thời gian
        self.timer.stop()
        self.is_running = False
        self.timeEdit_2.setEnabled(True)
        self.focusBtn.setText("FOCUS")

    def load_sessions(self):
        path = os.path.join(os.path.dirname(__file__), "sessions.json")
        if os.path.exists(path):
            f = open(path, "r", encoding='utf8')
            self.sessions = json.load(f)
            f.close()

    def save_sessions(self):
        path = os.path.join(os.path.dirname(__file__), "sessions.json")
        f = open(path, "w", encoding='utf8')
        json.dump(self.sessions, f)
        f.close()

    def format(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.minimize_btn.setText("–")
        self.maximize_btn.setText("□")
        self.close_btn.setText("×")

        self.minimize_btn.setStyleSheet("""
    QPushButton{
        font-size:16px;
        border:none;
        background:transparent;
    }
    QPushButton:hover{
        background:#E5E5E5;
    }
    """)

        self.maximize_btn.setStyleSheet("""
    QPushButton{
        font-size:16px;
        border:none;
        background:transparent;
    }
    QPushButton:hover{
        background:#E5E5E5;
    }
    """)

        self.close_btn.setStyleSheet("""
    QPushButton{
        font-size:16px;
        border:none;
        background:transparent;
    }
    QPushButton:hover{
        background:red;
        color:white;
    }
    """)

        self.minimize_btn.clicked.connect(self.minimize_window)
        self.maximize_btn.clicked.connect(self.maximize_window)
        self.close_btn.clicked.connect(self.close_window)

    def maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def minimize_window(self):
        self.showMinimized()

    def close_window(self):
        self.close()
