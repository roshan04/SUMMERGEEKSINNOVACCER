from flask import Flask, render_template, request, redirect,url_for
from flask_mail import Mail, Message
import sqlite3 as sql
import time
app = Flask(__name__)
mail=Mail(app)
mail1=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'                
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nikamdeveloper@gmail.com'                     #host address
app.config['MAIL_PASSWORD'] = 'roshandev1234'                                #host password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

host='ROSHAN KISHOR NIKAM'  
hostaddress= 'roshannikam04n@gmail.com'                   #host name

mail = Mail(app)
mail1=Mail(app)

@app.route('/')
def home():
   return render_template('home.html')                               

@app.route('/start',methods = ['POST', 'GET'])
def start():
   if request.method == 'POST':
      task=request.form['task']
      if task == '1':
         return redirect( url_for('list'))
      elif task == '2':
         return render_template('person.html')

@app.route("/dekho")
def index():
   msg = Message('Hello', sender = host, recipients = ['roshannikam04@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

@app.route('/newinfo')
def new_student():
   return render_template('person.html')

@app.route('/record',methods = ['POST', 'GET'])
def record():
   if request.method == 'POST':
      try:
         nm    = request.form['nm']
         email = request.form['email']
         phone = request.form['phone']
         md    = request.form['md']
         address=request.form['address']
         if md == "entry":
            now = time.ctime(int(time.time()))
            with sql.connect("database.db") as con:
               cur = con.cursor()
               
               cur.execute("INSERT INTO students (name,email,phone,intime,outtime,address) VALUES (?,?,?,?,?,?)",(nm,email,phone,now,"NULL",address))
               
               con.commit()
               cur.close()
               msg = "Record successfully added"
         elif md == "exit":
            nower = time.ctime(int(time.time()))



            with sql.connect("database.db") as con:

               cur=con.cursor()
               cur.execute("select * from students where name=(?) and phone=(?)",(nm,phone))
               t=cur.fetchall();
               #print(len(t))
               intime = (t[0][3])

               cur.close()
   
               cur=con.cursor()
               cur.execute('''UPDATE students set outtime = (?) where name = (?) and phone=(?)''',(nower,nm,phone))
               con.commit()
               print("out time updated succesfully")
               cur.close()

               mailMsg = Message(nm+" info recieved", sender = hostaddress , recipients = [email])
               mailMsg.body = "Name : "+nm+"\nEmail : "+email+"\n Phone No. : "+phone+"\nIn-time : "+intime+"\nOut-time : "+nower+"Address visited : "+address+"\nname of host : "+host
               mail.send(mailMsg)

               mailMsg = Message(nm+" info recieved", sender = email , recipients = [hostaddress])
               mailMsg.body = "Name : "+nm+"\nEmail : "+email+"\n Phone No. : "+phone+"\nIn-time : "+intime+"\nOut-time : "+nower+"Address visited : "+address
               mail1.send(mailMsg)

               msg="exited successfully"
      except:
         con.rollback()
         msg = "error in the operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()

   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True, port = 4998)