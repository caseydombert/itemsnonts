import psycopg2
import config

config = config.configDict
def newConCur():
    global conn
    conn = psycopg2.connect(dbname=config["dbname"],
                            user=config["user"],
                            password=config["password"],
                            host=config["host"],
                            port=config["port"])
    global cur
    cur = conn.cursor()

def closeCS():  # close, save
    conn.commit()
    cur.close()
    conn.close()

def closeCNS():  # close, no save
    cur.close()
    conn.close()

item = input('type the item or blank to exit/n')

conn = psycopg2.connect("dbname=itemsnonts user=postgres password=" + password + " host=" + host + " port=5432")
cur = conn.cursor()
cur.execute("INSERT INTO items (item) VALUES (%s);", [item])
closeCS()