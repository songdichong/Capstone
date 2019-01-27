from flask import Flask,render_template,jsonify,request,session
from flask_bootstrap import Bootstrap
from xml.dom import minidom
app=Flask(__name__)

def xmlfetcher(filename):
	mydoc = minidom.parse(filename)
	items = mydoc.getElementsByTagName('title')
	result = []
	for item in items:
		result.append(item.firstChild.data)
	return result
	
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
	bootstrap=Bootstrap(app)
	app.debug=True
	app.run(host='0.0.0.0')

