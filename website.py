from flask import Flask,render_template,jsonify,request,session
from flask_bootstrap import Bootstrap
from xml.dom import minidom
import sched, time, _thread,json,io

app=Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

def xmlfetcher(filename):
	mydoc = minidom.parse(filename)
	items = mydoc.getElementsByTagName('title')
	result = []
	for item in items:
		result.append(item.firstChild.data)
	return result


def write_to_json(): 
	my_list = xmlfetcher("HomePage.xml")
	f1 = open("outfile.json","w")
	with io.open('outfile.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(my_list, ensure_ascii=False))
	s.enter(3600, 1, write_to_json)
	s.run()

@app.route('/',methods=['GET','POST'])
def index():
	# website post method 
	if request.method == "POST":
		return jsonify(data = some_data)
	# website get method
	some_data = "some data from back"
	#jsonify(data = some_data)
	return render_template('index.html')

if __name__=="__main__":
	_thread.start_new_thread(write_to_json,())
	bootstrap=Bootstrap(app)
	app.debug=True
	app.run(host='0.0.0.0')
	
