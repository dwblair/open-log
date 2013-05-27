from flask import jsonify
from flask import request, send_from_directory, make_response, redirect, url_for
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
	x=list(reader)

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
	x=list(reader)
	a=np.asarray(x)
	label=a[:,1][0] #column heading
	dates=a[:,0]
	vals=np.asarray(a[:,2],dtype='float')
	ds=[datetime.datetime.strptime(d,"%Y-%m-%d %H:%M:%S") for d in dates]


#	fig=plt.figure()
#	fig.set_frameon(False)
#	ax=fig.add_subplot(111)
#	ax.set_axis_off()
#	ax.patch.set_alpha(0.0)
#	ndvi_plot = ax.plot(vals)

#	imageOutPath=os.path.join(app.config['UPLOAD_FOLDER'],'test.png')
#	fig.savefig(imageOutPath)
#	return "yep"

	fig=Figure()
	ax=fig.add_subplot(111)
	#ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
	ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
	#ax.xaxis.set_major_locator(MinuteLocator())
	ax.plot(ds,vals,'-',label=label)
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
    return 'Hello!'
