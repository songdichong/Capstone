from flask import Flask,render_template,jsonify,request,session,redirect,url_for
from flask_bootstrap import Bootstrap
from xml.dom import minidom
from urllib.request import urlopen
import sched, time, _thread,json,io

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
	bootstrap=Bootstrap(app)
	app.debug=True
	app.run(host='0.0.0.0',port='4300')
