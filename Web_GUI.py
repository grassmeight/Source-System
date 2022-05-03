from flask import Flask, redirect, url_for, render_template, request, session
from data_watchdog import *
from data_analyst import *
from multiprocessing import Process, freeze_support, Queue
from threading import Thread

#setting a Flask app and setting the secret key 9required for session managing)
app = Flask(__name__)
app.secret_key = "nibba"

#the method responsible for fetching the homepage
@app.route("/")
def home():
    return render_template("index.html")

#the method responsible for fetching the jobs dashboard
@app.route("/jobs")
def jobs():
    return render_template("jobs.html", headers = data[0].columns, values = data[0].values)

#the method responsible for fetching the branches dashboard
@app.route("/branches")
def branches():
    return render_template("branches.html", headers = data[1].columns, values = data[1].values)

#a method to control the data updating process
def updateData(queue_large):
    #initialzing the watchdog and analyst (the two classes responsible for the data)
    watchdog = DataWatchdog()
    analyst = DataAnalyst(watchdog.getData()[0],watchdog.getData()[1],watchdog.getData()[2],watchdog.getCodex()[0],watchdog.getCodex()[1])

    #getting a queue to synchronize the data between the two threads
    queue_small = Queue()

    #initializing the Thread responsible for watching for changes in the data.
    #the thread will run the processUpdate method of the DataWatchdog class.
    watch_thread = Thread(target = watchdog.processUpdate, daemon = True, args = [queue_small, ])
    watch_thread.start()

    counter = 0
    #creating an infinite loop. The loop will only stop when the program stops (the process will be a daemon)
    while True:
        #checking if the queue is not empty (this means there is new data that needs handeling)
        if not queue_small.empty():
            #getting the data from the queue and using the runAnalysis function to analyze it
            data = queue_small.get()
            analyst.runAnalysis(data[0], data[1], data[2], data[3], data[4])
            
            #a simple check
            counter += 1
            print(counter)
    

if __name__ == "__main__":
    freeze_support()
    q = Queue()
    p = Process(target = updateData, daemon = True)
    p.start()
    counter = 0
    while True:
        if q
    #app.run(debug = True)