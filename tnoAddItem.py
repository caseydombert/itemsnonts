import psycopg2

password = 'password'
host = '172.17.0.6'

item = input('type the item or blank to exit/n')

conn = psycopg2.connect("dbname=itemsnonts user=postgres password=" + password + " host=" + host + " port=5432")
cur = conn.cursor()
cur.execute("INSERT INTO items (item) VALUES (%s);", [item])
conn.commit()
cur.close()
conn.close()