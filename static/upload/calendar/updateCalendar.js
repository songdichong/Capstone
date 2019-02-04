/*
Original Author: Yue Ma
Creation date: Jan 27th, 2019
Contents of file:
	1. fetch calendar events based on the calendar ID
*/
$(function() {
    $('#calendarList').gCalReader({ calendarId:'en.usa#holiday@group.v.calendar.google.com', apiKey:'AIzaSyBvbDOa1m-gETLQgRjN5nHPt2xElEFiTZ8'});
});

// window.calendarList = function($elem) {
//     console.log($elem);
//     var top = parseInt($elem.css("top"));
//     var temp = -1 * $('#calendarList > li').height();
//     if (top < temp) {
//         top = $('#calendarList').height()
//         $elem.css("top", top);
//     }
//     $elem.animate({
//         top: (parseInt(top) - 60)
//     }, 600, function() {
//         window.calendarList($(this))
//     });
//     }
//     $(document).ready(function() {
//     var i = 0;
//     $("#calendarList > li").each(function() {
//         $(this).css("top", i);
//         i += 60;
//         window.calendarList($(this));
//     });
// });
  
  

