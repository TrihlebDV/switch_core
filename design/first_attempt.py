#!/usr/bin/python3
# -*- coding: utf-8 -*-

#GUI libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

#necessary libraries
import sys

#lib for drawing
import numpy as np
import cv2

#GUI form
import first_des

class Implement(QtWidgets.QWidget, first_des.Ui_FORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.strObj1One = ""
        self.globalLabel.setText("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.put_start_img()
        #self.text.setPlaceholderText("   write here   ")
        
        self.Button.clicked.connect(self.addText)

    def addText(self):
        if not self.text.text() == "": 
            self.strObj1One = self.strObj1One + self.text.text() + "\n"
            self.text.setText("")
            self.localLabel.setText(self.strObj1One)
        
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
                
                

def main():
    app = QtWidgets.QApplication(sys.argv)
    imp = Implement()
    imp.show()
    app.exec_()

if __name__ == '__main__':
    main()
