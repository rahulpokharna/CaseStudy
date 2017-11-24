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
idnum = 1;
$(document).ready(function() {
    $('#calendar').fullCalendar({
        viewRender: function(view, element) {
            $('#calendar').fullCalendar('removeEvents');
            renderEvents();

            var moment = $('#calendar').fullCalendar('getDate');
            $('#date').html(moment.format("MMM D YYYY"));
        },
        eventClick: function(event, element) {
            alert(event.title)
            showEventEdit();
            $("#editEventForm input.editTitle").val(event.title);
            $('#calendar').fullCalendar('updateEvent', event);
        },
        header: false,
        navLinks: true,
        editable: true
    });

    //store the current time for default form values
    var now = new Date();
    localStorage.currentTime = [[now.getFullYear(), AddZero(now.getMonth()+1), AddZero(now.getDate())].join("-"),[AddZero(now.getHours()),
        AddZero(now.getMinutes())].join(":")].join("T");


    // GET DISPLAY TYPE AND CHANGE DATE ACCORDINGLY

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
});

//Pad given value to the left with "0"
function AddZero(num) {
    return (num >= 0 && num < 10) ? "0" + num : num + "";
}

function buttonEventAdd() {
    $("#inputForm").css("display", "initial");
}

function closeInputForm() {
    $("#inputForm").css("display", "none");
}

function renderEvents() {
    setUserId()
    var events = $.ajax({
        type: "GET",
        url: "request/events",
        data: {userID: localStorage.userId},
        async: false});

    var parsedEvents = JSON.parse(events.responseText);

    for (parsedEvent in parsedEvents) {
        var event = parsedEvents[parsedEvent];
        var parsedEvent = makeEvent(event['Title'], event['Start'], event['End'], event['EventID']);
        $('#calendar').fullCalendar('renderEvent', parsedEvent);
    }
}

function makeEvent(title, start, end, id) {
    var event = {
        title: title,
        start: start,
        end: end,
        id: id
    };
    return event;
}

$(".dateChange").click(function() {
    // GET DISPLAY TYPE AND CHANGE DATE ACCORDINGLY
    var moment = $('#calendar').fullCalendar('getDate');
    $('#date').html(moment.format("MMM D YYYY"));
});

function addEventButton() {
    var eventTitle = prompt("What is your new event called?", "Event Title");
    var eventStart = prompt("When does your event start?\nFormat Example: \"2017-12-25T12:00:00\"", "Year-Month-DayTHour:Minute:Second");
    var eventEnd = prompt("When does your event end?\nFormat Example: \"2017-12-25T15:00:00\"", "Year-Month-DayTHour:Minute:Second");
    addAnEvent(eventTitle, eventStart, eventEnd);
}

function addAnEvent(title, start, end) {
    var eventID = $.ajax({
        type: 'POST',
        url: "request/events",
        data: {title: title, start: start, end: end},
        async: false}
    );
    var event = makeEvent(title, start, end, eventID);
    $('#calendar').fullCalendar('renderEvent', event);
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
    console.log(idnum);
}

function editEvent(id, title, start, end) {
    var eventID = $.ajax({
        type: 'POST',
        url: "request/events",
        data: {title: title, start: start, end: end, id: id},
        async: false
    });
    var event = makeEvent(title, start, end, id);
    $('#calendar').fullCalendar('renderEvent', event);
}

function notifyEvent() {
    var id = Number(prompt("What event would you like to send a notification for?", "Event ID"));
    alert("Event " + id + " has started.");
    window.location = "/study?eventID=" + id;
}

function deleteEvent() {
    var eventToDelete = Number(prompt("Which Event ID would you like to delete?", "Event ID"));
    console.log(eventToDelete);
    $.ajax({
        type: 'GET',
        url: "request/events",
        data: {eventID: eventToDelete, delete: true},
        async: false});
    $('#calendar').fullCalendar( 'refetchEvents' );
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

function showEventEdit() {
    $("#divFormEventEdit").css("display", "initial");
}

function hideEventEdit() {
    $("#divFormEventEdit").css("display", "none");
}

$(function() {
    $("form[name='editEventForm']").validate({
        rules: {
            title: {
                required: true,
                maxlength: 12
            },
            start: {
                required: true,
                minlength: 19,
                maxlength: 19
            },
            end: {
                required: true,
                minlength: 19,
                maxlength: 19
            }
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});

