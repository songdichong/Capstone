/*
Original Source: https://github.com/bradoyler/GoogleCalReader-jquery-plugin/issues/12
Original Author: bradoyler
Secondary Editor: Shengyao Lu & Yue Ma
Creation date: Jan 27th, 2019
Contents of file:
	1. Google Calendar feed reader - plugin to get upcoming events from a public google calendar
*/

(function($) {

    $.fn.gCalReader = function(options) {
      var $div = $(this);  
      var defaults = $.extend({
          calendarId: 'en.usa#holiday@group.v.calendar.google.com',
          apiKey: 'Public_API_Key',
          dateFormat: 'ShortDate+ShortTime',
          errorMsg: 'No events in calendar',
          maxEvents: 5,
          futureEventsOnly: true,
          sortDescending: false
        },
        options);
  
      var s = '';
      var feedUrl = 'https://www.googleapis.com/calendar/v3/calendars/' +
        encodeURIComponent(defaults.calendarId.trim()) +'/events?key=' + defaults.apiKey +
        '&orderBy=startTime&singleEvents=true';
        if(defaults.futureEventsOnly) {
          feedUrl+='&timeMin='+ new Date().toISOString();
        }  
      $.ajax({
        url: feedUrl,
        dataType: 'json',
        success: function(data) {
          if(defaults.sortDescending){
            data.items = data.items.reverse();
          }
          data.items = data.items.slice(0, defaults.maxEvents);

          $.each(data.items, function(e, item) {
            var eventdate = item.start.dateTime || item.start.date ||'';
            var eventdate2 = item.end.dateTime || item.end.date ||'';
    
            if(item.start.dateTime == null){
                var mydate = new Date(eventdate2);
               eventdate2 = date2str(mydate, 'yyyy-MM-dd');
            } 
            console.log("0- "+eventdate);
            console.log("00- "+eventdate2);
            var summary = item.summary || '';
            var description = item.description;
            var location = item.location;
            var eventDate = formatDate(eventdate, defaults.dateFormat.trim());
            var eventDate2 = formatDate(eventdate2, defaults.dateFormat.trim());
            console.log("2- "+eventDate);
            console.log("3- "+eventDate2);
            console.log("4- "+location);
            console.log("5- "+description);
            console.log("6- "+summary);
            s ='<div class="eventtitle"> &nbsp&nbsp'+ summary +'</div>';
            s +='<div class="eventdate"> &nbsp&nbsp&nbsp&nbsp&nbsp'+ eventDate +'</div>';
            // s +='<div class="eventdate2"> Ends: '+ eventDate2 +'</div>';
            if(location) {
                s +='<div class="location">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'+ location +'</div>';
            }
            $($div).append('<li>' + s + '</li>');
          });
          Scroll();
        },
        error: function(xhr, status) {
          $($div).append('<p>' + status +' : '+ defaults.errorMsg +'</p>');
        }
      });

  function date2str(x, y) {
      var z = {
          M: x.getMonth() + 1,
          d: x.getDate(),
          h: x.getHours(),
          m: x.getMinutes(),
          s: x.getSeconds()
      };
      y = y.replace(/(M+|d+|h+|m+|s+)/g, function(v) {
          return ((v.length > 1 ? "0" : "") + eval('z.' + v.slice(-1))).slice(-2)
      });
  
      return y.replace(/(y+)/g, function(v) {
          return x.getFullYear().toString().slice(-v.length)
      });
  }
  
  function formatDate(strDate, strFormat) {
    var fd, arrDate, am, time;
    var calendar = {
      months: {
        full: ['', 'January', 'February', 'March', 'April', 'May',
          'June', 'July', 'August', 'September', 'October',
          'November', 'December'
        ],
        short: ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
          'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
      },
      days: {
        full: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
          'Friday', 'Saturday', 'Sunday'
        ],
        short: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat',
          'Sun'
        ]
      }
    };
  
    if (strDate.length > 10) {
      arrDate = /(\d+)\-(\d+)\-(\d+)T(\d+)\:(\d+)/.exec(strDate);

      am = (arrDate[4] < 12);
      time = am ? (parseInt(arrDate[4]) + ':' + arrDate[5] + ' AM') : (
        arrDate[4] - 12 + ':' + arrDate[5] + ' PM');

      if (time.indexOf('0') === 0) {
        if (time.indexOf(':00') === 1) {
          if (time.indexOf('AM') === 5) {
            time = 'MIDNIGHT';
          } else {
            time = 'NOON';
          }
        } else {
          time = time.replace('0:', '12:');
        }
      }  
    } else {
      arrDate = /(\d+)\-(\d+)\-(\d+)/.exec(strDate);
      time = 'Time not present in feed.';
    }
  
    var year = parseInt(arrDate[1]);
    var month = parseInt(arrDate[2]);
    var dayNum = parseInt(arrDate[3]);

    var d = new Date(year, month - 1, dayNum);

    switch (strFormat) {
      case 'ShortTime':
        fd = time;
        break;
      case 'ShortDate':
        fd = month + '/' + dayNum + '/' + year;
        break;
      case 'LongDate':
        fd = calendar.months.full[
          month] + ' ' + dayNum + ', ' + year + '&nbsp&nbsp' + calendar.days.short[d.getDay()];
        break;
      case 'LongDate+ShortTime':
        fd = calendar.days.full[d.getDay()] + ' ' + calendar.months.full[
          month] + ' ' + dayNum + ', ' + year + ' ' + time;
        break;
      case 'ShortDate+ShortTime':
        fd = month + '/' + dayNum + '/' + year + ' ' + time;
        break;
      case 'DayMonth':
        fd = calendar.days.short[d.getDay()] + ', ' + calendar.months.full[
          month] + ' ' + dayNum;
        break;
      case 'MonthDay':
        fd = calendar.months.full[month] + ' ' + dayNum;
        break;
      case 'YearMonth':
        fd = calendar.months.full[month] + ' ' + year;
        break;
      default:
        fd = calendar.days.full[d.getDay()] + ' ' + calendar.months.short[
          month] + ' ' + dayNum + ', ' + year + ' ' + time;
    }

  return fd;
    }
  };

  function Scroll() {
    var lis = document.getElementById("calendarList").getElementsByTagName("li");

    var j=0;
    var i = 0;
    $('#calendarList > li').each(function() {
      scrollanItem($(lis[j]));
      j += 1;
      i += $('#calendarList > li').height();
      $(lis[j]).css("top", i);
    });

    function scrollanItem($elem) {
      var top = parseInt($elem.css("top"));
      var temp = -1 * $('#calendarList > li').height();
      if (top <= temp) {
          top = $('#calendarList').height()
          $elem.css("top", top);
      }
      $elem.animate({
          top: (parseInt(top) - $('#calendarList > li').height())
      }, 2000, function() {
        scrollanItem($(this))
      });
    }
  }
  
}(jQuery));