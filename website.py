'''
Original Author: Dichong Song, Yuhan Ye, Yue Ma, Shengyao Lu
Creation date: Jan 10, 2019
Contents of file: 
	1. Flask framework (main thread) 
		1.1 render static html source
		1.2 accept message from frontend web page
		1.3 monitor the login/register state
		1.4 handles the login/logout state and send corresponding data to front end
		1.5 find information in database and register in database
		1.6 always on
	2. Xml fetcher (sub-thread)
		2.1 parse content from given url
		2.2 output in json format
		2.3 repeat every hour
	3. FaceDetection
'''
from flask import Flask,render_template,jsonify,request,session,redirect,url_for
from xml.dom import minidom
from urllib.request import urlopen
from pyfingerprint.pyfingerprint import PyFingerprint
import sched, time, _thread,json,io,shlex,subprocess,datetime,sqlite3,requests,os
######################### Constant Division ############################
FRONT_END_MSG_RESPOND = 3
FRONT_END_MSG_TAKE_PHOTO = 2
INVALID_USER = -1
MODE_INITIAL = 0
MODE_LOGIN = 1
MODE_REGISTER = 2
MODE_LOGOUT = 3
MODE_FINGERPRINT_REGISTERED = 4
NOT_SELECTED = "A"
SELECETED = "B"
preference = "AAAA"
########################################################################

###################### Initialization Division #########################
app=Flask(__name__)
CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
s = sched.scheduler(time.time, time.sleep)
username = ""
email = ""
userID = INVALID_USER
DETECTEDUSER = [1,1,1]
mode = MODE_INITIAL
databaseName = 'test.db'
########################################################################

################### Useful Function Division ###########################
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
	return result

