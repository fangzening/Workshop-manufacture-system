var part = document.getElementById('partnum');
var keyparts = document.documentElement;




function changePart(element,str){
    part.value = str;
    
    elements = element.getElementsByClassName('major');
    elementText = element.getElementsByClassName('txt');

    keypartsElements = keyparts.getElementsByClassName('major');
    keypartsElementText = keyparts.getElementsByClassName('txt');
    
    

    for(let i = 0; i < keypartsElements.length; i++){
        
                       

        keypartsElements[i].classList.add('key-part-container-action');
        keypartsElements[i].classList.remove('key-part-container-wait');
        
        
    
    }
    for(let i = 0; i < keypartsElementText.length; i++){
        
                       
        
        keypartsElementText[i].innerHTML = "Not Yet Started";
        
        
        
    
    }


    
    for(let i = 0; i < elements.length; i++){

        
        elements[i].classList.remove('key-part-container-action');
        elements[i].classList.add('key-part-container-wait');
        
        
    
    }
    for(let i = 0; i <  elementText.length; i++){
        
                       
        
        elementText[i].innerHTML = "In-Progress";
        
        
        
    
    }
    
   
    
}

