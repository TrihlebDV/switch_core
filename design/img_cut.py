#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2

img = cv2.imread("do_not_change.png")
print(img.shape[:2])
cv2.imshow("olol", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cut = img[84:684, 400:1000]
cv2.imshow("olol1", cut)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("img.jpg", cut)
