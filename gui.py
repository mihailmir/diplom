# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mlp import SQLITE_DB, INPUT_PARAMETERS


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class NotEmptyValidator(QtGui.QValidator):
    def validate(self, text, pos):
        state = QtGui.QIntValidator.Acceptable if bool(text) else QtGui.QValidator.Invalid
        return state, text, pos


class UiDialog(QtWidgets.QWidget):
    trigger = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui(self)

    def setup_ui(self, Dialog):
        fields_count = 7
        field_pattern = 'lineEdit_{}'
        self.input_fields = []
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 261, 341, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 181, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit_0 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_0.setGeometry(QtCore.QRect(200, 20, 141, 22))
        self.lineEdit_0.setObjectName(_fromUtf8("Buying price"))
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(200, 50, 141, 22))
        self.lineEdit_1.setObjectName(_fromUtf8("Maintenance price"))
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 80, 141, 22))
        self.lineEdit_2.setObjectName(_fromUtf8("Doors"))
        int_validator = QtGui.QIntValidator(self.lineEdit_2)
        self.lineEdit_2.setValidator(int_validator)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(200, 110, 141, 22))
        self.lineEdit_3.setObjectName(_fromUtf8("Persons"))
        int_validator = QtGui.QIntValidator(self.lineEdit_3)
        self.lineEdit_3.setValidator(int_validator)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(200, 140, 141, 22))
        self.lineEdit_4.setObjectName(_fromUtf8("Lug boot"))
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(200, 170, 141, 22))
        self.lineEdit_5.setObjectName(_fromUtf8("Safety"))
        self.lineEdit_6= QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(200, 200, 141, 22))
        self.lineEdit_6.setObjectName(_fromUtf8("class"))
        self.label_0 = QtWidgets.QLabel(Dialog)
        self.label_0.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.label_0.setObjectName(_fromUtf8("label_0"))
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(30, 50, 121, 16))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 81, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 81, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 170, 81, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 210, 81, 16))
        self.error_dialog = QtWidgets.QErrorMessage()

        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.retranslate_ui(Dialog)

        for num in range(fields_count):
            self.input_fields.append(getattr(self, field_pattern.format(num)))

        self.buttonBox.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.update_db)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def update_db(self):
        for index, field in enumerate(self.input_fields):
            field_name = field.objectName()
            state, text, poss = NotEmptyValidator().validate(field.text(), index)
            if state == QtGui.QValidator.Invalid:
                self.error_dialog.showMessage('Field {} is not valid.'.format(field_name))
                return

        converted_fields = [field.text() for field in self.input_fields]
        cursor = SQLITE_DB.cursor()
        cursor.execute(
            "insert into cars ({}) values ({}) ".format(
                ", ".join(INPUT_PARAMETERS), ", ".join(['?' for par in INPUT_PARAMETERS])
            ), converted_fields
        )
        SQLITE_DB.commit()
        self.error_dialog.showMessage('DataBase updated successfully. Fields: {}'.format(", ".join(converted_fields)))

    def retranslate_ui(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "UPDATE", None))
        self.label_0.setText(_translate("Dialog", "Buying price", None))
        self.label_1.setText(_translate("Dialog", "Maintenance price", None))
        self.label_2.setText(_translate("Dialog", "Doors count", None))
        self.label_3.setText(_translate("Dialog", "Persons count", None))
        self.label_4.setText(_translate("Dialog", "Lug boot", None))
        self.label_5.setText(_translate("Dialog", "Safety", None))
        self.label_6.setText(_translate("Dialog", "Car Class ", None))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = UiDialog()
    ex.show()
    sys.exit(app.exec_())