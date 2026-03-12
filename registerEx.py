import json
import os
from PyQt6.QtWidgets import QMainWindow, QLineEdit
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from register import Ui_Register
from PyQt6.QtGui import QPixmap





class RegisterEx(QMainWindow, Ui_Register):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.format()
        self.default_value()

        self.btn_minimize.clicked.connect(self.minimize_window)
        self.btn_maximize.clicked.connect(self.maximize_window)
        self.btn_close.clicked.connect(self.close_window)

        self.binding_events()
        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "p_Images", "background.png")

        pix = QPixmap(img_path)
        self.label_background.setPixmap(pix)
        self.label_background.setScaledContents(True)

        self.pB_dangky.clicked.connect(self.back_login)

    def format(self):
        self.label_dangky.setStyleSheet("color:#5F7F73;font-weight:700;")
        self.lbl_error.setStyleSheet("color:red;")
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        self.lbl_error.setMinimumHeight(50)


    def default_value(self):

        self.LineE_hovaten.setPlaceholderText("Nhập họ và tên")
        self.LineE_tendangnhap.setPlaceholderText("Nhập tên đăng nhập")
        self.LineE_matkhau.setPlaceholderText("Nhập mật khẩu")
        self.LineE_xacnhan.setPlaceholderText("Xác nhận mật khẩu")

        self.LineE_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
        self.LineE_xacnhan.setEchoMode(QLineEdit.EchoMode.Password)

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

        self.btn_eye_password.clicked.connect(self.toggle_password)
        self.btn_eye_confirm.clicked.connect(self.toggle_confirm)

        self.LineE_hovaten.textChanged.connect(self.hide_error)
        self.LineE_tendangnhap.textChanged.connect(self.hide_error)
        self.LineE_matkhau.textChanged.connect(self.hide_error)
        self.LineE_xacnhan.textChanged.connect(self.hide_error)

        self.pB_dangky.clicked.connect(self.register)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.pB_dangnhap.clicked.connect(self.back_login)


    def toggle_password(self):

        if self.LineE_matkhau.echoMode() == QLineEdit.EchoMode.Password:

            self.LineE_matkhau.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_eye_password.setIcon(QIcon("p_Images/eye_open.jpeg"))
            self.btn_eye_password.setIconSize(QSize(28, 28))

        else:

            self.LineE_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_eye_password.setIcon(QIcon("p_Images/eye_close.png"))
            self.btn_eye_password.setIconSize(QSize(20, 20))

    def toggle_confirm(self):

        if self.LineE_xacnhan.echoMode() == QLineEdit.EchoMode.Password:

            self.LineE_xacnhan.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_eye_confirm.setIcon(QIcon("p_Images/eye_open.jpeg"))
            self.btn_eye_confirm.setIconSize(QSize(28, 28))

        else:

            self.LineE_xacnhan.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_eye_confirm.setIcon(QIcon("p_Images/eye_close.png"))
            self.btn_eye_confirm.setIconSize(QSize(20, 20))


    def show_error(self, message):

        self.lbl_error.setText(message)
        self.lbl_error.setVisible(True)

    def hide_error(self):
        self.lbl_error.setText("")
        self.lbl_error.setVisible(False)


    def register(self):

        fullname = self.LineE_hovaten.text()
        username = self.LineE_tendangnhap.text()
        password = self.LineE_matkhau.text()
        confirm = self.LineE_xacnhan.text()

        if fullname == "" or username == "" or password == "" or confirm == "":
            self.show_error("Vui lòng nhập đầy đủ thông tin")
            return

        if password != confirm:
            self.show_error("Mật khẩu xác nhận không khớp")
            return

        if len(username) < 4 or len(username) > 20:
            self.show_error("Tên đăng nhập phải từ 4-20 ký tự")
            return

        if " " in username:
            self.show_error("Tên đăng nhập không được có khoảng trắng")
            return

        if len(password) < 6 or len(password) > 20:
            self.show_error("Mật khẩu phải từ 6-20 ký tự")
            return

        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)

        if not (has_letter and has_number):
            self.show_error("Mật khẩu phải có chữ và số")
            return

        self.hide_error()

        os.makedirs("Data", exist_ok=True)

        filename = "Data/accounts.json"

        try:
            with open(filename, "r", encoding="utf8") as f:
                data = json.load(f)
        except:
            data = {"users": []}

        for user in data["users"]:
            if username == user["username"]:
                self.show_error("Tên đăng nhập đã tồn tại")
                return

        new_user = {
            "fullname": fullname,
            "username": username,
            "password": password
        }

        data["users"].append(new_user)

        with open(filename, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Đăng ký thành công")

        self.hide()

    def back_login(self):
        from loginEx import LoginEx

        self.login = LoginEx()
        self.login.show()
        self.close()







