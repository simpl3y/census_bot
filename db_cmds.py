import os
import sqlite3

from const import *


# creates a table
def create_db_table(name,entries):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS %s (%s)''' % (name,entries))
    except:
        conn.close()
        return 1

    conn.close()
    return 0


def list_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    tables = []
    entries = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for entry in entries:
        tables.append(entry[0])
    conn.close()
    return tables


def fetch_table(name,entries,id):
    conn = sqlite3.connect(DB_NAME)
    try:
        results = conn.execute("SELECT %s FROM %s" % (entries,name))
    except:
        conn.close()
        return None
    
    for row in results:
        if((int(row[0]) == int(id))):
            print(row[1])
            conn.close()
            return str(row[1]) 
            
    conn.close()
    return None

def fetch_table_response(name,entries,response):
    conn = sqlite3.connect(DB_NAME)
    try:
        results = conn.execute("SELECT %s FROM %s" % (entries,name))
    except:
        conn.close()
        return None
    entries = []
    for row in results:
        if(str(row[1]).find(response) == 0):
            entries.append(row[0])
    
    conn.close()
    return entries




def scan_table(name,entries,keyword):
    conn = sqlite3.connect(DB_NAME)
    entries = []
    try:
        results = conn.execute("Select %s FROM %s" % (entries,name))
    except:
        conn.close()
        return entries
    for row in results:
        if(str(keyword) == str(row[1])):
            entries.append(int(row[0]))
    return entries




def addto_table(name,entries,values):
    conn = sqlite3.connect(DB_NAME)
    try:
        # print("SELECT %s FROM %s" % (entries,name))
        results = conn.execute("SELECT %s FROM %s" % (entries,name))
    except:
        print("failed to check table")
        conn.close()
        return 1
    
    for row in results:
        if(values.find(str(row[0])) >= 0):
            # removefrom_table(name,int(row[0]))
            conn.execute("DELETE FROM %s WHERE ID = %d" % (name, row[0]))
            break

    try:
        print("INSERT INTO %s (%s) VALUES(%s)" %(name,entries,values))
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
        print("DELETE FROM %s WHERE ID = %d" % (name, id))
        conn.execute("DELETE FROM %s WHERE ID = %d" % (name, id))
        conn.commit()
    except:
        print("failed to remove")
        conn.close()
        return 1
    
    conn.close()
    return 0


