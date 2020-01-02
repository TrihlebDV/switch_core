#!/usr/bin/python3
# -*- coding: utf-8 -*-

#GUI libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

#necessary libraries
import sys

import time

#lib for drawing
import numpy as np
import cv2
import queue

#GUI form
import first_des
from SysHandl  import SysHandler,  Sender
from PostHandl import PostHandler, Spawer


class Implement(QtWidgets.QWidget, first_des.Ui_FORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.strObj1One = []
        for i in range(4):
            self.strObj1One.append("local:" + str(i))
        self.str_now = 0
        self.gl_seq = "global label\n"
        self.globalLabel.setText(self.gl_seq)
        self.sq = queue.Queue()
        self.pq = queue.Queue()
        self.put_start_img()
        self.thread = QThread()
        self.thread.start()
        self.sysHandler = SysHandler(self.sq, self.main_part)
        self.sysHandler.start()
        #self.sysHandler.moveToThread(self.thread)
        #self.sysHandler.run_trigger.emit()
        self.sender = Sender(self.sq)
        self.sender.start()
        self.instr = []
        for i in range(4):
            self.instr.append("key SERIAL PRIMARY KEY, data varchar(100), real int")
        self.postHandler = PostHandler(self.pq, self.sq, self.instr, quantity=4)
        self.postHandler.start()
        self.spawer = Spawer(self.sq, self.pq)
        self.spawer.start()
        #self.sender.moveToThread(self.thread)
        #self.sender.run_trigger.emit()
        
        #self.count
        #self.text.setPlaceholderText("   write here   ")
        
        self.Button.clicked.connect(self.addText)


    def main_part(self, key, num, msg):
        if key:
            self.gl_seq += msg + "\n"
            self.globalLabel.setText(self.gl_seq)
        else:
            self.strObj1One[num] += msg + "\n"
            self.str_now = num
            self.localLabel.setText(self.strObj1One[self.str_now])

    def addText(self):
        if not self.text.text() == "": 
            self.strObj1One[self.str_now] = self.strObj1One[self.str_now] + self.text.text() + "\n"
            self.text.setText("")
            self.localLabel.setText(self.strObj1One[self.str_now])
        else:
            if self.str_now == 3:
                self.str_now = 0
            else:
                self.str_now += 1
            self.localLabel.setText(self.strObj1One[self.str_now])
        
    def put_start_img(self):
        img = QtGui.QPixmap("img.jpg")
        self.imgLabel.setPixmap(img)

    def keyPressEvent(self, e):
        if e.key()   ==  Qt.Key_Escape:
            self.close()
        elif e.key() ==  Qt.Key_Return:
            self.addText()
        elif e.key() ==  Qt.Key_Enter:
            self.addText()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.postHandler.stop_trigger.emit()
            self.spawer.stop_trigger.emit()
            self.sysHandler.sysStop_trigger.emit()
            self.sender.sysStop_trigger.emit()
            time.sleep(10)
            QApplication.instance().quit()
            
                
                

def main():
    app = QtWidgets.QApplication(sys.argv)
    imp = Implement()
    imp.show()
    app.exec_()

if __name__ == '__main__':
    main()
