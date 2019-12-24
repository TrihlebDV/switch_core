#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject

import com_dict

import socket

class TCPClient(QObject):
    def __init__(self, HOST = 'localhost', PORT = 8686, sys_worker = None):
        super(TCPClient, self).__init__()
        self.SERVER_ADDRESS = (HOST, PORT)
        self.client = None
        self.sys_worker = sys_worker

    def serv_connect(self, status):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(self.SERVER_ADDRESS)
        except ConnectionError as e:
            self.client.close()
            err_dict = com_dict.conn_err
            err_dict.update({2:status, 3:e, 4:self})
            #self.sys_worker.put(err_dict)
            print(err_dict)

    def send_msg(self, income_dict):
        if self.client.fileno() > 0:
            #some how retranslete to str
            msg = "ololollol"
            try:
                print("Yha-ha")
                self.client.send(bytes(msg, encoding = 'UTF-8'))
            except OSError as e:
                err_dict = com_dict.send_err
                err_dict.update({2:e, 3:self})
                print(err_dict)
                #self.sys_worker.put(err_dict)
        
            
def main():
    client = TCPClient()
    client.serv_connect("conn")
    client.send_msg("O:A:A")

if __name__ == '__main__':
    main()
    
