console.log("station-create.js is loaded");

document.getElementById("template").onchange = function(){

    let allActionsArray = document.getElementsByClassName("template");
    
    for(var i = 0; i < allActionsArray.length; i++){
        allActionsArray[i].classList.add("hidden");
    }

    let template = this.value;
    let element_name = "template-"+template;
    let actionsArray = document.getElementsByClassName(element_name);

    for(var i = 0; i < actionsArray.length; i++){
        actionsArray[i].classList.remove("hidden");
    }

};