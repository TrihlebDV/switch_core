#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
import threading

import com_dict

import socket

class Synapse(QObject):
    def __init__(self, HOST = 'localhost', PORT = 8686,
                 sys_worker = None, post_handler = None):
        super(Synapse, self).__init__()
        self.deamon = True
        self._stopped = threading.Event()
        
        self.SERVER_ADDRESS = (HOST, PORT)
        self.server = None
        self.max_listen = 1
        self.connected = []
        self.buff = 4096
        
        self.sys_worker = sys_worker
        self.post_handler = post_handler

    def serv_up(self):
        try:
             self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             self.server.bind(SERVER_ADDRESS)
             self.server.listen(self.max_listen)
            except OSError as e:
                self.server.close()
                err_dict = com_dict.send_err
                err_dict.update({2:e, 3:self})
                print(err_dict)
                #self.sys_worker.put(err_dict)

    def run(self):
        while not self._stopped.is_set():
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
                            self.send_info()
                        except OSError as e:
                            sock.close()
                            err_dict = com_dict.send_err
                            err_dict.update({2:e, 3:self})
                
