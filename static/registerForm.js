// Wait for the DOM to be ready
$(function() {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("#registration").validate({
      // Specify validation rules
      rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        FirstName: {
            required: true,
            maxlength: 30
        },
        LastName: {
            required: true,
            maxlength: 30
        },
        email: {
          required: true,
          // Specify that email should be validated
          // by the built-in "email" rule
          email: true
        },
        password: {
          required: true,
          minlength: 6
        },
        confirmpassword: {
          equalTo: "#password"
        }
      },
      // Specify validation error messages
      messages: {
        FirstName: {
          required: "Please provide a first name",
          maxlength: "First name must be less than 30 characters"
        },
        LastName: {
          required: "Please provide a last name",
          maxlength: "Last name must be less than 30 characters"
        },
        password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long"
        },
        email: "Please enter a valid email address",
        confirmpassword: "Must be the same as password"
      },
      // Make sure the form is submitted to the destination defined
      // in the "action" attribute of the form when valid
      submitHandler: function(form) {
        form.submit();
      }
    });
  });