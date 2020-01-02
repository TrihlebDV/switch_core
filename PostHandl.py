#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

import sys, os

import time

import select
import socket

import psycopg2
import com_dict
from com_dict import get_command

class PostHandler(QObject):
    def __init__(self, queue):
        super(PostHandler, self).__init__()
        self.queue = queue
        self._stopped = False

        self.stop_trigger.connect(self.stop)

    def get_answr(self, req):
        #get object wich done reqwest -> if there is no object "return 0"
        try:
            obj = req["obj"]
        except:
            return None

        #get reqwest -> if there is no reqwest "return 0"
        try:
            req = req["req"] #type dict:{ int i : str "command"} i = 1, 2, 3...
        except:
            return None

        ans = {} #create empty template of answer
        #fetching information from the table
        for key in req:
            try:
                cur.execute(req[key])
                ans.update({key : cur.fetchall()})
            except Exception as e:
                ans.clear()           #make ans empty
                ans.update({"err", e})#put error to ans
                #send exception to sys_handler
                return None
        return ans
        

    def req_henadler(self, req):
        ans = self.get_answr(req)
        f_ans = ""
        if not ans is None:
            for key in ans:
                f_ans += str(ans[key])
            return f_ans
        else:
            return None
                
    
    def run(self):
        try:
            conn = psycopg2.connect(get_command("connection").format('switch_core', 'local', 'localhost', '123'))
            conn.autocommit = True
            cur = conn.cursor()
            while not self._stopped:
                if not self.queue.empty():
                    req = self.queue.get()
                    ans = req_henadler(req)
                    if not ans is None:
                        obj = req["obj"]
                        obj.ans = ans
                        
        except Exception as e:
            #send exception to sys_handler
        finally:
            cur.close()
            conn.close()
            #send emit of ending posthandler worker to sys_handler

    def command_handler(self, com):
        obj = com['obj']
        if com['type'] == 'err':
            

    stop_trigger = pyqtSignal()
    def stop(self):
        self._stopped = True


    
