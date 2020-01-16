#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

import time


class SysHandler(QtCore.QThread):
    sysStop_trigger = pyqtSignal()
    run_trigger     = pyqtSignal()
    def __init__(self, sysQueue, infUpdate= None, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.queue = sysQueue
        self._stopped = False
        self._onUpdate = None
        if (not infUpdate is None) and callable(infUpdate):
            self._onUpdate = infUpdate #function from GUI for updating information in labels

        self.sysStop_trigger.connect(self.stop)
        self.run_trigger.connect(self.run)
    
    def req_handler(self,pr, req):
        for key in req:
            if key == "info":
                com = req[key]
                for key in com:
                    if key == "main":
                        self._onUpdate(True,  1,   com[key])
                    else:
                        self._onUpdate(False, key, com[key])
            elif key == "log":
                '''
                here will be block of logging with under key indexation
                something like:
                    open index_of_file with a:
                        close

                !!! and logFile size control like function!!!
                '''
                pass
            
                
    @pyqtSlot()
    def run(self):
        #self._onUpdate(True, 1, "SysHandler started!")
        #print("SysHandler started!")
        while not self._stopped:
            if not self.queue.empty():
                pr, req = self.queue.get()
                self.req_handler(pr, req)
                self.queue.task_done()
            #else:
            #    time.sleep(0.1)
        #print("SysHandler Stopped!")
        #self._onUpdate(True, 1, "SysHandler Stopped!")
        
 #   @pyqtSlot()
    def stop(self):
        self._stopped = True

'''
class Sender(QtCore.QThread):
    def __init__(self, q, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.queue = q
        self._stopped = False

        self.sysStop_trigger.connect(self.stop)
        self.run_trigger.connect(self.run)
        #print("AAA")

    sysStop_trigger = pyqtSignal()
    run_trigger     = pyqtSignal()
    
    @pyqtSlot()
    def run(self):
        count = 0
        print("Sender started")
        while not self._stopped:
            main  = "message for mainLabel:"  + str(count) + str(int(time.time()))
            local = "message for localLabel:" + str(count) + str(int(time.time()))
            dic1 = {"main" : {"msg" : main}}
            dic2 = {count : {"msg" : local}}
            self.queue.put(dic1)
            self.queue.put(dic2)
            count += 1
            if count == 4: count = 0
            time.sleep(10)
        print("Sender Stopped!")

    def stop(self):
        self._stopped = True

if __name__ == '__main__':
    import queue
    qu = queue.Queue()
    sysHandler = SysHandler(q=qu)
    sysHandler.run()
'''
