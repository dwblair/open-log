from flask import jsonify
from flask import request, send_from_directory, make_response, redirect, url_for, render_template
from flask import Flask, redirect, Request, g


import os
import json
import csv

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
#import numpy
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

import datetime


import StringIO
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.dates import DayLocator, MinuteLocator, HourLocator

from app import app


SECRETKEY='bananas'

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



    

@app.route('/senddata')
def data():
    feedID=request.args.get('feedID')
    secretKey=request.args.get('secretKey')
    field1=request.args.get('field1')
    val1=request.args.get('val1')

    if secretKey==SECRETKEY:
        #save to server
        #data=[{'feedID':feedID, 'field1':field1, 'val1':val1}]
        #jsonOut=json.dumps(data)
        #uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.json')
        #f=open(uploadFilePath,'a')
        #f.write(jsonOut)
        #f.close()

        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        
        uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.csv')
        if os.path.exists(uploadFilePath)==False:
            f=open(uploadFilePath,'a')
            f.write('date,field1,val1\n')
            f.close()
        f=open(uploadFilePath,'a')
        timeNow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # for this method, see: http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
        
        
        f.write(timeNow+","+field1+','+val1+'\n')
        f.close()
        #generate response
        jsonR = jsonify(timestamp=timeNow,feedID=feedID,field1=field1,val1=val1)
        return jsonR
        #return redirect(url_for('plot',feedID=feedID)) 
    else:
        return "You can't do that."

@app.route('/latest/<feedID>')
def showFeed(feedID):
    uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.csv')
    f=open(uploadFilePath,'a')
    return uploadFilePath

#uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],filename)

@app.route('/data/<feedID>/csv')
def send_csv_file(feedID):
    return send_from_directory(UPLOAD_FOLDER,feedID+'.csv')

@app.route('/data/<feedID>/latest/json')
def get_latest_data_from_file_json(feedID):
    uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.csv')
    #data=np.loadtxt(uploadFilePath)
    reader=csv.reader(open(uploadFilePath,"rb"),delimiter=',')
    x=list(reader)
    lastItem=x[len(x)-1]
    timeStamp=lastItem[0]
    lastField=lastItem[1]
    lastVal=lastItem[2]

    #dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    #timeOut=json.dumps(timeStamp, default=dthandler)
    
    return jsonify(timeStamp=json.dumps(timeStamp),feedId=feedID,field1=json.dumps(lastField),val1=lastVal)
    #return send_from_directory(UPLOAD_FOLDER,feedID+'.csv')

@app.route('/data/<feedID>/latest/csv')
def get_latest_data_from_file_csv(feedID):
    uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.csv')
    #data=np.loadtxt(uploadFilePath)
    reader=csv.reader(open(uploadFilePath,"rb"),delimiter=',')
    reader.next() #skip header line
    x=[]
    for row in reader:
        x.append(row)
#    x=list(reader)
    lastItem=x[len(x)-1]
    timeStamp=lastItem[0]
    lastField=lastItem[1]
    lastVal=lastItem[2]
    return timeStamp+","+lastField+","+lastVal

@app.route('/data/<feedID>/plot')
def plot(feedID):

    uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.csv')
    #data=np.loadtxt(uploadFilePath)
    reader=csv.reader(open(uploadFilePath,"rb"),delimiter=',')
    reader.next() #skip header line
    x=[]
    for row in reader:
        x.append(row)
#    x=list(reader)
    a=np.asarray(x)
    label=a[:,1][0] #column heading
    dates=a[:,0]
    vals=np.asarray(a[:,2],dtype='float')
    ds=[datetime.datetime.strptime(d,"%Y-%m-%d %H:%M:%S") for d in dates]


#    fig=plt.figure()
#    fig.set_frameon(False)
#    ax=fig.add_subplot(111)
#    ax.set_axis_off()
#    ax.patch.set_alpha(0.0)
#    ndvi_plot = ax.plot(vals)

#    imageOutPath=os.path.join(app.config['UPLOAD_FOLDER'],'test.png')
#    fig.savefig(imageOutPath)
#    return "yep"

    fig=Figure()
    ax=fig.add_subplot(111)
    #ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    #ax.xaxis.set_major_locator(MinuteLocator())
    ax.plot(ds,vals,'-o',label=label)
    dslength=len(ds)
#    print dslength
    xmin= ds[dslength-11]
    xmax= ds[dslength-1]
#    print xmin,xmax
    ymin=vals.min()
    ymin=ymin-.1*ymin
    ymax=vals.max()
    ymax=ymax+.1*ymax
#    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.legend()
    #ax.plot(vals,'-.')
    #ax.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response



@app.route('/')
def index():
    return render_template('index.html')


@app.route("/data")
@app.route("/data/<int:ndata>")
def randdata(ndata=100):
    """
    On request, this returns a list of ``ndata`` randomly made data points.

    :param ndata: (optional)
        The number of data points to return.

    :returns data:
        A JSON string of ``ndata`` data points.

    """
    x = 10 * np.random.rand(ndata) - 5
    y = 0.5 * x + 0.5 * np.random.randn(ndata)
    A = 10. ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
        "color": c[i]}
        for i in range(ndata)])


@app.route("/testScatter")
def testScatter():
    return render_template("plotd3_2.html")

@app.route('/data/<feedID>/plotd3')
def plotd3(feedID):
    #filename='poop'
    #uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],feedID+'.csv')
    #uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],'data.csv')
    
    return render_template('plotd3noob.html', filename='/data/'+str(feedID)+'/csv')


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': task } ), 201

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )



