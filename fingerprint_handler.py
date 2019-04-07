from flask import Flask,request
import requests,shlex,subprocess,_thread,os
SEARCH = 1
REGISTER = 2
OFF = 0

app=Flask(__name__)
mode = OFF
CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
def execute_cmd(cmd):
	args = shlex.split(cmd)
	p = subprocess.run(args,stdout = subprocess.PIPE)
	result = p.stdout
	return result

def execute_search_fingerprint():
	execute_cmd("sudo python3 "+ CURRENT_WORKING_DIRECTORY + "/pyFingerprint/example_search.py")


def execute_enroll_fingerprint():
	execute_cmd("sudo python3 "+ CURRENT_WORKING_DIRECTORY + "/pyFingerprint/example_enroll.py")

@app.route('/register',methods = ['POST'])
def register():
	global mode
	if request.method == "POST":
		execute_cmd("sudo fuser -k /dev/ttyUSB0")
		_thread.start_new_thread(execute_enroll_fingerprint,())
		mode = REGISTER
	return "success"

@app.route('/search',methods = ['POST'])
def search():
	global mode
	if request.method == "POST":
		if mode == OFF:
			_thread.start_new_thread(execute_search_fingerprint,())
			mode = SEARCH
	return "success"

@app.route('/exit',methods = ['POST'])
def exit():
	global mode
	if request.method == "POST":
		execute_cmd("sudo fuser -k /dev/ttyUSB0")
		mode = OFF
	return "success"


app.run(host='0.0.0.0',port = 4311)
