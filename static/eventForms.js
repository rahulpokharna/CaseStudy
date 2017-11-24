function buttonEventNew() {
	$("#divFormEventNew").css("display", "initial");
	$("#buttonEventNew").text("(>)");
	datetimes = document.getElementsByClassName("myCurrentDate")
	for(var i = 0; i < datetimes.length; i++){
		datetimes[i].value = localStorage.currentTime
	}
}

function submitNewEventForm() {
	$("#divFormEventNew").css("display", "none");
	$("#buttonEventNew").text("(<)");
	validateFormInputs("formEventNew");
}

function cancelNewEventForm() {
	$("#divFormEventNew").css("display", "none");
	$("#buttonEventNew").text("(<)");
}

function deleteEvent() {
    var eventID = $("#eventToDelete")[0].value
	console.log(eventID)
	$.ajax({
        type: 'GET',
        url: "request/events",
        data: {eventID: eventID, delete: true},
        async: false});
    $('#calendar').fullCalendar( 'refetchEvents' );
}

$("#formEventNew").submit(function() {
	if (validateNewFormInputs()) {
		//addFormEvent();
		alert("HELLO");
	} else {
		alert("Invalid Event Input!");
	}
});

function dateTimetoMoment(day, month, year, hour, minute, ampm) {
	//2017-12-25T15:00:00
	return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":00"
}

$(function() {
	$("form[name='newEventForm']").validate({
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

