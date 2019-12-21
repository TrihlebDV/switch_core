#from multiprocessing  import Process
#import time
print("started")
from queue import Queue
import threading

import file1
from file1 import get_command
import psycopg2


#def count(key):
##    now = time.time()
#    for i in range(5):
#        time.sleep(1)
#    print("Process:{} started at:{} finished at:{}\n\
#           -----worked duiring:{}".format(key, now, time.time(), time.time()-now))
def main():
    q = Queue()
    ev = threading.Event()
    ex = file1.ExClass(queue = q, event = ev)
    #ex = file1.ExClass(event = ev)
    th = threading.Thread(target=ex.wait_and_put)
    th.start()
    ev.wait()
    #com = ex.put
    com = q.get()
    obj = com["obj"]
    print(get_command("connection").format(com["connection"][1],
                                           com["connection"][2],
                                           com["connection"][3],
                                           com["connection"][4]))
    try:
        #con = psycopg2.connect(get_command("connection").format(com["connection"][1],
        #                                                        com["connection"][2],
        #                                                        com["connection"][3],
        #                                                        com["connection"][4]))
        con = psycopg2.connect("dbname=switch_core user=local host=localhost password=123")
        con.autocommit = True
    except:
        print("I am unable to connect to the database")

    cur = con.cursor()
    ans = {}
    for key in com["commands"]:
        cur.execute(get_command("select").format(com["commands"][key][1],
                                                 com["commands"][key][2],
                                                 com["commands"][key][3]))
        ans.update({key : cur.fetchall()})
    obj.on_recive(ans)
    cur.execute(get_command("drop").format("first "))
    cur.execute(get_command("drop").format("second"))
    cur.close()
    con.close()
    
        


    
if __name__ == '__main__':
    main()
    #   for key in range(5):
  #      pr = Process(target = count, args=(1,))
   #    pr.start()
    #    pr.join()
