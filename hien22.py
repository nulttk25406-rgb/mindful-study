import sys
from PyQt6.QtWidgets import QApplication
from main22 import ChartLogic  # Nhập class từ file logic của bạn


def main():
    # 1. Tạo thực thể ứng dụng (Bắt buộc cho mọi app PyQt)
    app = QApplication(sys.argv)

    # 2. Khởi tạo cửa sổ chính
    window = ChartLogic()

    # 3. Căn giữa cửa sổ trên màn hình khi mới mở
    center_window(window)

    # 4. Hiển thị cửa sổ
    window.show()

    # 5. Duy trì ứng dụng chạy cho đến khi người dùng đóng
    sys.exit(app.exec())


def center_window(window):
    """Hàm phụ trợ để đưa app ra giữa màn hình"""
    frame_gm = window.frameGeometry()
    screen = window.screen().availableGeometry().center()
    frame_gm.moveCenter(screen)
    window.move(frame_gm.topLeft())


if __name__ == "__main__":
    main()