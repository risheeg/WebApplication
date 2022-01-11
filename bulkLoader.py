# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 20:39:49 2022

@author: rishe
"""
import sqlite3 as lite
conn = lite.connect('database.db')
print ("Opened database successfully")
'''
If you are rerunning this Python file, you can uncomment the Drop table 
and refresh the table by creating it again.
'''
#conn.execute('DROP TABLE items')
conn.execute('CREATE TABLE items (id TEXT, title TEXT, location TEXT, artist TEXT, price REAL)')
print ("Table created successfully")
conn.close()

from collections import defaultdict
            
class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.file_handle = None

    def __enter__(self):
        self.file_handle = open(self.filename)
        return self.file_handle

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file_handle:
            self.file_handle.close()
            

class CRUD:     
    def __init__(self, dbname):
        self.conn = lite.connect(dbname)
        self.cur = self.conn.cursor()
        
    def _create(self,store, k, v ):
        try:
            self.cur.execute("INSERT INTO items(id,title,location,artist,price) VALUES (?,?,?,?,?)",
                (k,v[0],v[1],v[2],v[3]) )
            
            self.conn.commit()
            print("Record successfully added")
        except:
            self.conn.rollback()
            print("error in insert operation")
            self.conn.close()
            
    def _read(self,store):
        self.conn.row_factory = lite.Row
        stmt = "select * from " + store
        self.cur.execute(stmt)
        rows = self.cur.fetchall()
        print(rows)
        self.conn.close()
        
        
def addrecs(dbname,tblname, datafile, bulk_id):
    D = defaultdict(list)    
    with FileReader(datafile) as file_handle:
        for i,s in enumerate(file_handle.read().splitlines()):
            key = bulk_id+str(i)
            for data in s.split(sep=','):
                D[key].append(data) 
            D[key].append(0)
    S = CRUD(dbname)
    for k,v in D.items(): S._create(tblname,k,v)
    S.conn.close()
    
def dbread(dbname,tblname):
    S = CRUD(dbname)
    S._read(tblname)
    
    
                  
db = "database.db"
tbl ="items"
path = "./BulkLoader/data/locations.csv"
bulk_id = "famous"

'''
Note that addrecs need to be run only once since we do not have any checks to put duplicate
data in the db.  You can always drop the table and recreate the store with sample data if you are not satisfied 
with the loaded data.
'''
addrecs(db,tbl,path, bulk_id)
dbread(db,tbl)
