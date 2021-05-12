/*

This program collects table data and converts all of the changes
into json. Then submits a post request to my back end via
and endpoint including the csrf token


*/

var table = document.getElementById('table');
var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

// array of segments
let segments = new Array();
// table row
class Segment {
    constructor(id,position, name, datatype, length){
        this.id = id;
        this.position = position;
        this.name = name;
        this.datatype = datatype;
        this.length = length;
    }
}

function updateChanges() {
    
    // iterates through the table
    for(let i = 1, row; row = table.rows[i]; i++ ){
        
        let temp = new Array();
        temp.push(row.id);

        for( let j=1; j < row.cells.length-1; j++){
            col = row.cells[j];
            temp.push(col.textContent);
        }
        
        let seg = new Segment(temp[0],temp[1],temp[2],temp[3],temp[4]);
        let json = JSON.stringify(seg);
        segments.push(json);
    }
    console.log(segments);
    sendJSON()
}
function sendJSON() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        console.log(this.responseText);
        window.location.href= xhttp.responseURL;
      }
    };
    // http://127.0.0.1:8000
    xhttp.open("POST", "/config/segments/", true);
    xhttp.setRequestHeader("X-CSRFToken", csrf);
    xhttp.send(segments);
    
  }

