function buttonEventNew() {
	$("#divFormEventNew").css("display", "initial");
	$("#buttonEventNew").text("(>)");
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

$("#formEventNew").submit(function() {
	if (validateNewFormInputs()) {
		//addFormEvent();
		alert("HELLO");
	} else {
		alert("Invalid Event Input!");
	}
});

function addFormEvent(formId) {
	
}

function validateNewFormInputs() {
	var title = $("#newEventTitle").val();
	alert(title);
	return true;
}

function dateTimetoMoment(day, month, year, hour, minute, ampm) {
	//2017-12-25T15:00:00
	return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":00"
}

$(function() {
	$("form[name='newEventForm']").validate({
    	rules: {
      		newEventTitle: {
      			required: true,
      			maxlength: 12
      		},
  			newStartDateTime: {
  				required: true,
  				minlength: 19,
  				maxlength: 19
  			},
  			newEndDateTime: {
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

