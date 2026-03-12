import json
from PyQt6.QtWidgets import QMainWindow, QLineEdit
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtGui import QIcon
from login import Ui_Login
from PyQt6.QtGui import QPixmap
from registerEx import RegisterEx
from resetEx import ResetEx

class LoginEx(QMainWindow,Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.format()
        self.default_value()
        self.btn_minimize.clicked.connect(self.minimize_window)
        self.btn_maximize.clicked.connect(self.maximize_window)
        self.btn_close.clicked.connect(self.close_window)
        self.binding_events()
        pix = QPixmap("p_Images/login.png")
        self.label_login.setPixmap(pix)
        self.label_login.setScaledContents(True)
        self.pB_dangky.clicked.connect(self.open_register)
        self.pB_quenmk.clicked.connect(self.open_reset)



    def format(self):
        self.pB_quenmk.setStyleSheet("color:#4E6F66; font-weight:600;")
        self.pB_dangky.setStyleSheet("color:#4E6F66; font-weight:600;")


        self.lbl_error.setStyleSheet("color:red;")
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        self.lbl_error.setMinimumHeight(50)

    def default_value(self):
        self.LineE_tendangnhap.setPlaceholderText("Nhập tên đăng nhập")
        self.LineE_matkhau.setPlaceholderText("Nhập mật khẩu")
        self.LineE_matkhau.setEchoMode(QLineEdit.EchoMode.Password)


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
        self.btn_eye.clicked.connect(self.show_hide_password)
        self.LineE_tendangnhap.textChanged.connect(self.hide_error)
        self.LineE_matkhau.textChanged.connect(self.hide_error)
        self.pB_dangnhap.clicked.connect(self.login)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


    def show_hide_password(self):

        if self.LineE_matkhau.echoMode() == QLineEdit.EchoMode.Password:

            self.LineE_matkhau.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_eye.setIcon(QIcon("p_Images/eye_open.jpeg"))
            self.btn_eye.setIconSize(QSize(28, 28))

        else:

            self.LineE_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_eye.setIcon(QIcon("p_Images/eye_close.png"))
            self.btn_eye.setIconSize(QSize(20, 20))

    def show_error(self, message):

        self.lbl_error.setText(message)
        self.lbl_error.setVisible(True)

    def hide_error(self):
        self.lbl_error.setText("")
        self.lbl_error.setVisible(False)

    def login(self):
        username = self.LineE_tendangnhap.text()
        password = self.LineE_matkhau.text()

        if username == "" or password == "":
            self.show_error("Vui lòng nhập tên đăng nhập và mật khẩu")
            return

        if len(username) < 4 or len(username) > 20:
            self.show_error("Tên đăng nhập phải từ 4-20 ký tự")
            return

        if " " in username:
            self.show_error("Tên đăng nhập không được có khoảng trắng")
            return

        if username.startswith(".") or username.endswith("."):
            self.show_error("Tên đăng nhập không được bắt đầu hoặc kết thúc bằng dấu chấm")
            return

        if len(password) < 6 or len(password) > 20:
            self.show_error("Mật khẩu phải từ 6-20 ký tự")
            return

        if " " in password:
            self.show_error("Mật khẩu không được có khoảng trắng")
            return

        if password.startswith(".") or password.endswith("."):
            self.show_error("Mật khẩu không được bắt đầu hoặc kết thúc bằng dấu chấm")
            return

        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)

        if not (has_letter and has_number):
            self.show_error("Mật khẩu phải có chữ và số")
            return

        self.hide_error()

        try:

            with open("Data/accounts.json", "r", encoding="utf8") as f:
                data = json.load(f)

            found = False

            for user in data["users"]:

                if username == user["username"] and password == user["password"]:
                    found = True
                    break

            if found:
                print("Đăng nhập thành công")
            else:
                self.show_error("Sai tài khoản hoặc mật khẩu")
        except:

            self.show_error("Chưa có tài khoản được đăng ký")

        print("Đăng nhập thành công")
        self.hide()
    def open_register(self):

        self.reg = RegisterEx()
        self.reg.show()
        self.close()

    def open_reset(self):

        self.reset = ResetEx()
        self.reset.show()
        self.close()







