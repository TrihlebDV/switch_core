commands = {"connection" : "dbname={} user={} host={} password={}",
            "create"     : "CREATE TABLE {}(key SERIAL PRIMARY KEY, {})",
            "insert"     : "INSERT INTO {}({}) VALUES ({})",
            "drop"       : "DROP TABLE {}",
            "select"     : "SELECT {} FROM {} {}"}

conn_err    = { 1 : "conn_err",    2 : None, 3 : None, 4:None}
send_err    = { 1 : "send_err",    2 : None, 3 : None}
recv_err    = { 1 : "recv_err",    2 : None, 3 : None}
serv_up_err = { 1 : "serv_up_err", 2 : None, 3 : None}
