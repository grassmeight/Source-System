from flask import Flask, redirect, url_for, render_template, request, session
from data_watchdog import *
from data_analyst import *
from multiprocessing import Process, freeze_support
from threading import Thread
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

def updateData():
    watchdog = DataWatchdog()
    analyst = DataAnalyst(watchdog.getData()[0],watchdog.getData()[1],watchdog.getData()[2],watchdog.getCodex()[0],watchdog.getCodex()[1])
    queue = Queue()
    watch_thread = Thread(target = watchdog.processUpdate, daemon = True, args = [queue, ])
    watch_thread.start()
    counter = 0
    while True:
        if not queue.empty():
            data = queue.get()
            analyst.runAnalysis(data[0], data[1], data[2], data[3], data[4])
            counter += 1
            print(counter)
    

if __name__ == "__main__":
    freeze_support()
    p = Process(target = updateData, daemon = True)
    p.start()
    while True:
        sleep(1)
    #app.run(debug = True)