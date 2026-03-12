import json
import os
from PyQt6.QtWidgets import QMainWindow, QLineEdit
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from reset import Ui_Reset
from PyQt6.QtGui import QPixmap



class ResetEx(QMainWindow, Ui_Reset):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.format()
        self.default_value()

        # window buttons
        self.btn_minimize.clicked.connect(self.minimize_window)
        self.btn_maximize.clicked.connect(self.maximize_window)
        self.btn_close.clicked.connect(self.close_window)
        self.pB_ma.clicked.connect(self.back_login)

        self.binding_events()

        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "p_Images", "background.png")

        pix = QPixmap(img_path)
        self.label_background.setPixmap(pix)
        self.label_background.setScaledContents(True)

    def format(self):

        self.lbl_error.setStyleSheet("color:red;")
        self.label_khoiphuc.setStyleSheet("color:red;color:#5F7F73;font-weight:700;")
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        self.lbl_error.setMinimumHeight(50)


    def default_value(self):

        self.lineEdit_tendangnhap.setPlaceholderText("Nhập tên đăng nhập")
        self.lineEdit_matkhau.setPlaceholderText("Nhập mật khẩu mới")
        self.lineEdit_xacnhan.setPlaceholderText("Xác nhận mật khẩu")

        self.lineEdit_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_xacnhan.setEchoMode(QLineEdit.EchoMode.Password)


    def minimize_window(self):
        self.showMinimized()

    def maximize_window(self):

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def close_window(self):
        self.close()


    def binding_events(self):

        self.btn_eye_password.clicked.connect(self.show_hide_password)
        self.btn_eye_confirm.clicked.connect(self.show_hide_confirm)

        self.lineEdit_tendangnhap.textChanged.connect(self.hide_error)
        self.lineEdit_matkhau.textChanged.connect(self.hide_error)
        self.lineEdit_xacnhan.textChanged.connect(self.hide_error)

        self.pB_ma.clicked.connect(self.reset_password)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


    def show_hide_password(self):

        if self.lineEdit_matkhau.echoMode() == QLineEdit.EchoMode.Password:

            self.lineEdit_matkhau.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_eye_password.setIcon(QIcon("p_Images/eye_open.jpeg"))
            self.btn_eye_password.setIconSize(QSize(28, 28))

        else:

            self.lineEdit_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_eye_password.setIcon(QIcon("p_Images/eye_close.png"))
            self.btn_eye_password.setIconSize(QSize(20, 20))


    def show_hide_confirm(self):

        if self.lineEdit_xacnhan.echoMode() == QLineEdit.EchoMode.Password:

            self.lineEdit_xacnhan.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_eye_confirm.setIcon(QIcon("p_Images/eye_open.jpeg"))
            self.btn_eye_confirm.setIconSize(QSize(28, 28))

        else:

            self.lineEdit_xacnhan.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_eye_confirm.setIcon(QIcon("p_Images/eye_close.png"))
            self.btn_eye_confirm.setIconSize(QSize(20, 20))

    def show_error(self, message):

        self.lbl_error.setText(message)
        self.lbl_error.setVisible(True)

    def hide_error(self):

        self.lbl_error.setText("")
        self.lbl_error.setVisible(False)


    def reset_password(self):

        username = self.lineEdit_tendangnhap.text()
        password = self.lineEdit_matkhau.text()
        confirm = self.lineEdit_xacnhan.text()

        if username == "" or password == "" or confirm == "":
            self.show_error("Vui lòng nhập đầy đủ thông tin")
            return

        if password != confirm:
            self.show_error("Mật khẩu không khớp")
            return

        if not os.path.exists("users.json"):
            self.show_error("Không có dữ liệu tài khoản")
            return

        with open("users.json", "r", encoding="utf8") as f:
            users = json.load(f)

        found = False

        for user in users:
            if user["username"] == username:
                user["password"] = password
                found = True
                break

        if not found:
            self.show_error("Tên đăng nhập không tồn tại")
            return

        with open("users.json", "w", encoding="utf8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

        self.label_error.setStyleSheet("color:green")
        self.label_error.setText("Đổi mật khẩu thành công")

    def back_login(self):
        from loginEx import LoginEx

        self.login = LoginEx()
        self.login.show()
        self.close()
