# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_history.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WindowLichSu(object):
    def setupUi(self, WindowLichSu):
        WindowLichSu.setObjectName("WindowLichSu")
        WindowLichSu.resize(1139, 745)
        self.centralwidget = QtWidgets.QWidget(WindowLichSu)
        self.centralwidget.setObjectName("centralwidget")
        self.tb_lichsu = QtWidgets.QTableWidget(self.centralwidget)
        self.tb_lichsu.setEnabled(True)
        self.tb_lichsu.setGeometry(QtCore.QRect(15, 21, 611, 441))
        self.tb_lichsu.setObjectName("tb_lichsu")
        self.tb_lichsu.setColumnCount(4)
        self.tb_lichsu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_lichsu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_lichsu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_lichsu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_lichsu.setHorizontalHeaderItem(3, item)
        self.tb_lichsu.horizontalHeader().setCascadingSectionResizes(False)
        self.tb_lichsu.horizontalHeader().setSortIndicatorShown(False)
        self.tb_lichsu.verticalHeader().setCascadingSectionResizes(False)
        self.tb_lichsu.verticalHeader().setSortIndicatorShown(False)
        self.tb_lichsu.verticalHeader().setStretchLastSection(False)
        self.lb_screen_database = QtWidgets.QLabel(self.centralwidget)
        self.lb_screen_database.setGeometry(QtCore.QRect(640, 20, 470, 303))
        self.lb_screen_database.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_screen_database.setFrameShape(QtWidgets.QFrame.Panel)
        self.lb_screen_database.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lb_screen_database.setLineWidth(2)
        self.lb_screen_database.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_screen_database.setObjectName("lb_screen_database")
        self.te_bsx = QtWidgets.QTextEdit(self.centralwidget)
        self.te_bsx.setGeometry(QtCore.QRect(760, 660, 201, 41))
        self.te_bsx.setObjectName("te_bsx")
        self.btn_tim_bsx = QtWidgets.QPushButton(self.centralwidget)
        self.btn_tim_bsx.setGeometry(QtCore.QRect(970, 670, 75, 23))
        self.btn_tim_bsx.setObjectName("btn_tim_bsx")
        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(20, 470, 75, 23))
        self.btn_refresh.setObjectName("btn_refresh")
        self.lb_screen_database_face = QtWidgets.QLabel(self.centralwidget)
        self.lb_screen_database_face.setGeometry(QtCore.QRect(720, 340, 320, 240))
        self.lb_screen_database_face.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_screen_database_face.setFrameShape(QtWidgets.QFrame.Panel)
        self.lb_screen_database_face.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lb_screen_database_face.setLineWidth(2)
        self.lb_screen_database_face.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_screen_database_face.setObjectName("lb_screen_database_face")
        WindowLichSu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WindowLichSu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1139, 21))
        self.menubar.setObjectName("menubar")
        WindowLichSu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WindowLichSu)
        self.statusbar.setObjectName("statusbar")
        WindowLichSu.setStatusBar(self.statusbar)

        self.retranslateUi(WindowLichSu)
        QtCore.QMetaObject.connectSlotsByName(WindowLichSu)

    def retranslateUi(self, WindowLichSu):
        _translate = QtCore.QCoreApplication.translate
        WindowLichSu.setWindowTitle(_translate("WindowLichSu", "History"))
        self.tb_lichsu.setSortingEnabled(False)
        item = self.tb_lichsu.horizontalHeaderItem(0)
        item.setText(_translate("WindowLichSu", "Biển số xe"))
        item = self.tb_lichsu.horizontalHeaderItem(1)
        item.setText(_translate("WindowLichSu", "Tính trạng"))
        item = self.tb_lichsu.horizontalHeaderItem(2)
        item.setText(_translate("WindowLichSu", "Thời gian"))
        item = self.tb_lichsu.horizontalHeaderItem(3)
        item.setText(_translate("WindowLichSu", "Name"))
        self.lb_screen_database.setText(_translate("WindowLichSu", "Anh"))
        self.btn_tim_bsx.setText(_translate("WindowLichSu", "Tìm"))
        self.btn_refresh.setText(_translate("WindowLichSu", "Refresh"))
        self.lb_screen_database_face.setText(_translate("WindowLichSu", "Face"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WindowLichSu = QtWidgets.QMainWindow()
    ui = Ui_WindowLichSu()
    ui.setupUi(WindowLichSu)
    WindowLichSu.show()
    sys.exit(app.exec_())
