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
from xml.dom import minidom
from urllib.request import urlopen
import sched, time, _thread,json,io,shlex,subprocess,datetime,hashlib,sqlite3
from pyfingerprint.pyfingerprint import PyFingerprint
from watchdog.observers import Observer
from watchdog.events import *

app=Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
userID = -1
currentUser = -1
isupdated = 0


class FileEventHandler(FileSystemEventHandler):
	def __init__(self):
		FileSystemEventHandler.__init__(self)

	def on_moved(self, event):
		if event.is_directory:
			print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
		else:
			print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

	def on_created(self, event):
		if event.is_directory:
			print("directory created:{0}".format(event.src_path))
		else:
			print("file created:{0}".format(event.src_path))

	def on_deleted(self, event):
		if event.is_directory:
			print("directory deleted:{0}".format(event.src_path))
		else:
			print("file deleted:{0}".format(event.src_path))

	def on_modified(self, event):
		global isupdated
		if event.is_directory:
			print("directory modified:{0}".format(event.src_path))
		else:
			isupdated = 1
			print("file modified:{0}".format(event.src_path))

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

def update_userID():
	global userID,isupdated
	observer = Observer()
	event_handler = FileEventHandler()
	observer.schedule(event_handler,'/home/cmput274/Capstone/',True)
	observer.start()
	while True:
		with open('loginstate.txt', 'r') as f:
			if isupdated == 1:
				try:
					lines = f.read().splitlines()
					last_line = lines[-1]
					if last_line == userID:
						pass
					else:
						userID = last_line
					isupdated = 0
				except Exception:
					pass
		time.sleep(1)
def select_from_database(userID):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	t = (int(userID),)
	c.execute('SELECT * FROM User WHERE findex=?',t)
	a=c.fetchone()
	conn.commit()
	conn.close()
	return a
	
def add_into_database(userID,username,email,preference):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('''
	INSERT INTO User(findex,username,email,preference)VALUES(?,?,?,?)
	''',(userID,username,email,preference))
	conn.commit()
	conn.close()

@app.route('/',methods=['GET','POST'])
def index():
	global userID,currentUser
	if request.method == "POST":
		data = request.form['request'].encode('utf-8')
		print(data)
		if (int(data) == 3 ) and (userID != "-1") and (userID != currentUser):
			#successfully login
			currentUser = userID
			result = select_from_database(userID)
			username = result[1]
			email = result[2]
			preference = result[3]
			print(username)

			return jsonify({"username":username})
		elif int(data) == 2:
			try:
				execute_cmd("mkdir -p " + username)
				filename = username + "_" + datetime.datetime.now().strftime("%B_%d_%Y_%H:%M:%S")+".jpg"
				msg = execute_cmd("raspistill -n -o "+"./"+username +"/"+filename)
				return jsonify({"status":msg})
			except Exception:
				print("some error happens 1")
				return render_template("specialUserPage.html")
	return render_template('mainPage.html')
	
def search_fingerprint():
	## Tries to initialize the sensor
        try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
                file1 =  open("loginstate.txt","a+")
                if ( f.verifyPassword() == False ):
                        raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
                #~ exit(1)

        
        
        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

                ## Tries to search the finger and calculate hash
        try:
                print('Waiting for finger...')

                ## Wait that finger is read
                while ( f.readImage() == False ):
                        pass

                ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)
                
                ## Searchs template
                result = f.searchTemplate()
                print (result)
                positionNumber = result[0]
                accuracyScore = result[1]

                if ( positionNumber == -1 ):
                        print('No match found!')
                        #~ search_fingerprint()
                    #~ exit(0)
                else:
                        print('Found template at position #' + str(positionNumber))
                        print('The accuracy score is: ' + str(accuracyScore))
                file1.write(str(positionNumber)+'\n')
                file1.flush()
                ## OPTIONAL stuff
                ##
                ## Loads the found template to charbuffer 1
                f.loadTemplate(positionNumber, 0x01)
                print("1")
                print(result)
                ## Downloads the characteristics of template loaded in charbuffer 1
                characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                print("2")
                print(result)
                ## Hashes characteristics of template
                print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
                time.sleep(1)
                
        except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                #~ exit(1)
        time.sleep(1)
        search_fingerprint()
        

@app.route('/signup',methods=['POST'])
def signup():
	print(1234)
	if request.method == "POST":
		print('GMAIL:'+request.form['gml'])
		print('UserName:'+request.form['uname'])

	return redirect("/")
	
@app.route('/specialUserPage',methods = ['GET'])
def specialUserPage():
	return render_template("specialUserPage.html")

@app.route('/login',methods = ['POST'])
def login():
	global userID
	if request.method == "POST":
		data = request.form['userID']
		print(data)
		userID = int(data)
		return "success"

def print_global():
	global userID
	while True:
		print(userID)
		time.sleep(1)
	
if __name__=="__main__":
	#~ file1 =  open("loginstate.txt","w")
	#~ file1.write('-1\n')
	#~ file1.close()
	
	_thread.start_new_thread(write_to_json,())
	#~ _thread.start_new_thread(search_fingerprint,())
	#~ _thread.start_new_thread(update_userID,())
	#~ _thread.start_new_thread(print_global,())
	app.debug=True
	app.run(host='0.0.0.0',port=4310)
	
