#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import sys
#from PyQt5.QtWidgets import QApplication, QWidget
import cv2
import numpy as np
import math


def draw(c, r, p):
    points = np.array(r, np.int)
    cv2.polylines(img, np.int32([points]), isClosed=True, color=(255, 0, 255), thickness=2)
    
    #cv2.circle(img, c, 200, (0,0,255), 2)
    cv2.circle(img, p, 3, (255,0,0), -1)

def rotate(c, r, p, a):
    x0 = c[0]
    y0 = c[1]
    for i, point in enumerate(r):
        x = point[0]
        y = point[1]
        X = int(x0 + (x - x0) * math.cos(a) - (y - y0) * math.sin(a))
        Y = int(y0 + (y - y0) * math.cos(a) + (x - x0) * math.sin(a))
        r[i] = [X, Y]
    x = p[0]
    y = p[1]
    X = int(x0 + (x - x0) * math.cos(a) - (y - y0) * math.sin(a))
    Y = int(y0 + (y - y0) * math.cos(a) + (x - x0) * math.sin(a))
    p = [X, Y]
    
    return (r, p)
    

if __name__ == '__main__':
    img = np.ones((600, 600, 3), np.uint8)
    img *= 255
    r = [[270, 450], [330, 450], [330, 550], [270, 550]]
    p = [300, 500]
    c = (300, 300)
    #draw(c, r, (p[0], p[1]))
    r, p = rotate(c, r, p, math.radians(45))
    draw(c, r, (p[0], p[1]))

    for count in range(3):
        r, p = rotate(c, r, p, math.radians(90))
        draw(c, r, (p[0], p[1]))
    
    cv2.imshow("sdsdsd", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    #app = QApplication(sys.argv)

    #w = QWidget()
    #w.resize(600, 600)
    #w.move(300, 300)
    #w.setWindowTitle('Simple')
    #w.show()

    #sys.exit(app.exec_())
