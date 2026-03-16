import sys
from PyQt6.QtWidgets import QApplication
from main44 import AILogic  # Import class xử lý từ file main_ai.py


def main():
    # 1. Khởi tạo ứng dụng Qt
    app = QApplication(sys.argv)

    # 2. Tạo đối tượng xử lý Logic AI
    window = AILogic()

    # 3. Căn giữa cửa sổ trên màn hình người dùng
    # Lấy thông số màn hình và tính toán vị trí tâm
    screen_geometry = window.screen().availableGeometry()
    center_point = screen_geometry.center()

    # Lấy khung của cửa sổ và di chuyển tâm khung vào tâm màn hình
    window_frame = window.frameGeometry()
    window_frame.moveCenter(center_point)

    # Di chuyển cửa sổ thật đến tọa độ đã tính
    window.move(window_frame.topLeft())

    # 4. Hiển thị cửa sổ
    window.show()

    # 5. Giữ ứng dụng luôn chạy
    sys.exit(app.exec())


if __name__ == "__main__":
    main()