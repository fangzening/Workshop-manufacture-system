window.onload = populateSerialNumbers;
function populateSerialNumbers(){

    
    console.log(serial_numbers);
    if(serial_numbers != null){
        let counter = 1;
        
        serial_numbers.forEach(element => {
            if(counter <=18){
                let barcode_id = "barcode" + counter
                JsBarcode("#" + barcode_id, element);
                
                let barcode_entry = document.getElementById(barcode_id);
                
                barcode_entry.style = "max-height:88px; padding: 0; margin:0;";


                counter++;
            }
        });
    }
    print();
}