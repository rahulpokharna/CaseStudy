function validateLogin() {
    var email = document.forms["myForm"]["email"].value;
    var password = document.forms["myForm"]["password"].value;
    if(!validateEmail(email)){
        alert("Please enter a valid email");
        console.log('fuck')
        return false;
    }else if(!validatePassword(password)){
        alert("Please enter a valid password")
        console.log('fuck')
        return false;
    }
    return true;

}

function validateEmail(mail) {
     if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(myForm.emailAddr.value))
      {
        return (true)
      }

        return (false)
}

function validatePassword(password){
    if (password.length > 0) {
        return true;
    }else{
        return false;
    }
}