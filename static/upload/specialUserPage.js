/*
Original Author: Shengyao Lu
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
*/
var KEY_ENTER = 13;
var FRONT_END_MSG_RESPOND = 3;
var FRONT_END_MSG_TAKE_PHOTO = 2;
var TAKE_PHOTO_SUCCESS = "photo_success";
var LOGOUT_SUCCESS = "logout_success";

let preference = window.location.href.split('/')[6]; //calendar news stock weather
let name = window.location.href.split('/')[4]; //calendar news stock weather

$('.alert').html('Hi, '+ name).addClass('alert-welcome').show().delay(2000).fadeOut();

document.addEventListener('keydown', function(e) {

	if (e.keyCode == KEY_ENTER){
	  e.keypress = '1';
	  runAjax(FRONT_END_MSG_TAKE_PHOTO);
	}
});


if(preference[0]==='0'){

	var div = document.getElementById('calendarList');
	div.style.visibility = "hidden";
	div.style.display = "none";

}
if(preference[1]==='0'){

	var div = document.getElementById('news');
	div.style.visibility = "hidden";
	div.style.display = "none";

}
if(preference[2]==='0'){

	var div = document.getElementById('trade');
	div.style.visibility = "hidden";
	div.style.display = "none";

}
if(preference[3]==='0'){

	var div = document.getElementById('weather');
	div.style.visibility = "hidden";
	div.style.display = "none";

} else {
	var div = document.getElementById('weather_small');
	div.style.visibility = "hidden";
	div.style.display = "none";
}




function runAjax(REQUEST) {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':REQUEST},
		success: function(result){
			if (result.mode == TAKE_PHOTO_SUCCESS){
				// the alert will disappear after 3 seconds. 
				$('.alert').html('A photo has been taken. We will implement a way for you to check it later!').addClass('alert-success').show().delay(2000).fadeOut();
			}
			if (result.mode == LOGOUT_SUCCESS) {
				window.location.href="/";
			}
		}
	});
}

setInterval(readFace, 2000);
function readFace() {
    runAjax(FRONT_END_MSG_RESPOND);
}
//voice control


// Create a variable that stores your instance
const artyom = new Artyom();

// Or if you are using it in the browser
// var artyom = new Artyom();// or `new window.Artyom()`

// Add command (Short code artisan way)
artyom.on(['Good morning','Good afternoon']).then((i) => {
	switch (i) {
		case 0:
			console.log('Good morning, how are you?');
			break;
		case 1:
			console.log('Good afternoon, how are you?');
			break;
	}
});

// or add some commandsDemostrations in the normal way
artyom.addCommands([
	{
		indexes: ['Hello','Hi','/^.*Hello.*$/i'],
		action: (i) => {
		}
	},
	{
		indexes: ['Log out','Bye','Goodbye','See you','buy','by'],
		action: (i) => {
			window.location.href="/";

		}
	},
	// The smart commands support regular expressions
	{
		indexes: [/^.*photo.*$/i],
		smart:true,
		action: (i,wildcard) => {
			console.log('Ready for photo');
			runAjax(FRONT_END_MSG_TAKE_PHOTO);

		}
	},
	{
		indexes: ['shut down yourself'],
		action: (i,wildcard) => {
			artyom.fatality().then(() => {
				console.log("Artyom succesfully stopped");
			});
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
