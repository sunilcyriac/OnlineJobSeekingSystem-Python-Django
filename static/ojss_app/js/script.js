
function applicationViewer() {

    var x = document.getElementsByClassName("application-toggler")[0];
    var button = document.getElementById("applyButton")
    if (x.style.display == "none") {

        x.style.display = "block";
        button.innerHTML = "CANCEL APPLICATION";
        button.setAttribute('class','btn btn-warning')

    }
    else if (x.style.display == "block"){

        x.style.display = "none";
        button.innerHTML = "APPLY";
        button.setAttribute('class','btn btn-info')
    }

}