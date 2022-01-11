import sqlite3
conn = sqlite3.connect('database.db')
print ("Opened database successfully")
#conn.execute('DROP TABLE items')
#conn.execute('CREATE TABLE items (id TEXT, title TEXT, narrative TEXT, artist TEXT, price REAL, tags TEXT)')
print ("Table created successfully")
conn.close()

from flask import Flask, render_template, url_for, request
app = Flask(__name__)

def xtract(title):
  x = title.split(' ')
  return ''.join(wrd[0] for wrd in x)

@app.route('/')
def my_inventory():
   return render_template('index.html')

@app.route('/enternew')
def new_item():
   return render_template('item.html')

@app.route('/report',methods = ['POST', 'GET'])
def report():
   if request.method == 'POST':
      report = request.form
      return render_template("report.html",report = report)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         add = request.form['add']
         artist = request.form['artist']
         price = request.form['amt']
         
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            key = "webEntry"+xtract(nm)
            cur.execute("INSERT INTO items(id,title,narrative,artist,price) VALUES (?,?,?,?,?)",(key,nm,add,artist,price) )
            
            con.commit()
            print("Record successfully added")
      except:
         con.rollback()
         print("error in insert operation")
      
      finally:
        report = request.form
        return render_template("report.html",report = report)
        con.close()
    
@app.route('/list')
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from items")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
