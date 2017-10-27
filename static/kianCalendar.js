/*
calendar.js

modifier buttons: 
add event
modify event
remove event

navigation buttons:
next
prev
today

view buttons:
month
week
day
*/
$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: false,
        navLinks: true,
        editable: true
    });

    // GET DISPLAY TYPE AND CHANGE DATE ACCORDINGLY
    var moment = $('#calendar').fullCalendar('getDate');
    $('#date').html(moment.format("MMM D YYYY"));

    idnum = 1;

    var events = $.ajax({
        type: "GET",
        url: "request/events",
        data: {userID: 1},
        async: false});
    //console.log(events.responseText);
    var parsedEvents = JSON.parse(events.responseText);
    //console.log(parsedEvents);
    /*
    for (var i = 0; i < events.length; ++i) {
        for (var ind in events[i]) {
            console.log(ind);
            for (var vals in obj[i][ind]) {
                console.log(vals, obj[i][ind][vals]);
            }
        }
    }
    */
    for (parsedEvent in parsedEvents) {
    	var event = parsedEvents[parsedEvent];
    	addEvent(event['Title'], event['Start'], event['End'])
    }
});

$(".dateChange").click(function() {
    // GET DISPLAY TYPE AND CHANGE DATE ACCORDINGLY
    var moment = $('#calendar').fullCalendar('getDate');
    $('#date').html(moment.format("MMM D YYYY"));
});

function addEventButton() {
    var eventTitle = prompt("What is your new event called?", "Event Title");
    var eventStart = prompt("When does your event start?\nFormat Example: \"2017-12-25T12:00:00\"", "Year-Month-DayTHour:Minute:Second");
    var eventEnd = prompt("When does your event end?\nFormat Example: \"2017-12-25T15:00:00\"", "Year-Month-DayTHour:Minute:Second");
    addEvent(eventTitle, eventStart, eventEnd);
}

function addEvent(title, start, end) {
    var eventToAdd = {
        title: title,
        start: start,
        end: end,
        id: idnum
    };
    $('#calendar').fullCalendar('renderEvent', eventToAdd);
    console.log("Adding Event ID: " + eventToAdd);
    idnum++;
}

function removeEvent() {
    var eventToDelete = Number(prompt("Which Event ID would you like to delete?", "Event ID"));

    if (isNaN(eventToDelete) || typeof eventToDelete !== "number") {
        alert("INVALID EVENT ID!");
    } else {
        $('#calendar').fullCalendar('removeEvents', eventToDelete);
        console.log("Removing Event ID: " + idnum);
        idnum--;
    }
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}