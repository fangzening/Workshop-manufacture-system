function addRow(tableID) {

			var table = document.getElementById(tableID);

			var rowCount = table.rows.length;
			var row = table.insertRow(rowCount);

			var colCount = table.rows[0].cells.length;

			for(var i=0; i<colCount; i++) {
			    var text1 = '<form method="POST" action="{% url \'maskconfig:create-mask-row\' %}">{% csrf_token %}';
				var text2 = '</form>';

				var newcell	= row.insertCell(i);

				document.createElement("FORM");
			    document.getElementsByTagName("form")[0].setAttribute("action", "{% url \'maskconfig:create-mask-row\' %}");


				newcell.innerHTML =
				table.rows[0].cells[i].innerHTML;
				//alert(newcell.childNodes);
				switch(newcell.childNodes[0].type) {
					case "text":
							newcell.childNodes[0].value = "";
							newcell.classList.add("col-xs-3");
							break;
					case "checkbox":
							newcell.childNodes[0].checked = false;
							newcell.classList.add("add-row");
							break;

				    case "hidden":
							newcell.childNodes[0].checked = false;
							newcell.classList.add("add-row");
							break;
			 		case "submit":
							newcell.childNodes[0].checked = false;
							newcell.classList.add("add-row");
							break;
					case "select-one":
							newcell.childNodes[0].selectedIndex = 0;
							newcell.classList.add("add-row");
							break;
				}




			}
		}

function deleteRow(tableID) {
	try {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;

	for(var i=0; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked) {
			if(rowCount <= 1) {

				alert("Cannot delete all the rows.");

				break;
			}
			table.deleteRow(i);
			rowCount--;
			i--;
		}


	}
	}catch(e) {
		alert(e);
	}
}
