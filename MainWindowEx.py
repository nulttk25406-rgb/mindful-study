import sys
import json
import os.path 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (QApplication, QMainWindow, QListWidgetItem, 
                             QTableWidgetItem, QMessageBox)
from MainWindow import Ui_Mindfulstudy
from Nhiemvu import Nhiemvu
from Deadline import Deadline
from TKB import Thoikhoabieu

class MainWindowEx(Ui_Mindfulstudy):
    def __init__(self):
        self.file_dataTask = "data_task.json"
        self.file_dataDeadlines = "data_deadlines.json"
        self.file_dataTKB = "data_tkb.json"

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow 
        self.MainWindow.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.stackedWidget.setCurrentIndex(0) # Trang đầu tiên khi mở app
        self.setupSignalAndSlot()
    def show(self):
        self.MainWindow.show()    
        
        # tải dữ liệu
        self.processLoadData()

    def setupSignalAndSlot(self):
        self.btn_minimize.clicked.connect(self.processMinimize)
        self.btn_maximize.clicked.connect(self.processMaximize)
        self.btn_close.clicked.connect(self.processClose)

    # kết nối nút chuyển trang     
        self.btn_home.clicked.connect(self.processChuyenTrangHome)
        self.btn_deadlines.clicked.connect(self.processChuyenTrangDeadlines)
        self.btn_thoikhoabieu.clicked.connect(self.processChuyenTrangThoiKhoaBieu)
        self.btn_taptrung.clicked.connect(self.processChuyenTrangTapTrung)
       

    # kết nối nút chuyển trang 0    
        self.btn_them1.clicked.connect(self.processAddTask)
        self.lineEdit_nv.returnPressed.connect(self.processAddTask) 
        self.btn_xoa1.clicked.connect(self.processDeleteTask)
    # kết nối chuyển trang 1
        self.btn_them2.clicked.connect(self.processAddDeadline)
        self.btn_xoa2.clicked.connect(self.processDeleteDeadline)
        self.btn_luu.clicked.connect(self.processAutoSaveDeadline)
        self.btn_dong.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        
        self.tableWidget.itemChanged.connect(self.processAutoSaveTKB)
        #xóa và thêm tkb 
        self.shortcut_xoa_tkb = QShortcut(QKeySequence("Delete"), self.tableWidget)
        self.shortcut_xoa_tkb.activated.connect(self.processDeleteTKB)

    def processChuyenTrangHome(self):
        self.stackedWidget.setCurrentIndex(0)
    def processChuyenTrangDeadlines(self):
        self.stackedWidget.setCurrentIndex(1)
    def processChuyenTrangThoiKhoaBieu(self):
        self.stackedWidget.setCurrentIndex(2)
    def processChuyenTrangTapTrung(self) :
        self.stackedWidget.setCurrentIndex(3)
        # để không bị vòng lặp 
        self.listWidget_taptrung.clear()
        #lấy danh sách từ trang 0 qua trang 3
        for i in range (self.listWidget_nv.count()):
            item_text_nv = self.listWidget_nv .item (i).text()
            self.listWidget_taptrung.addItem (item_text_nv)
        # lấy danh sách từ trang 1 qua trang 3    
        for i in range(self.listWidget_dl.count()):
            item_text_dl = self.listWidget_dl.item(i).text()
            self.listWidget_taptrung.addItem(item_text_dl)



    # kết nối các nút cửa sổ 
    def processMinimize(self):
        self.MainWindow.showMinimized() 

    def processMaximize(self):
        if self.MainWindow.isMaximized():
            self.MainWindow.showNormal()
        else:
            self.MainWindow.showMaximized()
 
    def processClose(self):
        msg = QMessageBox()
        msg.setText("Bạn có chắc chắn muốn thoát ứng dụng không?")
        msg.setWindowTitle("Xác nhận thoát")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()


    # thêm nhiệm vụ
    def processAddTask(self):
        ten = self.lineEdit_nv.text().strip()
        if ten == "" :
            QMessageBox.warning(self.MainWindow,"Thiếu thông tin","Bạn chưa nhập thông tin" )
            return 
        obj = Nhiemvu(ten)
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, obj)
        item.setText(str(obj)) 
        self.listWidget_nv.addItem(item)
        self.lineEdit_nv.setText("")
        self.lineEdit_nv.setFocus()
        self.processAutoSaveTask()
    #thêm deadline 
    def processAddDeadline(self):
                ten_deadline = self.lineEdit_dl.text().strip()
                if ten_deadline == "":
                  QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Bạn chưa nhập tên deadline")
                  return
                ngay_gio = self.dateTimeEdit.dateTime().toString("dd/MM/yyyy HH:mm")
                obj = Deadline(ten_deadline, ngay_gio)
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, obj)
                item.setText(str(obj))
                self.listWidget_dl.addItem(item)
                self.lineEdit_dl.setText("")
                self.lineEdit_dl.setFocus()
               
        
