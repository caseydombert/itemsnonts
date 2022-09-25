import psycopg2

password = 'password'
host = '172.17.0.6'

conn = psycopg2.connect("dbname=itemsnonts user=postgres password=" + password + " host=" + host + " port=5432")
cur = conn.cursor()
cur.execute("""CREATE TABLE items (
	id serial PRIMARY KEY NOT NULL,
	item text NOT NULL,
    time time NOT NULL DEFAULT statement_timestamp(), --ADD SQL TO AUTOMATICALLY TIMESTAMP AT INSERT IF NONE PRESENT; #tnotime: first class time
    filepath text
);

CREATE TABLE onts (
    id serial PRIMARY KEY NOT NULL,
    ont text NOT NULL
);

CREATE TABLE items_onts (
	item_id int NOT NULL REFERENCES items (id),
	ont_id int NOT NULL REFERENCES onts (id),
	PRIMARY KEY (item_id, ont_id)
);

CREATE TABLE combs (
	id serial PRIMARY KEY NOT NULL,
	comb text,
	query text NOT NULL
);

CREATE TABLE items_combs (
	item_id int NOT NULL REFERENCES items (id),
	comb_id int NOT NULL REFERENCES combs (id),
	PRIMARY KEY (item_id, comb_id),
    complete bool
);""")
conn.commit()
cur.close()
conn.close()