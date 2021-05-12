var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

var serial_number = document.getElementById('serial_number');
var partnum = document.getElementById('partnum');
var kp_serialnumber = document.getElementById('kp_serialnumber');
var form = document.getElementById('kp_form');
// simulate button clicks



window.onload = focusInput();

function focusInput(){
    if(serial_number.value == ''){
        serial_number.focus();
    } else if(partnum != null) {
        console.log(partnum)
        partnum.focus();
    } else {
        kp_serialnumber.focus();
    }
}

function changeInputBox(event){
    var button = document.createElement("button");
    button.hidden=true;
    button.type="submit";
    
    
   if(event.key === "Enter"){
        let target = event.target.id;
        
        if(target == "serial_number"){
            if(serial_number.value != ""){
                
                form.appendChild(button);
                button.click();
            }
        } else if(target == "partnum") {
            if(partnum.value == ""){
                partnum.value = " ";
            }
            if (kp_serialnumber == null) {
                form.appendChild(button);
                button.click();
            } else {
                kp_serialnumber.focus();
            }
            
        } else if(target == "kp_serialnumber"){
            if(serial_number.value != "" && partnum == null ){
                form.appendChild(button);
                button.click();
                
            } else if(serial_number.value != "" && partnum.value != ""){
                form.appendChild(button);
                button.click();
            }
        }


   }
}

