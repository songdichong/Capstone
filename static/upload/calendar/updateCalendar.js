/*
Original Author: Yue Ma
Creation date: Jan 27th, 2019
Contents of file:
	1. fetch calendar events based on the calendar ID
*/

$(function() {
    let gmail = window.location.href.split('/')[5];
    console.log(gmail);
    $('#calendarList').gCalReader({ calendarId:gmail, apiKey:'AIzaSyBvbDOa1m-gETLQgRjN5nHPt2xElEFiTZ8'});
});
  
// $('body').keypress(function(e) {
//     console.log(111)
//     console.log('keypress',String.fromCharCode(e.which))
// });

