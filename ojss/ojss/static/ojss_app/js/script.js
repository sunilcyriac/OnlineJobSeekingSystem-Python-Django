
// Takes care of showing and hiding the application forms
function applicationViewer() {

    var x = document.getElementsByClassName("application-toggler")[0];
    var button = document.getElementById("applyButton");

    if (x.style.display == "none") {

        x.style.display = "block";
        button.innerHTML = "CANCEL APPLICATION";
        button.setAttribute('class','btn btn-warning');

    }
    else if (x.style.display == "block"){

        x.style.display = "none";
        button.innerHTML = "APPLY";
        button.setAttribute('class','btn btn-info');
    }

}


//take care of profile reset button

function resetButton() {


     var inputItems = document.getElementsByClassName("input-control");
     var resetButton = document.getElementById("profileResetButton");
     var submitButton = document.getElementById('profileEditButton');
     var headerText = document.getElementById('profile-heading');

     headerText.innerText = "Profile";
     resetButton.style.display = 'None';
     submitButton.type = "submit";
     submitButton.innerText = "EDIT PROFILE";

    for (i = 0; i < inputItems.length ; i++) {



            inputItems[i].setAttribute("readonly","true");
            console.log("test" + 1);


    }


}







// Takes care of the profile edit features for seeker

function toggleProfileEdit() {

    var formElement = document.getElementById("profile-edit");
    var heading = document.getElementById("profile-heading");
    var submitButton = document.getElementById("profileEditButton");
    var resetButton = document.getElementById("profileResetButton");
    var dateButton = document.getElementsByClassName('date-picking')[0];

    if (submitButton.type == "button") {

        submitButton.type = "submit";
        submitButton.innerText = "Edit Profile";
        resetButton.style.display = "none";
        heading.innerText = "PROFILE";




    }
    else {

        submitButton.type = "button";
        submitButton.innerText = "Save Profile";
        resetButton.style.display = "inline";
        heading.innerText = "EDIT PROFILE";


    }


    var inputItems = document.getElementsByClassName("input-control");
    for (i = 0; i < inputItems.length ; i++) {

        if (inputItems[i].hasAttribute("readonly"))

            inputItems[i].removeAttribute("readonly");

        else {

            inputItems[i].setAttribute("readonly");
        }

    }


    var optionItem = document.getElementsByClassName("option-values");
    for (i=0; i < optionItem.length; i++) {

        if (optionItem[i].hasAttribute('disabled')) {

            optionItem[i].removeAttribute("disabled");
            console.log("check here disabled removed");
        }
        else {
            optionItem[i].setAttribute("disabled");
            console.log("disabled enabled");
        }

    }

}


function removeVal(){

    var textArea = document.getElementById('datepicker');
    textArea.setAttribute("value","");
}


//takes care of the reset/cancel button in skill form

function resetSkill() {

    var resetButton = document.getElementById("skill-reset");
    var submitButton = document.getElementById("skill-submit");
    var inputFields = document.getElementsByClassName("skill-input-control");
    var heading = document.getElementById("skill-heading");

    resetButton.style.display = "None";
    submitButton.innerText = "EDIT SKILlS";
    submitButton.type = "submit";
    heading.innerText = "SKILLS";

    for( i=0; i < inputFields.length; i++) {

        inputFields[i].setAttribute("readonly");

    }

}



//takes care of the edit/submit button in the skill page



function toggleSkillEdit() {

    var resetButton = document.getElementById("skill-reset");
    var submitButton = document.getElementById("skill-submit");
    var inputFields = document.getElementsByClassName("skill-input-control");
    var heading = document.getElementById("skill-heading");

    if (submitButton.type == "button") {

        submitButton.type = "submit";
        submitButton.innerText = "EDIT SKILLS";
        resetButton.style.display = "none";
        heading.innerText = "SKILLS";



    }
    else {

        submitButton.type = "button";
        submitButton.innerText = "SAVE SKILLS";
        resetButton.style.display = "inline";
        heading.innerText = "EDIT SKILLS";


    }



    for (i = 0; i < inputFields.length ; i++) {

        if (inputFields[i].hasAttribute("readonly")) {

            inputFields[i].removeAttribute("readonly");
            console.log("remove readonly");

        }

        else {

            inputFields[i].setAttribute("readonly");
            console.log("add read only")
        }

    }


}



function showInterviewForm() {

    var interviewButton = document.getElementById('interview-button');
    var interviewForm = document.getElementById('interview-form');

    if (interviewForm.style.display == 'none') {

        interviewForm.style.display = 'block';
        interviewButton.innerText = "CANCEL INTERVIEW FORM";

    }

    else {

        interviewForm.style.display = 'none'
        interviewButton.innerText = "SEND INTERVIEW CALL";
    }

}

