var selector = document.getElementById('id_data_type');
var length = document.getElementById('id_length');
var value = document.getElementById('id_value');



function validate() {
    
    select_type = selector.value;

    if (select_type == 'Hard Code'){
        length.disabled = true;
        value.disabled = false;
    } else {
        value.disabled = true;
        length.disabled = false;
    }
}



document.addEventListener("DOMContentLoaded", validate());
