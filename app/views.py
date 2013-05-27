from flask import jsonify
from flask import request

from app import app

@app.route('/data')
def data():
	field1=request.args.get('field1')
	val1=request.args.get('val1')
	json = jsonify(field1=val1)
	return json

@app.route('/')
def index():
    return 'Hello!'
