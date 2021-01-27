import os
import sqlite3
import datetime

from const import *

def create_db_table(name,entries):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS %s (%s)''' % (name,entries))
    except:
        conn.close()
        return 1

    conn.close()
    return 0


def fetch_table(name,entries,id,scan=0,bday_list=[]):
    conn = sqlite3.connect(DB_NAME)
    try:
        results = conn.execute("SELECT %s FROM %s" % (entries,name))
    except:
        conn.close()
        return None
    
    entry = []
    if(not scan):
        for row in results:
            if((int(row[0]) == int(id))):
                if(name == 'birthdays'):
                    entry.append("%02d/%02d/%04d" % (row[2],row[3],row[1]))
                    break 
                else:
                    entry.append("%s" % row[1])
                    break
    else:
        dt = datetime.datetime.today()
        for row in results:
            if(int(row[2]) == dt.month and int(row[3]) == dt.day):
                entry.append(row[0])

    conn.close()
    return entry

def addto_table(name,entries,values):
    conn = sqlite3.connect(DB_NAME)
    try:
        results = conn.execute("SELECT %s FROM %s" % (entries,name))
    except:
        print("failed to check table")
        conn.close()
        return 1
    
    for row in results:
        if(values.find(str(row[0])) >= 0):
            removefrom_table(name,int(row[0]))
            break

    try:
        conn.execute("INSERT INTO %s (%s) VALUES(%s)" %(name,entries,values))
    except:
        print("failed to insert")
        conn.close()
        return 1

    conn.commit()
    conn.close()
    return 0

def removefrom_table(name,id):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("DELETE FROM %s WHERE ID = %d" % (name, id))
        conn.commit()
    except:
        print("failed to remove")
        conn.close()
        return 1
    
    conn.close()
    return 0


