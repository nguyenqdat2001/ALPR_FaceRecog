import sys
import cv2
import numpy as np
import datetime
import time

from cropnumber import read_plate
from imageprocessing import detection_plate
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets
from UI_Main import Ui_MainWindow
from UI_History import Ui_WindowLichSu
from SVM import SVM
from database import Database
from Serial_arduino import Serial_Arduino
from face_rec import Face_Rec
from imutils.video import VideoStream
import imutils

path_load_cudnn = "Pictures/013.png"
imgcudnn = cv2.imread(path_load_cudnn)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.model = SVM()
        self.face_rec = Face_Rec()
        self.imgloadcudnn, self.naneloadcudnn = self.face_rec.Rec(imgcudnn)
        self.arduino = Serial_Arduino()
        self.database = Database()
        self.gl_rfid = ""
        self.gl_bsx_vao = ""
        self.gl_bsx_ra = ""
        self.gl_name_vao = ""
        self.gl_name_ra = ""
        self.gl_img_vehicle_vao = None
        self.gl_img_vehicle_ra = None
        self.gl_img_face_ra = None
        self.gl_img_face_vao = None
        self.gl_temp_name_ra = None
        self.gl_temp_name_vao = None
        self.thread = {}
        self.uic.btn_stop_vao.setEnabled(False)
        self.uic.btn_stop_ra.setEnabled(False)
        self.uic.btn_stop_face_vao.setEnabled(False)
        self.uic.btn_stop_face_ra.setEnabled(False)
        self.uic.btn_history.clicked.connect(self.open_history)
        self.uic.btn_start_vao.clicked.connect(self.start_video_vao)
        self.uic.btn_stop_vao.clicked.connect(self.stop_video_vao)
        self.uic.btn_start_ra.clicked.connect(self.start_video_ra)
        self.uic.btn_stop_ra.clicked.connect(self.stop_video_ra)
        self.uic.btn_start_face_vao.clicked.connect(self.start_face_vao)
        self.uic.btn_stop_face_vao.clicked.connect(self.stop_face_vao)
        self.uic.btn_start_face_ra.clicked.connect(self.start_face_ra)
        self.uic.btn_stop_face_ra.clicked.connect(self.stop_face_ra)
        self.uic.btn_open_vao.clicked.connect(self.open_vao)
        self.uic.btn_open_ra.clicked.connect(self.open_ra)

    def open_history(self):
        self.History_window = QtWidgets.QMainWindow()
        self.uic_hsr = Ui_WindowLichSu()
        self.uic_hsr.setupUi(self.History_window)
        self.History_window.show()
        self.uic_hsr.tb_lichsu.setColumnWidth(0, 160)
        self.uic_hsr.tb_lichsu.setColumnWidth(1, 160)
        self.uic_hsr.tb_lichsu.setColumnWidth(2, 115)
        self.uic_hsr.tb_lichsu.setColumnWidth(3, 160)
        self.loaddata(self.database.Get_Data_TB())
        self.uic_hsr.tb_lichsu.doubleClicked.connect(self.rowselect)
        self.uic_hsr.btn_tim_bsx.clicked.connect(self.timbsx)
        self.uic_hsr.btn_refresh.clicked.connect(self.refreshtable)

    def loaddata(self, data):
        tablerow = 0
        self.uic_hsr.tb_lichsu.setRowCount(len(data))
        for row in data:
            self.uic_hsr.tb_lichsu.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.uic_hsr.tb_lichsu.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.uic_hsr.tb_lichsu.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.uic_hsr.tb_lichsu.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            tablerow += 1

    def rowselect(self):
        for item in self.uic_hsr.tb_lichsu.selectedItems():
            row = item.row()
            bsx = self.uic_hsr.tb_lichsu.item(row, 0)
            stt = self.uic_hsr.tb_lichsu.item(row, 1)
            time = self.uic_hsr.tb_lichsu.item(row, 2)
            name = self.uic_hsr.tb_lichsu.item(row, 3)
            time_convert = datetime.datetime.strptime(time.text(), '%Y-%m-%d %H:%M:%S.%f')
            path_vehicle = "History/Vehicle/" + stt.text() + "_" + name.text() + "_" + bsx.text() + "_" + str(
                time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                time_convert.minute) + ".jpg"
            path_face = "History/Face/" + stt.text() + "_" + name.text() + "_" + bsx.text() + "_" + str(
                time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                time_convert.minute) + ".jpg"
            img_vehicle_history = cv2.imread(path_vehicle)
            img_face_history = cv2.imread(path_face)
            self.show_img_history(img_vehicle_history, img_face_history)

    def timbsx(self):
        bsx = self.uic_hsr.te_bsx.toPlainText()
        self.loaddata(self.database.Search_Plate(bsx))

    def refreshtable(self):
        self.loaddata(self.database.Get_Data_TB())

    def open_vao(self):
        if self.arduino.status == 1:
            self.arduino.write_arduino('0')
        CustomMessageBox.showWithTimeout(3, "Mở cổng vào", "CẢNH BÁO (Đóng sau 3s)",
                                         icon=QMessageBox.Warning)

    def open_ra(self):
        if self.arduino.status == 1:
            self.arduino.write_arduino('1')
        CustomMessageBox.showWithTimeout(3, "Mở cổng ra", "CẢNH BÁO (Đóng sau 3s)",
                                         icon=QMessageBox.Warning)

    def show_bsx_vao(self, img):
        info_plate = self.model.readchar(read_plate(img))
        self.gl_bsx_vao = info_plate
        self.uic.lb_bsx_vao.setText(info_plate)
        # self.arduino.write_arduino()

    def show_bsx_ra(self, img):
        info_plate = self.model.readchar(read_plate(img))
        self.gl_bsx_ra = info_plate
        self.uic.lb_bsx_ra.setText(info_plate)

    def show_name_vao(self, imgname):
        _, name = self.face_rec.Rec(imgname)
        self.gl_name_vao = name
        # print("face vao:",self.gl_name_vao)
        self.uic.lb_name_vao.setText(name)
        self.save_database_face_vao(name)

    def show_name_ra(self, imgname):
        _, name = self.face_rec.Rec(imgname)
        self.gl_name_ra = name
        # print("face ra:", self.gl_name_ra)
        self.uic.lb_name_ra.setText(name)
        self.show_tt(name)
        self.save_database_face_ra(name)

    def show_tt(self, msv=''):
        if msv != "No Face" and msv != "Unknown":
            try:
                bsgd = self.database.Get_BSGD(msv)
            except:
                bsgd = "Không có dữ liệu"
            self.uic.lb_tt_ten.setText(self.database.Search_TT(msv)[0][0])
            self.uic.lb_tt_msv.setText(msv)
            self.uic.lb_tt_khoa.setText(self.database.Search_TT(msv)[0][2])
            self.uic.lb_tt_lop.setText(self.database.Search_TT(msv)[0][3])
            self.uic.lb_tt_bsgd.setText(bsgd)

    def save_database_face_vao(self, ten):
        try:
            bsx, status, time, name = self.database.Get_Data_DB(ten)
            if status == '0' and ten != "No Face" and ten != "Unknown":
                time_convert = datetime.datetime.now()
                path_save_xe_vao = "History/Vehicle/1_" + self.gl_name_vao + "_" + self.gl_bsx_vao + "_" + str(
                    time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                    time_convert.minute) + ".jpg"
                path_save_face_vao = "History/Face/1_" + self.gl_name_vao + "_" + self.gl_bsx_vao + "_" + str(
                    time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                    time_convert.minute) + ".jpg"
                cv2.imwrite(path_save_xe_vao, self.gl_img_vehicle_vao)
                cv2.imwrite(path_save_face_vao, self.gl_img_face_vao)
                self.database.Insert_Or_Update_DB(self.gl_bsx_vao, '1', time_convert, self.gl_name_vao)
                self.gl_temp_name_vao = self.gl_name_vao
                self.open_vao()
                self.stop_face_vao()

        except:
            if ten != "No Face" and ten != "Unknown":
                time_convert = datetime.datetime.now()
                path_save_xe_vao = "History/Vehicle/1_" + self.gl_name_vao + "_" + self.gl_bsx_vao + "_" + str(
                    time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                    time_convert.minute) + ".jpg"
                path_save_face_vao = "History/Face/1_" + self.gl_name_vao + "_" + self.gl_bsx_vao + "_" + str(
                    time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                    time_convert.minute) + ".jpg"
                cv2.imwrite(path_save_xe_vao, self.gl_img_vehicle_vao)
                cv2.imwrite(path_save_face_vao, self.gl_img_face_vao)
                self.database.Insert_Or_Update_DB(self.gl_bsx_vao, '1', time_convert, self.gl_name_vao)
                self.gl_temp_name_vao = self.gl_name_vao
                self.open_vao()
                self.stop_face_vao()

    def save_database_face_ra(self, ten):
        try:
            bsx, status, time, name = self.database.Get_Data_DB(ten)
            if status == "1" and ten != "No Face" and ten != "Unknown":
                self.uic.lb_name_history.setText(name)
                self.uic.lb_bsx_ra_uid.setText(bsx)
                time_convert = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
                path_save_xe = "History/Vehicle/1_" + self.gl_name_vao + "_" + self.gl_bsx_vao + "_" + str(
                    time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                    time_convert.minute) + ".jpg"
                path_save_face = "History/Face/1_" + self.gl_name_vao + "_" + self.gl_bsx_vao + "_" + str(
                    time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                    time_convert.minute) + ".jpg"
                img_vehicle_save = cv2.imread(path_save_xe)
                img_face_save = cv2.imread(path_save_face)
                self.show_face_save(img_face_save)
                self.show_img_save(img_vehicle_save)

                if bsx == self.gl_bsx_ra:
                    self.database.Insert_Or_Update_DB(self.gl_bsx_ra, '0', datetime.datetime.now(), self.gl_name_ra)
                    time_convert = datetime.datetime.now()
                    path_save_vehicle_ra = "History/Vehicle/0_" + self.gl_name_ra + "_" + self.gl_bsx_ra + "_" + str(
                        time_convert.year) + str(
                        time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                        time_convert.minute) + ".jpg"
                    path_save_face_ra = "History/Face/0_" + self.gl_name_ra + "_" + self.gl_bsx_ra + "_" + str(
                        time_convert.year) + str(
                        time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                        time_convert.minute) + ".jpg"
                    cv2.imwrite(path_save_vehicle_ra, self.gl_img_vehicle_ra)
                    cv2.imwrite(path_save_face_ra, self.gl_img_face_ra)
                    self.gl_temp_name_ra = self.gl_name_ra
                    self.open_ra()
                    self.stop_face_ra()
                else:
                    self.stop_face_ra()
                    mess = QMessageBox.question(self, "CẢNH BÁO", "Biển số xe không giống khi vào!!! \n Bạn có muốn mở của không ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if mess == QMessageBox.Yes:
                        self.database.Insert_Or_Update_DB(self.gl_bsx_ra, '0', datetime.datetime.now(), self.gl_name_ra)
                        time_convert = datetime.datetime.now()
                        path_save_vehicle_ra = "History/Vehicle/0_" + self.gl_name_ra + "_" + self.gl_bsx_ra + "_" + str(
                            time_convert.year) + str(
                            time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                            time_convert.minute) + ".jpg"
                        path_save_face_ra = "History/Face/0_" + self.gl_name_ra + "_" + self.gl_bsx_ra + "_" + str(
                            time_convert.year) + str(
                            time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(
                            time_convert.minute) + ".jpg"
                        cv2.imwrite(path_save_vehicle_ra, self.gl_img_vehicle_ra)
                        cv2.imwrite(path_save_face_ra, self.gl_img_face_ra)
                        self.gl_temp_name_ra = self.gl_name_ra
                        self.open_ra()
        except:
            x = 0

    def closeEvent(self, event):
        try:
            self.stop_video()
            if self.arduino.status == 1:
                self.thread[2].stop()
            self.arduino.close_arduino()
        except:
            pass

    def stop_video_vao(self):
        self.uic.btn_stop_vao.setEnabled(False)
        self.uic.btn_start_vao.setEnabled(True)
        self.thread[1].stop()

    def stop_video_ra(self):
        self.uic.btn_stop_ra.setEnabled(False)
        self.uic.btn_start_ra.setEnabled(True)
        self.thread[3].stop()

    def stop_face_vao(self):
        self.uic.btn_stop_face_vao.setEnabled(False)
        self.uic.btn_start_face_vao.setEnabled(True)
        self.thread[4].stop()

    def stop_face_ra(self):
        self.uic.btn_stop_face_ra.setEnabled(False)
        self.uic.btn_start_face_ra.setEnabled(True)
        self.thread[2].stop()

    def start_video_vao(self):
        self.uic.btn_start_vao.setEnabled(False)
        self.uic.btn_stop_vao.setEnabled(True)
        self.thread[1] = thread_capture_video(index=1, path='Video\Video_Vao.mp4')
        self.thread[1].start()
        self.thread[1].signal_img.connect(self.show_webcam_vao)
        self.thread[1].signal_imgplate.connect(self.show_bsx_vao)

    def start_video_ra(self):
        self.uic.btn_start_ra.setEnabled(False)
        self.uic.btn_stop_ra.setEnabled(True)
        self.thread[3] = thread_capture_video(index=3, path='Video\Video_Ra.mp4')
        self.thread[3].start()
        self.thread[3].signal_img.connect(self.show_webcam_ra)
        self.thread[3].signal_imgplate.connect(self.show_bsx_ra)

    def start_face_vao(self):
        self.uic.btn_start_face_vao.setEnabled(False)
        self.uic.btn_stop_face_vao.setEnabled(True)
        self.thread[4] = thread_capture_face(index=4, path='Video/camtest.mp4')
        self.thread[4].start()
        self.thread[4].signal_img.connect(self.show_webcam_face_vao)
        self.thread[4].signal_imgname.connect(self.show_name_vao)

    def start_face_ra(self):
        self.uic.btn_start_face_ra.setEnabled(False)
        self.uic.btn_stop_face_ra.setEnabled(True)
        self.thread[2] = thread_capture_face(index=2, path='Video/camtest.mp4')
        self.thread[2].start()
        self.thread[2].signal_img.connect(self.show_webcam_face_ra)
        self.thread[2].signal_imgname.connect(self.show_name_ra)

    def show_webcam_face_vao(self, cv_img):
        self.gl_img_face_vao = cv_img
        qt_img = self.convert_cv_qt_face(cv_img)
        self.uic.lb_screen_face_vao.setPixmap(qt_img)

    def show_webcam_face_ra(self, cv_img):
        self.gl_img_face_ra = cv_img
        qt_img = self.convert_cv_qt_face(cv_img)
        self.uic.lb_screen_face_ra.setPixmap(qt_img)

    def show_webcam_vao(self, cv_img):
        self.gl_img_vehicle_vao = cv_img
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.lb_screen_Vao.setPixmap(qt_img)

    def show_webcam_ra(self, cv_img):
        self.gl_img_vehicle_ra = cv_img
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.lb_screen_Ra.setPixmap(qt_img)

    def show_img_save(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.lb_screen_img_uid.setPixmap(qt_img)

    def show_face_save(self, cv_img):
        qt_img = self.convert_cv_qt_face(cv_img)
        self.uic.lb_screen_face_history.setPixmap(qt_img)

    def show_img_history(self, cv_img, img_face):
        qt_img_face = self.convert_cv_qt_face(img_face)
        qt_img = self.convert_cv_qt(cv_img)
        self.uic_hsr.lb_screen_database.setPixmap(qt_img)
        self.uic_hsr.lb_screen_database_face.setPixmap(qt_img_face)

    def convert_cv_qt(self, cv_img):
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(472, 304, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def convert_cv_qt_face(self, cv_img):
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(320, 240, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class thread_arduino_rfid(QThread):
    signal_rfid = pyqtSignal(str)

    def __init__(self, index, arduino):
        self.index = index
        self.arduino = arduino  # Serial_Arduino()
        print("Start Threading ", self.index)
        super(thread_arduino_rfid, self).__init__()

    def run(self):
        while 1:
            if self.arduino.status == 1:
                rfid = self.arduino.read_serial()
                if rfid != "":
                    self.signal_rfid.emit(rfid)

    def stop(self):
        print("Stop Threading", self.index)
        self.terminate()


class thread_capture_video(QThread):
    signal_img = pyqtSignal(np.ndarray)
    signal_imgplate = pyqtSignal(np.ndarray)

    def __init__(self, index, path):
        self.cap = None
        self.index = index
        self.path = path
        print("Start Threading ", self.index)
        super(thread_capture_video, self).__init__()

    def run(self):
        self.cap = cv2.VideoCapture(self.path)  # 'Video\VideoTest.mp4'
        checkimg = 0
        while True:
            ret, img = self.cap.read()
            if ret:
                check, imgPlate, imgVehicleDraw = detection_plate(img)
                # print("Bien xe: ", model.readchar(read_plate(imgPlate)))
                self.signal_img.emit(imgVehicleDraw)
                if checkimg == 20:
                    if check == 1:
                        self.signal_imgplate.emit(imgPlate)
                    checkimg = 0
            checkimg = checkimg + 1
            time.sleep(0.01)

    def stop(self):
        self.cap.release()
        print("Stop Threading", self.index)
        self.terminate()


class thread_capture_face(QThread):
    signal_img = pyqtSignal(np.ndarray)
    signal_imgname = pyqtSignal(np.ndarray)

    def __init__(self, index, path):
        self.cap = None
        self.index = index
        self.path = path
        print("Start Threading ", self.index)
        super(thread_capture_face, self).__init__()

    def run(self):
        # cap = cv2.VideoCapture(self.path)  # 'Video\VideoTest.mp4'
        self.cap = VideoStream(src=0).start()
        checkimg = 0
        while True:
            img = self.cap.read()
            img = imutils.resize(img, width=320)
            if 1:
                # imgface, name = self.face_rec.Rec(img)
                self.signal_img.emit(img)
                if checkimg == 60:
                    self.signal_imgname.emit(img)
                    checkimg = 0
                checkimg = checkimg + 1
            time.sleep(0.01)

    def stop(self):
        print("Stop Threading", self.index)
        self.terminate()


class CustomMessageBox(QMessageBox):
    def __init__(self, *__args):
        QMessageBox.__init__(self)
        self.timeout = 0
        self.autoclose = False
        self.currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoclose:
            self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.done(0)

    @staticmethod
    def showWithTimeout(timeoutSeconds, message, title, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        w = CustomMessageBox()
        w.autoclose = True
        w.timeout = timeoutSeconds
        w.setText(message)
        w.setWindowTitle(title)
        w.setIcon(icon)
        w.setStandardButtons(buttons)
        w.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

# pyuic5 -x ui_nhandienbsx.ui -o UI_Main.py
# pyuic5 -x ui_history.ui -o UI_History.py
