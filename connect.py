import psycopg2
hostname = 'localhost'
database = 'Db'
username = 'postgres'
pwd = 'Aruba@123'
port_id = 5432
conn = None
curr = None
 
try: 
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user =username,
        password = pwd,
        port = port_id

    )

    curr = conn.cursor()

    testt = '''CREATE TABLE IF NOT EXISTS TEST(
        id int PRIMARY KEY
    )'''

    curr.execute(testt)
    conn.commit()
except Exception as error:
    print (error)
finally:
    if curr is not None:
        curr.close()
    if conn is not None:
         conn.close()