def select_from_database(userID,databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	t = (int(userID),)
	c.execute('SELECT * FROM User WHERE findex=?',t)
	a=c.fetchone()
	conn.commit()
	conn.close()
	return a

def add_into_database(userID,username,email,preference,databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''
	INSERT INTO User(findex,username,email,preference)VALUES(?,?,?,?)
	''',(userID,username,email,preference))
	conn.commit()
	conn.close()

def update_database(userID,username,email,preference,databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''
	UPDATE User
	set username=?,email=?,preference=?
	where findex=?
	''',(username,email,preference,userID))
	conn.commit()
	conn.close()	

def createTable(databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''
	CREATE TABLE IF NOT EXISTS USER(findex int,username String,email String,preference String)
	''')
	conn.commit()
	conn.close()

def execute_search_fingerprint():
	url = "http://0.0.0.0:4311/search"
	data = {'data': 1}
	r = requests.post(url, data)

def execute_activate_fingerprint():
	url = "http://0.0.0.0:4311/activate"
	data = {'data': 1}
	r = requests.post(url, data)

def execute_enroll_fingerprint():
	url = "http://0.0.0.0:4311/register"
	data = {'data': 1}
	r = requests.post(url, data)

def execute_exit_fingerprint():
	url = "http://0.0.0.0:4311/exit"
	data = {'data': 1}
	r = requests.post(url, data)

def execute_send_email(filename, email):
	os.system('''echo "" | mail -s "Photo taken from mirror" ''' + "-A " + filename + " " + email)
########################################################################

########################## Flask Division ##############################
@app.route('/',methods=['GET','POST'])
def index():
	global userID,username,email,mode,preference,CURRENT_WORKING_DIRECTORY
	if request.method == "POST":
		data = request.form['request'].encode('utf-8')
		print("data",data)
		print("userID",userID)
		print("mode",mode)
		if (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_LOGIN):
			#successfully login
			result = select_from_database(userID,databaseName)
			username = result[1]
			email = result[2]
			preference = result[3]
			mode = MODE_INITIAL
			print(username)
			return jsonify({"mode":"login_success","username":username,"email":email,"preference":preference})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID == INVALID_USER) and (mode == MODE_LOGIN):
			#unknown user
			mode = MODE_INITIAL
			execute_search_fingerprint()
			return jsonify({"mode":"login_fail"})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_REGISTER):
			#register
			add_into_database(userID,username,email,preference,databaseName)
			mode = MODE_INITIAL
			userID = INVALID_USER
			return jsonify({"mode":"register_success","username":username,"email":email,"preference":preference})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_FINGERPRINT_REGISTERED):
			result = select_from_database(userID,databaseName)
			if result == None:	
				add_into_database(userID,username,email,preference,databaseName)
			else:
				update_database(userID,username,email,preference,databaseName)
			
				
			mode = MODE_INITIAL
			userID = INVALID_USER
			execute_search_fingerprint()
			return jsonify({"mode":"update_success","username":username})
			
		elif (int(data) == FRONT_END_MSG_RESPOND) and (mode == MODE_LOGOUT):
			#logout 
			mode = MODE_INITIAL
			username = ""
			email = ""
			userID = INVALID_USER
			return jsonify({"mode":"logout_success"})
		
		elif (int(data) == FRONT_END_MSG_TAKE_PHOTO):
			try:
				print("take photo")
				execute_cmd("mkdir -p " + CURRENT_WORKING_DIRECTORY + '/' + username)
				filename = username + "_" + datetime.datetime.now().strftime("%B_%d_%Y_%H:%M:%S")+".jpg"
				path_file =  CURRENT_WORKING_DIRECTORY + "/" + username + "/" + filename
				msg = execute_cmd("raspistill -n -o "+path_file)
				_thread.start_new_thread(execute_send_email,(path_file,email,))
				return jsonify({"mode":"photo_success"})
			except Exception:
				print("some error happens 1")
				return render_template("specialUserPage.html")
				
	return render_template('mainPage.html')

@app.route('/signup',methods=['POST'])
def signup():
	global username,email,mode,userID,preference 
	if request.method == "POST":
		email = request.form['gml']
		username = request.form['uname']
		newsPref = NOT_SELECTED 
		weatherPref = NOT_SELECTED 
		stockPref = NOT_SELECTED 
		calendarPref = NOT_SELECTED 
		
		
		try:
			newsPref = request.form['news']
			newsPref = SELECETED
		except Exception:
			pass
		
		try:
			weatherPref = request.form['fullWeather']
			weatherPref = SELECETED
		except Exception:
			pass
			
		try:
			stockPref = request.form['stock']
			stockPref = SELECETED
		except Exception:
			pass
			
		try:
			calendarPref = request.form['calendar']
			calendarPref = SELECETED
		except Exception:
			pass
		preference = calendarPref + newsPref + stockPref + weatherPref
		mode = MODE_REGISTER
		execute_enroll_fingerprint()
		print("here signup")
		
	return redirect('/')
		
@app.route('/specialUserPage',methods = ['GET'])
def specialUserPage():
	return render_template("specialUserPage.html")

@app.route('/login',methods = ['POST'])
def login():
	global userID,mode
	if request.method == "POST":
		data = request.form['userID']
		print(data)
		userID = int(data)
		mode = MODE_LOGIN
		return "success"

@app.route('/register',methods = ['POST'])
def register():
	global userID,mode
	if request.method == "POST":
		print("here")
		userID = request.form['positionNumber']
		goToSignUp = int(request.form['goToSignUp'])
		print(userID,goToSignUp)
		if goToSignUp == 0:
			mode = MODE_FINGERPRINT_REGISTERED
		else:
			mode = MODE_REGISTER
		return "success"
		
@app.route('/getUserFace',methods = ['POST'])
def getUserFace():
	global mode,DETECTEDUSER
	if request.method == "POST":
		data = int(request.form['isDetected'])
		if data == 0:
			if DETECTEDUSER == [0,0,0]:
				#turn off screen only when receive 3 continuous False
				mode = MODE_LOGOUT
				execute_cmd("xset dpms force off")
				execute_exit_fingerprint()
		else:
			#turn on screen immediately
			execute_cmd("xset dpms force on")
			execute_search_fingerprint()
		print(DETECTEDUSER)
		DETECTEDUSER.pop(0)
		DETECTEDUSER.append(data)
		return "success"
########################################################################

######################### Main Function ################################
if __name__=="__main__":
	execute_cmd("sudo fuser -k /dev/ttyUSB0")
	execute_search_fingerprint()
	_thread.start_new_thread(write_to_json,())
	createTable(databaseName)
	
	app.run(host='0.0.0.0',port = 4310)
########################################################################
