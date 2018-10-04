# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_2.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from base.base import Main
import os
import threading

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(360, 333)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 54, 12))
        self.label_3.setObjectName("label_3")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 261, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        # api key
        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        # secret key
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")


        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 262, 61, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.reload)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(290, 19, 61, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.showMsg)

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(80, 310, 251, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 210, 61, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.stop)

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(290, 160, 61, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        # 定义开始按钮的线程
        self.tread_01 = Work1()
        self.pushButton_4.clicked.connect(self.run)
        
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 110, 61, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.alfa)

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 120, 251, 181))
        self.textEdit.setObjectName("textEdit")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 310, 40, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OKEx网格交易机器人 v0.1"))
        self.label_3.setText(_translate("Form", "控制台："))
        self.label.setText(_translate("Form", "api key:"))
        self.label_2.setText(_translate("Form", "secret key:"))
        self.pushButton_2.setText(_translate("Form", "重启"))
        self.pushButton.setText(_translate("Form", "更新密匙"))
        self.label_4.setText(_translate("Form", "其实根本没有孙笑川,或者说人人都是孙笑川"))
        self.pushButton_3.setText(_translate("Form", "强制退出"))
        self.pushButton_4.setText(_translate("Form", "开始"))
        self.pushButton_5.setText(_translate("Form", "全部撤单"))
        self.label_5.setPixmap(QtGui.QPixmap(r'image\anpai.png'))

    def showMsg(self, Form):
        widget = QtWidgets.QWidget()
        secret_key = self.lineEdit.text()
        api_key = self.lineEdit_2.text()
        main = Main()
        if main.update_key(api_key, secret_key):
            QtWidgets.QMessageBox.information(widget, '信息提示框', '可以给你更新密匙，但是没必要。')
            self.textEdit.append("密匙已更新")
        else:
            self.textEdit.append("你更个锤子更，更新失败！")

    def alfa(self):
        print("开始撤单")
        main = Main()
        try:
            response =  main.alfa('show_usdt', 10)
            if response:
                self.textEdit.append("当前没有挂单")
            else:
                self.textEdit.append("撤单成功")    
        except:
            self.textEdit.append("出错了！\n先检查您的密匙是否更新\n再检查VPN是否正常")

    def run(self, Form):
        # 按钮4不可点击
#        self.pushButton_4.setEnabled(False)
        self.textEdit.append("*****开始挂单*****\n如果没有挂单成功请检查你的密匙和VPN\n")
        self.tread_01.start()


    def stop(self, Form):
        print("你把你闪现给我交了！")
        os._exit(0)

    def reload(self, Form):
        self.textEdit.append("对不起，这个功能还在开发中..\n")

class Work1(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(Work1, self).__init__()

    def run(self):
        #开始进行循环
        self.run = Main()
        try:
            self.run.main('show_usdt', 'show', 10)
        except:
            print("出错了，你个铁憨憨，请检查密匙是否正确，或者代理链接是否正常！")
        # 循环完毕后发出信号
        self.trigger.emit()


if __name__ == '__main__':
    run = Ui_Form()
    run.alfa()
