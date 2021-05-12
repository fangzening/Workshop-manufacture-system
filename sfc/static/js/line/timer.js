const counter = document.querySelector('.counter');

var seconds;
var remseconds;
var minuts;
var toCount = true;

function countdown(){
    seconds = 10;
    counting();
}

function count(){
    
    if(seconds > 0) {
        if(toCount == true){
            seconds--;
            remseconds = seconds % 60;
            minuts = Math.floor(seconds / 60);
            if (minuts < 10){
                minuts = "0" + minuts;
            }
            if(remseconds < 10){
                remseconds = "0" + remseconds
            }
            
            counter.innerHTML = minuts + " : " + remseconds;
            
        }
    }else{
        toCount == false;
    }
}


function counting(){
   
    remseconds = seconds % 60;
    minuts = Math.floor(seconds / 60);
    if (minuts < 10){
        minuts = "0" + minuts;
    }
    if(remseconds < 10){
        remseconds = "0" + remseconds
    }
    
    counter.innerHTML = minuts + " : " + remseconds;
    setInterval(count, 1000);
}

countdown();