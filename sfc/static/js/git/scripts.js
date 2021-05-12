
var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

function updateGit(e){
    var modal = document.getElementById("myModal");
    var message = document.getElementById("message");
    // collect data
    let po = e.currentTarget.id;
    let eta = document.getElementById((po+'_eta')).value;
    let etd = document.getElementById((po+'_etd')).value;
    let tracking_no = document.getElementById((po+'_tracking_no')).value;
    let tracking_company = document.getElementById((po+'_tracking_company')).value;


    let url = e.currentTarget.attributes['data-url'].value

    let data = {
        'po' : po,
        'eta' : eta,
        'etd' : etd,
        'tracking_no' : tracking_no,
        'tracking_company' : tracking_company,
    }
    
    var dateValid = dateIsValid(etd,eta)

    let payload = JSON.stringify(data);

    if (dateValid){
        var xhttp = new XMLHttpRequest();

 
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                let resp = JSON.parse(this.responseText)
                message.innerHTML=resp.message;
                modal.style.display = "block" 
            }
          };
    
        xhttp.open("POST", url, true);
        xhttp.setRequestHeader("Content-type","application/json");
        xhttp.setRequestHeader("X-CSRFToken", csrf);
        xhttp.send(payload);
    }else {

        message.innerHTML="ETA must be greater than ETD";
        modal.style.display = "block" 
        // alert("ETD must be greater than ETA");
    }


}

function dateIsValid(etd,eta) {
    return etd<eta;
}
