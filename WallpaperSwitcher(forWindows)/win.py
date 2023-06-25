from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

class EditWin(QObject):
    def setupUi(self, EditWin, save_fun, main_path):
        self.savefun = save_fun
        self.main_path = main_path
        if not EditWin.objectName():
            EditWin.setObjectName(u"EditWin")
        EditWin.resize(350, 200)
        EditWin.setMinimumSize(QSize(350, 200))
        EditWin.setMaximumSize(QSize(350, 200))
        self.label = QLabel(EditWin)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 351, 51))
        font = QFont()
        font.setFamily(u"\u534e\u6587\u4e2d\u5b8b")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(141, 136, 185, 255), stop:1 rgba(255, 255, 255, 255));")
        self.layoutWidget = QWidget(EditWin)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 60, 291, 81))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.longitude = QLineEdit(self.layoutWidget)
        self.longitude.setObjectName(u"longitude")
        self.longitude.setEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.longitude)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.latitude = QLineEdit(self.layoutWidget)
        self.latitude.setObjectName(u"latitude")
        self.latitude.setEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.latitude)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.timezone = QLineEdit(self.layoutWidget)
        self.timezone.setObjectName(u"timezone")
        self.timezone.setEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.timezone)

        self.label_1 = QLabel(self.layoutWidget)
        self.label_1.setObjectName(u"label_1")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_1)

        self.yes = QPushButton(EditWin)
        self.yes.setObjectName(u"yes")
        self.yes.setGeometry(QRect(240, 160, 75, 23))
        self.yes.clicked.connect(self.button_action)

        self.retranslateUi(EditWin)

        QMetaObject.connectSlotsByName(EditWin)
    # setupUi

    def retranslateUi(self, EditWin):
        EditWin.setWindowTitle(QCoreApplication.translate("EditWin", u"WallpaperSwitcher-Edit", None))
        self.label.setText(QCoreApplication.translate("EditWin", u"  \u7f16\u8f91", None))
        self.label_2.setText(QCoreApplication.translate("EditWin", u"\u7eac\u5ea6", None))
        self.label_3.setText(QCoreApplication.translate("EditWin", u"\u65f6\u533a", None))
        self.label_1.setText(QCoreApplication.translate("EditWin", u"\u7ecf\u5ea6", None))
        self.yes.setText(QCoreApplication.translate("EditWin", u"\u786e\u5b9a", None))
    # retranslateUi
    def button_action(self):
        result = [{'longitude': float(self.longitude.text()),\
              'latitude': float(self.latitude.text())},\
              int(self.timezone.text())]
        self.savefun(result[0], result[1])
        os.startfile(self.main_path)
        self.saved.emit()
        self.hide()
        

def edit_parameter(save_fun, main_path):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) 
    app = QApplication([])
    qwindow = QMainWindow()
    window = EditWin()
    window.setupUi(qwindow, save_fun, main_path)
    qwindow.show()
    app.exec_()
