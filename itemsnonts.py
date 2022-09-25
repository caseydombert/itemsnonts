import psycopg2
import keyring
import re
import pprint
pp = pprint.PrettyPrinter()

password = "password"
host = "172.17.0.6"

def newConCur():
    global conn
    conn = psycopg2.connect("dbname=itemsnonts user=postgres password=" + password + " host=" + host + " port=5432")
    global cur
    cur = conn.cursor()
def closeCS():  # close, save
    conn.commit()
    cur.close()
    conn.close()
def closeCNS():  # close, no save
    cur.close()
    conn.close()


def query():
    pass


def initComb(queryString, combName):
    newConCur()
    cur.execute("INSERT INTO combs (comb, query) VALUES (%s, %s);", (combName, queryString))
    cur.execute("SELECT id FROM combs WHERE comb='{}';".format(combName))
    combId = cur.fetchall()[0][0]
    print(combId)
    cur.execute(queryString)
    ids = [record [0] for record in cur.fetchall()]
    for id in ids:
        cur.execute("INSERT INTO items_combs VALUES (%s ,{}, False);".format(combId), [id])
    closeCS()
def displayCombs(): #displays existing combs 
    newConCur()
    cur.execute("SELECT * FROM combs;")
    a = cur.fetchall()
    pp.pprint(a)
    closeCNS()


def displayOnts():
    newConCur()
    cur.execute("SELECT * FROM onts;")
    a = cur.fetchall()
    print('')
    print("available onts (id, name):")
    pp.pprint(a)
    closeCNS()
def newOnt(ont):
    newConCur()
    cur.execute("INSERT INTO onts (ont) VALUES (%s);", [ont])
    closeCS()
def getNextItem(comb):
    newConCur()
    cur.execute("SELECT item_id FROM items_combs WHERE comb_id={} AND complete= (false) LIMIT 1;".format(comb))
    tnoId = cur.fetchall()
    tnoId = tnoId[0][0]
    closeCNS()
    return tnoId
def displayItem(id):
    newConCur()
    cur.execute("Select * FROM items LIMIT 0")
    cols = tuple([desc[0] for desc in cur.description])
    cur.execute("SELECT * FROM items WHERE id={};".format(id))
    data = cur.fetchall()[0]
    display = dict(zip(cols, data))
    print('-------------------')
    print("active item: " + str(display))
    closeCNS()


def applyOnt(ontId, value):
    newConCur()
    cur.execute("INSERT INTO items_onts VALUES (%s, %s);", (ontId, value))
    closeCS()
def completeItem(tnoId, comb):
    newConCur()
    cur.execute("UPDATE items_combs SET complete = (true) WHERE item_id=(%s) AND comb_id=(%s);", (tnoId, comb))
    closeCS()


def unOntItem(id, ont):
    pass
def deleteOnt():
    pass

def start(comb):
    tnoId = getNextItem(comb)
    displayItem(tnoId)
    displayOnts()
    idSelect = re.compile('^[0-9]+$')
    print()
    print('for new ont: input new ont name (text)')
    print('assign an existing ont to current item: input ont id')
    print("advance to next item in comb: input 'j'")
    stringIn = input()
    if stringIn == '':
        exit()
    elif stringIn == 'j':
        completeItem(tnoId, comb)
        start(comb)
    elif idSelect.match(stringIn): #if its an int
        applyOnt(tnoId, stringIn)
        start(comb)
    else:
        newOnt(stringIn)
        start(comb)

displayCombs()
comb = input('"comb" to create new comb, else select a comb_id (index 0 of above tuples): ')
if comb == 'comb':
    queryString = input('queryString: ')
    combName = input('combName: ')
    if combName == '':
        combName == none
    initComb(queryString, combName)
else:
    start(comb)
