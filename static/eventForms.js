function buttonEventNew() {
	$("#divFormEventNew").css("display", "initial");
	$("#buttonEventNew").text("(>)");
	datetimes = document.getElementsByClassName("myCurrentDate")
	for(var i = 0; i < datetimes.length; i++){
		datetimes[i].value = localStorage.currentTime
	}
}

function buttonProgramNew() {
	$("#divFormProgramNew").css("display", "initial");
	$("#buttonEventNew").text("(>)");
}

function buttonProgramDel() {
	$("#divFormProgramDel").css("display", "initial");
	$("#buttonEventDel").text("(>)");
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
function cancelNewProgramForm() {
	$("#divFormProgramNewNew").css("display", "none");
	$("#buttonProgramNew").text("(<)");
}


$("#formEventNew").submit(function() {
	if (validateNewFormInputs()) {
		//addFormEvent();
		alert("HELLO");
	} else {
		alert("Invalid Event Input!");
	}
});

function populateProgramDropdown(){
	//populate the program dropdown for add event
	var parsedProgams = JSON.parse(localStorage.getItem("allPrograms"));
	var length = $('#programList').children('option').length;
	if (length == 0 && parsedProgams != null){
		for(var i in parsedProgams){
			var option = parsedProgams[i];

			$('#programList').append($('<option/>').attr("value", option.ProgramID).text(option.Title));
		}
	}
}

function populateProgramDelDropdown() {
	var parsedProgams = JSON.parse(localStorage.getItem("allPrograms"));
	var length = $('#delProgramList').children('option').length;
	if (length == 0 && parsedProgams != null){
		for(var i in parsedProgams){
			var option = parsedProgams[i];
			$('#delProgramList').append($('<option/>').attr("value", option.ProgramID).text(option.Title));
		}
	}
}

setTimeout(populateProgramDropdown,1000);
setTimeout(populateProgramDelDropdown,1000);

function dateTimetoMoment(day, month, year, hour, minute, ampm) {
	//2017-12-25T15:00:00
	return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":00"
}

/*
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
*/
