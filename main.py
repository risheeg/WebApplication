import sqlite3
conn = sqlite3.connect('database.db')
print ("Opened database successfully")
#conn.execute('DROP TABLE items')
#conn.execute('DROP TABLE archiveditems')
#conn.execute('CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT,location TEXT, artist TEXT, price REAL, img TEXT, narrative TEXT)')
#conn.execute('CREATE TABLE archiveditems (id INTEGER PRIMARY KEY, archivecmt TEXT, title TEXT, location TEXT, artist TEXT, price REAL, img TEXT, narrative TEXT)')
print ("Table created successfully")
conn.close()

from flask import Flask, render_template, request
app = Flask(__name__)

def xtract(title,artist):
  a = ''.join(wrd[0] for wrd in artist.split())
  t = (''.join(wrd[0] for wrd in title.split()) )
  return a+t

@app.route('/')
def my_inventory():
   return render_template('index.html')

@app.route('/enternew')
def new_item():
   return render_template('item.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      msg = "initialized"
      try:
         nm = request.form['nm']
         loc = request.form['loc']
         artist = request.form['artist']
         price = request.form['amt']
         key = "webEntry"+xtract(nm,artist)
         
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO items(title,location,artist,price,img) VALUES (?,?,?,?,?)",(nm,loc,artist,price,key) )
            con.commit()
            print("Record successfully added")
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        report = request.form
        return render_template("report.html",report = report, msg = msg)
        con.close()

@app.route('/archiverec',methods = ['POST', 'GET'])
def archiverec():
   if request.method == 'POST':
      msg = "initialized"
      try:
         cmt = request.form['cmt']
         nm = request.form['nm']
         loc = request.form['loc']
         artist = request.form['artist']
         price = request.form['amt']
         key = request.form['img']
         add = request.form['add']
         
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO archiveditems(archivecmt,title,location,artist,price,img,narrative) VALUES (?,?,?,?,?,?,?)",(cmt,nm,loc,artist,price,key,add) )
            con.commit()
            print("Record successfully archived")
            msg = "Record successfully archived"
      except:
         con.rollback()
         msg = "error in archive operation"
      finally:
        con.close();
        report = request.form
        return render_template("report.html",report = report,msg = msg)

@app.route('/list')
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from items")
   
   rows = cur.fetchall(); 
   con.close();
   return render_template("list.html",rows = rows)

@app.route('/showarchive')
def showarchive():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from archiveditems")
   
   rows = cur.fetchall(); 
   con.close();
   return render_template("archive.html",rows = rows)


@app.route('/locate',methods = ['POST', 'GET'])
def locate():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   print("Locate",request.form["Id"])
   key = request.form["Id"]
   cur.execute("select * from items where id = " + str(key) )
   rows = cur.fetchall()
   con.close()
   return render_template("locate.html",rows = rows)

@app.route('/removerec',methods = ['POST', 'GET'])
def removerec():
   if request.method == 'POST':
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      key = request.form["Id"]
      cur.execute("select * from items where id = " + str(key) )
      rows = cur.fetchall()
      try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("delete from items where id = " + str(key) )
            con.commit()
            print("Deleted",key)
            msg = "Removed one record from inventory"
      except:
         print("error in delete operation")
         msg = "error in delete operation"
      finally:
        report = request.form
        con.close()
        return render_template("undelete.html", report = report, rows = rows, msg = msg)
    

@app.route('/editrec',methods = ['POST', 'GET'])
def editrec():
   if request.method == 'POST':
      key = request.form["Id"]
      col,val = "price","0.0"
      for k in request.form:
          print(k)
          if k == "add": col,val = "narrative",request.form["add"]
          elif k == "amt": col,val = "price", request.form["amt"]
          elif k == "loc":col,val = "location", request.form["loc"]
      print(key,col,val)
      try:
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("update items set " +
            col + " = \'" + val + "\'"
            " where id = " + str(key) )
            
            con.commit()
            msg = "Updated " + col + " of item id:" + str(key)
      except:
         con.rollback()
         print("error in update operation")
         msg = "error in update operation"
      
      finally:
        report = request.form
        return render_template("report.html",report = report, msg = msg)
        con.close()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
