/*
Original Author: Yue ma
Creation date: Jan 26th, 2019
Contents of file:
	1. read news.json file every certain interval
	2. update the content of the news DIV every certain interval
*/
var newsString = '';
var newsCounter = 0;
var NewsTitle = 'CBC';
var timerShort = 4000;
var timerLong = 1800000;
$.getJSON( "../static/upload/newsfeed/news.json", function( data ) {
    newsString = data;

});
//every timerShort second, update and show next news
setInterval(myTimer, timerShort);
//every timerLong second, fetch news.json file to get the newest news
setInterval(newsUpdateTime, timerLong);
function myTimer() {

    if(newsCounter<newsString.length-1){
        newsCounter += 1;
    }
    else{
        newsCounter = 0;
    }
    var currentNews = newsString[newsCounter];
    if(typeof(currentNews)!=='undefined' && currentNews.indexOf(NewsTitle)<0 ){
        document.getElementById("newsTitle").innerHTML = newsString[newsCounter];

    }
}

function newsUpdateTime() {

    $.getJSON( "../static/upload/newsfeed/news.json", function( data ) {
        newsString = data;

    });

}