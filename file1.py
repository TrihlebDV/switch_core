


import psycopg2
import threading
import time

commands = {"connection" : "dbname={} user={} host={} password={}",
            "create"     : "CREATE TABLE {}(key SERIAL PRIMARY KEY, {})",
            "insert"     : "INSERT INTO {}({}) VALUES ({})",
            "drop"       : "DROP TABLE {}",
            "select"     : "SELECT {} FROM {} {}"}


def get_command(name):
    try:
        return commands[name]
    except:
        return None

class ExClass(object):
    def __init__(self, queue = None, event = None):
        self.queue = queue
        #self.queue.put("AA")
        self.event = event
        self.CFTables()
        
    def CFTables(self):
        import psycopg2
        try:
            conn = psycopg2.connect(get_command("connection").format('switch_core', 'local', 'localhost', '123'))
            conn.autocommit = True
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()
        try:
            cur.execute(get_command("drop").format("first "))
        except:
            print("there's no TABLE first")
        try:
            cur.execute(get_command("drop").format("second "))
        except:
            print("there's no TABLE second")
        cur.execute(get_command("create").format("first", "data int"))  
        cur.execute(get_command("create").format("second", "data int"))
        
        for i in range(10):
            cur.execute(get_command("insert").format("first", "data", i))
            cur.execute(get_command("insert").format("second", "data", 10 - i))
        print("created and filled TABLES")
        cur.close()
        conn.close()
        

    def get_me(self):
        return self

    def put(self, count):
        self.count = count

    def on_recive(self, recive):
        print(recive)

    def close(self):
        cur.execute(get_command("drop").format("first "))
        cur.execute(get_command("drop").format("second"))

    def wait_and_put(self):
        print(self.queue)
        print(self.event)
        time.sleep(5)
        #'switch_core', 'local', 'localhost', '123'
        a = {"obj" : self,
             "connection" : {1 : 'switch_core', 2 : 'local', 3 : 'localhost', 4 : '123'},
             "commands"   : {"select_f" : {1 : "data", 2 : "first", 3 : ""},
                             "select_d" : {1 : "data", 2 : "first", 3 : "WHERE data = 9"},
                             "select_s" : {1 : "*", 2 : "second", 3 : "WHERE data = 9"}}}
        #self.put = a
        self.queue.put(a)
        self.event.set()
        
        

    
def main():
    try:
        conn = psycopg2.connect(get_command("connection").format('switch_core', 'local', 'localhost', '123'))
    
    except:
        print("I am unable to connect to the database")

    cur = conn.cursor()
    cur.execute(get_command("create").format("first", "data int"))  
    #    "CREATE TABLE first(key SERIAL PRIMARY KEY, data int);")
    conn.commit() # <--- makes sure the change is shown in the database
    for i in range(10):
        cur.execute(get_command("insert").format("first", "data", i))
            #"INSERT INTO first(data) VALUES ({})".format(i))
    conn.commit()


    answer = input()
    cur.execute(get_command("drop").format("first"))
    #
    conn.commit() # <--- makes sure the change is shown in the database
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()

