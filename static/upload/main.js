/*
Original Author: Dichong Song
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
	2. If login success, jumps to specialuserpage; otherwise, alert not correct
*/

var username;
var KEY_F2 = 113;
var KEY_Q = 81;
var KEY_ENTER = 13;
var KEY_UPARROW = 38;
var KEY_DOWNARROW = 40;
var KEY_LEFTARROW = 37;
var KEY_RIGHTARROW = 39;
var KEY_DELETE = 46;
var FRONT_END_MSG_RESPOND = 3;
var FRONT_END_MSG_REISTER = 1;
var LOGIN_FAIL = "login_fail";
var LOGIN_SUCCESS = "login_success";
var REGISTER_SUCCESS = "register_success";
var UPDATES_SUCCESS = "update_success";
var RECORD_FINGERPRINT = "record_finger";
document.addEventListener('keydown', function(e) {
	if (e.keyCode === KEY_F2 || e.keyCode === KEY_Q){
	  runAjax(FRONT_END_MSG_REISTER);
	  clearInterval(keeppost);
	}
	else if(e.keyCode === KEY_ENTER){

		document.getElementById('id01').style.display='block';
		document.getElementById("uname").focus();
	}
	else if(e.keyCode===KEY_UPARROW && isRegistering()){
		document.getElementById("calendarButton").click();

	}
	else if(e.keyCode===KEY_DOWNARROW && isRegistering()){
		document.getElementById("newsButton").click();

	}
	else if(e.keyCode===KEY_LEFTARROW && isRegistering()){
		document.getElementById("stockButton").click();

	}
	else if(e.keyCode===KEY_RIGHTARROW && isRegistering()){
		document.getElementById("weatherButton").click();

	}
	else if(e.keyCode===KEY_DELETE && isRegistering()){
		document.getElementById('id01').style.display='none'
	}
});

function isRegistering(){
	return document.getElementById('id01').style.display==='block'
}

function runAjax(REQUEST) {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':REQUEST},
		success: function(result){
			if (result.mode == LOGIN_FAIL){
				$('.alert').html('User cannot be recognized.\n Please register first!').addClass('alert-warning').show().delay(2000).fadeOut();

			}
			if (result.mode == RECORD_FINGERPRINT){
				$('.alert').html('Now please record your fingerprint.\n You need to record it twice.').addClass('alert-warning').show().delay(2000).fadeOut();
				window.location.href="/";
			}
			
			if (result.mode ==  REGISTER_SUCCESS){
				username = result.username;
				useremail = result.email;//Yue add
				userpreference = result.preference;//Yue add
				window.location.href="/specialUserPage?/"+username+"/"+useremail+"/"+userpreference;
			}
			
			if (result.mode == UPDATES_SUCCESS){
				username = result.username;
				useremail = result.email;//Yue add
				userpreference = result.preference;//Yue add
				$('.alert').html("update success\n Your new information is:" + username).addClass('alert-success').show().delay(2000).fadeOut();
				window.location.href="/specialUserPage?/"+username+"/"+useremail+"/"+userpreference;
			}

			if (result.mode == LOGIN_SUCCESS) {
				username = result.username;
				useremail = result.email;//Yue add
				userpreference = result.preference;//Yue add
				console.log(username);
				window.location.href="/specialUserPage?/"+username+"/"+useremail+"/"+userpreference;
			}
		}
	});
}

// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

var keeppost = setInterval(readFace, 2000);
function readFace() {
    runAjax(FRONT_END_MSG_RESPOND);
}

//voice control
// Create a variable that stores your instance
const artyom = new Artyom();


// or add some commandsDemostrations in the normal way
artyom.addCommands([
	{
		indexes: ['/^.*sign up.*$/i','/^.*register.*$/i','sign up','sign me up', 'log in'],
		action: (i) => {
			document.getElementById('id01').style.display='block';
			document.getElementById("uname").focus();

		}
	},
]);

// Start the commands !
artyom.initialize({
	lang: "en-US", // GreatBritain english
	continuous: true, // Listen forever
	soundex: true,// Use the soundex algorithm to increase accuracy
	debug: true, // Show messages in the console
	executionKeyword: "and do it now",
	listen: true, // Start to listen commands !

	// If providen, you can only trigger a command if you say its name
	// e.g to trigger Good Morning, you need to say "Jarvis Good Morning"
	//name:"Victoria"
}).then(() => {
	console.log("Artyom has been succesfully initialized");
}).catch((err) => {
	console.error("Artyom couldn't be initialized: ", err);
});
