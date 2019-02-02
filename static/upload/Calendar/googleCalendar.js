(function(e){e.fn.gCalReader=function(t){
    function o(e,t){
        var n,r,i,s;
        var o={months:{full:["","January","February","March","April","May","June","July","August","September","October","November","December"],
            "short":["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]},
            days:{full:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"short":["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sun"]}};
            if(e.length>10){
                r=/(\d+)\-(\d+)\-(\d+)T(\d+)\:(\d+)/.exec(e);
                i=r[4]<12;
                s=i?parseInt(r[4])+":"+r[5]+" AM":r[4]-12+":"+r[5]+" PM";
                if(s.indexOf("0")===0) {
                    if(s.indexOf(":00")===1){
                        if(s.indexOf("AM")===5){
                            s="MIDNIGHT"}else{s="NOON"
                        }
                    }
                    else{s=s.replace("0:","12:")
                    }
                }
            }
            else{r=/(\d+)\-(\d+)\-(\d+)/.exec(e);
            s="Time not present in feed."
            }
            var u=parseInt(r[1]);
            var a=parseInt(r[2]);
            var f=parseInt(r[3]);
            var l=new Date(u,a-1,f);
            switch(t){
                case"ShortTime":n=s;
                break;
                case"ShortDate":n=a+"/"+f+"/"+u;
                break;
                case"LongDate":n=o.days.full[l.getDay()]+" "+o.months.full[a]+" "+f+", "+u;
                break;
                case"LongDate+ShortTime":n=o.days.full[l.getDay()]+" "+o.months.full[a]+" "+f+", "+u+" "+s;
                break;
                case"ShortDate+ShortTime":n=a+"/"+f+"/"+u+" "+s;
                break;
                case"DayMonth":n=o.days.short[l.getDay()]+", "+o.months.full[a]+" "+f;
                break;
                case"MonthDay":n=o.months.full[a]+" "+f;
                break;
                case"YearMonth":n=o.months.full[a]+" "+u;
                break;
                default:n=o.days.full[l.getDay()]+" "+o.months.short[a]+" "+f+", "+u+" "+s
            }return n
    }
    var n=e(this);
    var r=e.extend(
        {calendarId:"en.usa#holiday@group.v.calendar.google.com",
            apiKey:"Public_API_Key",
            dateFormat:"LongDate",
            errorMsg:"No events in calendar",
            maxEvents:50,
            sortDescending:true},
        t);
    var i="";
    var s="https://www.googleapis.com/calendar/v3/calendars/"+encodeURIComponent(r.calendarId.trim())+"/events?key="+r.apiKey+"&orderBy=startTime&singleEvents=true";
    e.ajax({url:s,dataType:"json",success:function(t){if(r.sortDescending){t.items=t.items.reverse()}t.items=t.items.slice(0,r.maxEvents);
    e.each(t.items,function(t,s){var u=s.start.dateTime||s.start.date||"";
    var a=s.summary||"";
    var f=s.description;
    var l=s.location;
    i='<div class="eventtitle">'+a+"</div>";
    i+='<div class="eventdate"> When: '+o(u,r.dateFormat.trim())+"</div>";
    if(l){
        i+='<div class="location">Where: '+l+"</div>"
    }
    if(f){
        i+='<div class="description">'+f+"</div>"
    }
    e(n).append("<li>"+i+"</li>")
    }
    )
    },error:function(t){
        e(n).append("<p>"+r.errorMsg+" | "+t+"</p>")}})}})(jQuery)