from flask import Flask, redirect, url_for, render_template, request, session
from data_watchdog import *
from data_analyst import *
from multiprocessing import Process, freeze_support
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "nibba"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# db = SQLAlchemy(app)
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jobs")
def jobs():
    return render_template("jobs.html", headers = data[0].columns, values = data[0].values)

@app.route("/branches")
def branches():
    return render_template("branches.html", headers = data[1].columns, values = data[1].values)
    
if __name__ == "__main__":
    freeze_support()
    watchdog = DataWatchdog()
    data = watchdog.getData() + watchdog.getCodex()
    p = Process(target = watchdog.processUpdate, daemon = True)
    p.start()
    analyst = DataAnalyst(data[0], data[1], data[2], data[3], data[4])
    data = analyst.getData() + analyst.getDataLong()
    app.run(debug = True)