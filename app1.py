from flask import Flask, render_template, request
import matplotlib.pyplot as plt; plt.rcdefaults()
import plotly.graph_objects as go
import sqlite3 as sql
import pandas as pd
import sqlite3  
import numpy as np
import os
import random
warn="no"
error="no"
Table_Name = "Parts_Info"


app = Flask(__name__)

def Extract(value):
	global Table_Name
	con = sqlite3.connect("HW_Parts.db")
	cur = con.cursor()		
	sql = "SELECT DISTINCT " +value+", count("+value+") FROM "+Table_Name+" GROUP BY "+value+";"
	x=[]
	y=[]
	for row,n in cur.execute(sql):
		x.append(row)
		y.append(n)
	return x,y
def help():
	global Table_Name
	con = sqlite3.connect("HW_Parts.db")
	cur= con.cursor()
	cursor = con.execute('select * from '+Table_Name)
	names = list(map(lambda x: x[0], cursor.description))
	return names

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/dash')
def dash():
		cols=help()
		return render_template('Dashboard.html',cols=cols)

@app.route('/bar', methods=['GET', 'POST'])	
def bar():
	global warn
	global error
	global Table_Name
	fl='static/Reports/Barchart.png'
	if os.path.exists(fl):
		os.remove(fl)
		
	if request.method == 'POST':
		val = request.form['object']
	cols=help()
	if val not in cols:
		return render_template('Dashboard.html',error="yes",head=val,cols=cols)
	x,y=Extract(val)
	y_pos = np.arange(len(x))
	plt.barh(y_pos, y, align='center', alpha=0.5,color=(0.2, 0.4, 0.6, 0.6))
	plt.yticks(y_pos, x)
	plt.xlabel(val)
	plt.title("Bar Chart")
	for index, value in enumerate(y):
		plt.text(value, index, str(value))
	total= len(x)
	if(total>10):
		warn="o"
	if(plt.savefig(fl,bbox_inches = 'tight')):
		plt.clf()
		return render_template('Dashboard.html',l=x,g=y,f=fl,res="Barchart",head=val)
	else:
		plt.savefig(fl,bbox_inches = 'tight')
		plt.clf()
		return render_template('Dashboard.html',l=x,g=y,f=fl,res="Barchart",head=val,warn=warn,cols=cols)

@app.route('/pie', methods=['GET', 'POST'])
def pie():
	global Table_Name
	global warn
	global error
	fl='static/Reports/Piechart.png'
	if os.path.exists(fl):
		os.remove(fl)
	if request.method == 'POST':
		val = request.form['object']
	cols=help()
	if val not in cols:
		return render_template('Dashboard.html',error="yes",head=val,cols=cols)
	x,y=Extract(val)
	number_of_colors = len(x)
	total= len(x)
	if(total>10):
		warn="o"
	color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])for i in range(number_of_colors)]
	plt.pie(y, labels=x, colors=color,autopct='%1.1f%%', shadow=True, startangle=140)
	plt.axis('equal')
	plt.savefig(fl,bbox_inches = 'tight')
	plt.clf()
	return render_template('Dashboard.html',l=x,g=y,f=fl,res="Piechart",head=val,warn=warn,cols=cols,error=error)

@app.route('/sca', methods=['GET', 'POST'])
def sca():
	global Table_Name
	global warn
	global error
	fl='static/Reports/Scatter-plot-chart.png'
	
	if os.path.exists(fl):
		os.remove(fl)
	if request.method == 'POST':
		val = request.form['object']
	cols=help()
	if val not in cols:
		return render_template('Dashboard.html',error="yes",head=val,cols=cols)
	x,y=Extract(val)
	total= len(x)
	if(total>10):
		warn="o"
	plt.scatter(x, y) 
	plt.savefig(fl,bbox_inches = 'tight')
	plt.clf()
	return render_template('Dashboard.html',l=x,g=y,f=fl,res="Scatter-plot-chart",head=val,warn=warn,cols=cols,error=error)

@app.route('/line', methods=['GET', 'POST'])
def line():
	global warn
	global error
	global Table_Name
	fl='static/Reports/Line-plot-chart.png'

	if os.path.exists(fl):
		os.remove(fl)
	cols=help()
	if request.method == 'POST':
		val = request.form['object']
	cols=help()
	if val not in cols:
		return render_template('Dashboard.html',error="yes",head=val,cols=cols)
	x,y=Extract(val)
	total= len(x)
	if(total>10):
		warn="o"
	plt.plot(x,y) 
	plt.savefig(fl,bbox_inches = 'tight')
	plt.clf()
	return render_template('Dashboard.html',l=x,g=y,f=fl,res="Line-plot-chart",head=val,warn=warn,cols=cols,error=error)

@app.route('/view', methods=['GET', 'POST'])
def view():
	global Table_Name
	con = sqlite3.connect("HW_Parts.db")
	cur=con.execute("SELECT * FROM "+Table_Name)
	data = cur.fetchall()
	names = list(map(lambda x: x[0], cur.description))
	return render_template('view.html', data=data,clname=names,cols=names)


@app.route('/query', methods=['GET', 'POST'])
def query():
	con = sqlite3.connect("HW_Parts.db")
	if request.method == 'POST':
		val = request.form['object']

	cur=con.execute(val)
	data = cur.fetchall()
	cols=help()
	names = list(map(lambda x: x[0], cur.description))
	return render_template('view.html', data=data,clname=names,cols=cols)

if __name__ == '__main__':
	app.run(debug = True)