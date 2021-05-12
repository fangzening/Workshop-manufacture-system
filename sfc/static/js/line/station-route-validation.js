var available_stations = new Array();
var next_station = new Array();
var start_station = new Array();
var station_list = document.getElementById('station');
var next_station_list = document.getElementById('next_station');
var default_station = new Array();

class Station{

    constructor(id, name){
        this.id = id;
        this.name = name;
    }

}

window.onload = loadStations();

function loadStations(){
    
    for(let i = 0; i < station_list.length; i++){
        let option = station_list[i];
        
        if (option.textContent != 'Select station...'){
            let temp = new Station(option.value,option.textContent)
            available_stations.push(temp);
        } else if(option.textContent === 'Select station...') {
            
            default_station.push(new Station("",option.textContent));
        }
    }
}

function changeStation(event){

    let dropDown = event.target;
    let station = dropDown.options[dropDown.selectedIndex];
    
    if(dropDown.name === 'station'){

        if(start_station.length > 0){
            available_stations.push(start_station.splice(0, 1)[0]);
        }
        
        for( var i = 0; i < available_stations.length; i++){ 
            if ( available_stations[i].name === station.textContent) {
                start_station.push(available_stations.splice(i, 1)[0]); 
                }
            }
        
        updateStationLists();
    } else if(dropDown.name === 'next_station'){

        if(next_station.length > 0){
            available_stations.push(next_station.splice(0, 1)[0]);
        }

        for( var i = 0; i < available_stations.length; i++){ 
            if ( available_stations[i].name === station.textContent) {
                next_station.push(available_stations.splice(i, 1)[0]); 
                }
            }
        updateStationLists();
    }
}

// flush and update select elements
function updateStationLists(){

    
    // empty lists
    while (station_list.firstChild) {
        station_list.removeChild(station_list.firstChild);
    }

    while (next_station_list.firstChild) {
        next_station_list.removeChild(next_station_list.firstChild);
    }
    // add default 
    var defaultNode = default_station[0];
    

    let nodeNext = document.createElement('option');
    nodeNext.textContent = defaultNode.name;
    nodeNext.value = defaultNode.id;

    let nodeStart = document.createElement('option');
    nodeStart.textContent = defaultNode.name;
    nodeStart.value = defaultNode.id;

    station_list.appendChild(nodeStart);
    next_station_list.appendChild(nodeNext);

    

    // add selected to start stations

    if(start_station.length > 0){

        let node = document.createElement('option');
        node.textContent = start_station[0].name;
        node.value = start_station[0].id;
    
        node.selected = true;
        station_list.appendChild(node);
    }

   


    if(next_station.length > 0){
        let node = document.createElement('option');
        node.textContent = next_station[0].name;
        node.value = next_station[0].id;

        node.selected = true;
        next_station_list.appendChild(node);
    }
    
    // add selected to next stations 
    
    for(let i = 0; i < available_stations.length; i++){

        let tempNode1 = document.createElement('option');
        let tempNode2 = document.createElement('option');



        tempNode1.text = available_stations[i].name;
        tempNode1.value = available_stations[i].id;

        tempNode2.text = available_stations[i].name;
        tempNode2.value = available_stations[i].id;
        
        station_list.appendChild(tempNode1);
        

        next_station_list.appendChild(tempNode2);
    }
    
    
}

function cancelButton(url) {
    window.location.replace(url);
}


function changeState(event){
    let newState = event.target.options[event.target.selectedIndex].value;
    let stationrouteID = event.target.id;

    let saveButton = document.getElementById('currentState'+ stationrouteID);

    saveButton.value = newState;
    
}

