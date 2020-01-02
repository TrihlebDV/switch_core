#!/usr/bin/env python3
# -*- coding: utf-8
import time

i = 0

while True:
    i+=1
    if i%2 == 0:
        continue
    if i>15:
        break
    print(i)
    time.sleep(i/10)
    
