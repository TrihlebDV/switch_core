#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

import sys, os

import time

import select
import socket

import psycopg2
import com_dict
from com_dict import get_command


class PostHandler(QtCore.QThread):
    def __init__(self, pq, sq, instr, quantity=1, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.queue = pq
        self.syshand = sq
        self._stopped = False
        self.stop_trigger.connect(self.stop)
        self.run_trigger.connect(self.run)
        self._quantity = quantity
        self._instr = instr

    stop_trigger = pyqtSignal()
    run_trigger  = pyqtSignal()
        

    def get_answr(self, req, cur):
        #get object wich done reqwest -> if there is no object "return 0"
        try:
            obj = req["obj"]
        except:
            return None

        #get reqwest -> if there is no reqwest "return 0"
        try:
            rq = req["req"] #type dict:{ int i : str "command"} i = 1, 2, 3...
        except:
            return None

        ins = rq["insert"]
        if not ins == "":
            for key in ins:
                cur.execute(ins[key])

        exe = rq["exe"]
        if not exe == "":
            ans = {} #create empty template of answer
            #fetching information from the table
            for key in exe:
                try:
                    cur.execute(exe[key])
                    ans.update({key : cur.fetchall()})
                except Exception as e:
                    ans.clear()           #make ans empty
                    ans.update({"err", e})#put error to ans
                    #send exception to sys_handler
                    return None
            return ans
        

    def req_hendler(self, req, cur):
        ans = self.get_answr(req, cur)
        f_ans = ""
        if not ans is None:
            for key in ans:
                f_ans += str(ans[key])
            return f_ans
        else:
            return None
                
    @pyqtSlot()
    def run(self):
        print("postHandler started!")
        try:
            conn = psycopg2.connect(get_command("connection").format('switch_core', 'local', 'localhost', '123'))
            conn.autocommit = True
            cur = conn.cursor()
            for i in range(self._quantity):
                cur.execute("DROP TABLE table{}".format(i))
                cur.execute("CREATE TABLE table{}({})".format(i, self._instr[i])) 
            print("Tables Created!") 
            while not self._stopped:
                if not self.queue.empty():
                    req = self.queue.get()
                    ans = self.req_hendler(req, cur)
                    if not ans is None:
                        obj = req["obj"]
                        obj.ans = ans
            for i in range(self._quantity):
                cur.execute("DROP TABLE table{}".format(i))
            print("Tables deleted")
                
        except Exception as e:
            print(e)
            #send exception to sys_handler
        finally:
            cur.close()
            conn.close()
            print("postHandler stoped")
            #send emit of ending posthandler worker to sys_handler

    def command_handler(self, com):
        obj = com['obj']
        if com['type'] == 'err':
            pass

    def stop(self):
        self._stopped = True

class Spawer(QtCore.QThread):
    mutex = QtCore.QMutex()
    def __init__(self, sq, pq, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.sq = sq
        self.pq = pq
        self._stopped = False
        self.i = "INSERT INTO {}({}) VALUES ({})"
        self.s = "SELECT {} FROM {} {}"
        self.stop_trigger.connect(self.stop)
        self.ans = None
        
    stop_trigger = pyqtSignal()
                            
    def run(self):
        print("spqwer stared!")
        count = 0
        time.sleep(10)
        while not self._stopped:
            req = {"obj" : self,
                   "req" : {"insert" : {1 : self.i.format("table0", "data, real", "'ololol', {}".format(count)),
                                        2 : self.i.format("table1", "data, real", "'alalaa', {}".format(count)),
                                        3 : self.i.format("table2", "data, real", "'xdgxdr', {}".format(count)),
                                        4 : self.i.format("table3", "data, real", "'estrta', {}".format(count))},
                            "exe"    : {1 : self.s.format("*", "table0", ""),
                                        2 : self.s.format("*", "table1", ""),
                                        3 : self.s.format("*", "table2", ""),
                                        4 : self.s.format("*", "table3", "")}}}
            self.pq.put(req)
            count += 1
            if count == 10: count = 0
            time.sleep(10)
            if not self.ans is None:
                Spawer.mutex.lock()
                r = {count % 4 : {"msg" : self.ans}}
                self.sq.put(r)
                self.ans = None
                Spawer.mutex.unlock()
        print("spawer stoped")
            
    def stop(self):
        self._stopped = True


    
