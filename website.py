'''
Original Author: Dichong Song
Creation date: Jan 10, 2019
Contents of file: 
	1. Flask framework (main thread) 
		1.1 render static html source
		1.2 communicate with frontend web page
		1.3 always on
	2. Xml fetcher (sub-thread)
		2.1 parse content from given url
		2.2 output in json format
		2.3 repeat every hour
'''
from flask import Flask,render_template,jsonify,request,session,redirect,url_for
from flask_bootstrap import Bootstrap
from xml.dom import minidom
from urllib.request import urlopen
from pygame.locals import *
import sched, time, _thread,json,io,shlex,subprocess

app=Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
islogin = 0

def xmlfetcher(urllink):
	xml_file = urlopen(urllink)
	mydoc = minidom.parse(xml_file)
	items = mydoc.getElementsByTagName('title')
	result = []
	for item in items:
		result.append(item.firstChild.data)
	return result

def write_to_json(): 
	my_list = xmlfetcher("https://www.cbc.ca/cmlink/rss-topstories")
	f1 = open("./static/upload/newsfeed/news.json","w")
	with io.open('./static/upload/newsfeed/news.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(my_list, ensure_ascii=False))
	s.enter(3600, 1, write_to_json)
	s.run()
	
def execute_cmd(cmd):
	args = shlex.split(cmd)
	p = subprocess.run(args,stdout = subprocess.PIPE)
	result = p.stdout
	print(result)
	
def remote_controller():
	pass
				
		
@app.route('/',methods=['GET','POST'])
def index():
	if request.method == "POST":
		data = request.form['request'].encode('utf-8')
		print(data)
		if islogin == 0:
			return jsonify(result = {'username':'songdichong'})
	return render_template('mainPage.html')
		
@app.route('/specialUserPage',methods = ['GET','POST'])
def login():
	some_data1 = {'a':"some data from back123"}
	return render_template('specialUserPage.html',data = some_data1)

if __name__=="__main__":
	_thread.start_new_thread(write_to_json,())
	_thread.start_new_thread(remote_controller,())
	app.debug=True
	app.run(host='0.0.0.0',port='4110')


