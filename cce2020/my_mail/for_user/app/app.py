# -*- coding: utf-8 -*-
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
import os
import smtplib
import re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = '/var/www/html/flask-server/upload'
email_regex = '^[0-9a-zA-Z]([-_.+]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$'



db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    def __init__(self,username,password):
        self.password = password
        self.username = username


db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def sendMail(to, fro, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['MAIL FROM'] = fro
    msg['RCPT TO'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
 
    msg.attach( MIMEText(text) )
 
    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)
 
    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

@app.route("/",methods=["GET","POST"])
def index():
    if session and session['logged_in']==True:
        if request.method=="POST":
            title= request.form["title"]
            email= request.form["email"]
            content= request.form["content"]

            if(re.search(email_regex,email)==None):
                flash('invalid email')
                return render_template("index.html")
            file=request.files["attachment"]
            if not file:
                try:
                    sendMail([email],'{name} <{name}@cce.kr>'.format(name=session['username']),title,content,[])
                except:
                    flash('fail')
                    return render_template("index.html")
            else:
                if allowed_file(file.filename):
                    path=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(path)
                    os.chmod(path,0o644)
                    try:
                        sendMail([email],'{name} <{name}@cce.kr>'.format(name=session['username']),title,content,[path])
                        time.sleep(1)
                        os.remove(path)
                    except:
                        flash('fail')
                        return render_template("index.html")   
                else:
                    flash('invalid file')
                    return render_template("index.html")
            flash('succeeded in sending the mail.')
            return render_template("index.html")
        else:
            return render_template("index.html")
    else:
        return redirect(url_for("login"))



@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        login = user.query.filter_by(username=username, password=password).first()
        if login is not None:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for("index"))
        else:
            flash('login failed')
            return render_template("login.html")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        register = user(username = username, password = password)
        exist= user.query.filter_by(username=username).first()
        if exist is not None:
            flash('This username exists.')
            return render_template("register.html")        
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0')


