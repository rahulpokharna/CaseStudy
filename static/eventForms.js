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
		if (validateFormInputs("#formEventNew")) {
			addFormEvent();
			alert("HELLO");
		} else {
			alert("Invalid Event Input!");
		}
	});

	function addFormEvent(formId) {
		
	}

	function validateFormInputs(formId) {
		
	}