# xóa nhiệm vụ
    def processDeleteTask(self):
        row = self.listWidget_nv.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Bạn chưa click chọn nhiệm vụ nào để xóa!")
            return          
        msg = QMessageBox()
        msg.setText("Bạn có chắc chắn muốn xóa nhiệm vụ này không?")
        msg.setWindowTitle("Xác nhận")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)       
        if msg.exec() == QMessageBox.StandardButton.Yes:
                self.listWidget_nv.takeItem(row)      
                self.processAutoSaveTask()

# xóa deadline
    def processDeleteDeadline(self):
        row = self.listWidget_dl.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Bạn chưa click chọn deadline nào để xóa!")
            return       
        msg = QMessageBox()
        msg.setText("Bạn có chắc chắn muốn xóa deadline này không?")
        msg.setWindowTitle("Xác nhận")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)       
        if msg.exec() == QMessageBox.StandardButton.Yes:
                self.listWidget_dl.takeItem(row)

# xóa tkb
    def processDeleteTKB(self):
        for item in self.tableWidget.selectedItems():
            item.setText("") 

  
    # Lưu tự động
    def processAutoSaveTask(self):
        ds = [self.listWidget_nv.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.listWidget_nv.count())]
        with open(self.file_dataTask, "w", encoding="utf-8") as f:
            f.write(json.dumps([o.__dict__ for o in ds], ensure_ascii=False, indent=4))

    def processAutoSaveDeadline(self):
        ds = [self.listWidget_dl.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.listWidget_dl.count())]
        with open(self.file_dataDeadlines, "w", encoding="utf-8") as f:
            f.write(json.dumps([o.__dict__ for o in ds], ensure_ascii=False, indent=4))
            QMessageBox.information(self.MainWindow, "Thành công", "Đã lưu toàn bộ Deadlines!")
    

    def processAutoSaveTKB(self):
        ds_tkb = []
        for r in range(self.tableWidget.rowCount()):
           for c in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(r, c)
                if item is not None and item.text().strip() != "":
                    obj = Thoikhoabieu(r,c, item.text().strip())
                    ds_tkb.append(obj)   
        with open(self.file_dataTKB, "w", encoding="utf-8") as f:
            f.write(json.dumps([o.__dict__ for o in ds_tkb], ensure_ascii=False, indent=4))

    #Đọc dữ liệu json sang đối tượng 
    def processLoadData(self):
        # task 
        if os.path.isfile(self.file_dataTask):
            with open(self.file_dataTask, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.loads(f.read(), object_hook=lambda d: Nhiemvu(**d))
                    for obj in raw_data:
                        item = QListWidgetItem()
                        item.setData(Qt.ItemDataRole.UserRole, obj)
                        item.setText(str(obj))
                        self.listWidget_nv.addItem(item)
                except Exception as e: print("Lỗi Tải Nhiệm vụ:", e)

        #deadlines
        if os.path.isfile(self.file_dataDeadlines):
            with open(self.file_dataDeadlines, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.loads(f.read(), object_hook=lambda d: Deadline(**d))
                    for obj in raw_data:
                        item = QListWidgetItem()
                        item.setData(Qt.ItemDataRole.UserRole, obj)
                        item.setText(str(obj))
                        self.listWidget_dl.addItem(item)
                except Exception as e: print("Lỗi Tải Deadlines:", e)

        # tkb
        if os.path.isfile(self.file_dataTKB):
            with open(self.file_dataTKB, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.loads(f.read(), object_hook=lambda d: Thoikhoabieu(**d))
                    
                    self.tableWidget.blockSignals(True) 
                    
                    for obj in raw_data:
                        item = QTableWidgetItem(str(obj))
                        item.setData(Qt.ItemDataRole.UserRole, obj)
                        self.tableWidget.setItem(obj.row, obj.col, item)    
                    self.tableWidget.blockSignals(False)
                except Exception as e: print("Lỗi tải TKB:", e)

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MainWindowEx()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())