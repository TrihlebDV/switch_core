#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
import threading

import com_dict

import socket
import select

class Synapse(QObject):
    def __init__(self, HOST = 'localhost', PORT = 8686,
                 sys_worker = None, post_handler = None):
        super(Synapse, self).__init__()
        self.deamon = True
        self._stopped = False
        self.SERVER_ADDRESS = (HOST, PORT)
        self.server = None
        self.max_listen = 1
        self.connected = []
        self.buff = 4096
        
        self.sys_worker = sys_worker
        self.post_handler = post_handler

        self.stop_trigger.connect(self.stop)

        self.select_template = None
        temp = com_dict.get_command("select")
        self.create_selecting_template(temp)
        self.ans = None

    stop_trigger = pyqtSignal()
    #@pyqtSlot()
    def close(self):
        self._stopped = True
        

    def serv_up(self):
        try:
             self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             self.server.bind(SERVER_ADDRESS)
             self.server.listen(self.max_listen)
        except OSError as e:
            self.server.close()
            err_dict = com_dict.serv_up_err
            err_dict.update({2:e, 3:self})
            print(err_dict)
            #self.sys_worker.put(err_dict)

    def create_selecting_template(self, temp):#dictionart
        pass
        

    def run(self):
        while not self._stopped:
            read_sockets, write_sockets, error_sockets = select.select(self.server , [], [])
                for sock in read_sockets:
                    if sock == self.server:
                        sockfd, addr = server_socket.accept()
                        self.connected.append(sockfd)
                        print("Client (%s, %s) connected" % addr)
                        sock.send(bytes("Connected sucsessfuly\n", encoding='UTF-8'))
                    else:
                        try:
                            data = sock.recv(self.buff)
                            self.push_update(data)
                            if self.ans not is None:
                                sock.send(bytes(self.ans, encoding = 'UTF-8'))
                                self.ans = None
                            self.get_data()
                        except OSError as e:
                            sock.close()
                            err_dict = com_dict.send_err
                            err_dict.update({2:e, 3:self})

    def command_build(self, tempalte, data):
        pass

    def push_update(self, data):
        tempalte = com_dict.get_command("insert")
        command = self.command_build(tempalte, data)
        ins_req = {"obj"     : self,
                   "command" : command}
        self.post_handler.put(ins_req)

    def get_data(self):
        if self.ans is None:
            self.post_handler.put(self.select_template)

    def stop(self):
        self._stopped.set()
                
