

function updateBitrate() {
    $.ajax({
        url: "/get_bitrate",  // Update this URL with the endpoint of your Flask backend
        method: "GET",
        dataType: "json",
        success: function(data) {   
            // Update the bitrate in the HTML element
            $("#bitrate1").html(data.bitrate1 + " Mbps");
            $("#bitrate2").html(data.bitrate2 + " Mbps");
            $("#bitrate3").html(data.bitrate3 + " Mbps");
            $("#bitrate4").html(data.bitrate4 + " Mbps");
            $("#bitrate5").html(data.bitrate5 + " Mbps");

            console.log(bitrate1,bitrate2,bitrate3,bitrate4,bitrate5)
        },
        error: function(xhr, status, error) {
            console.error("Error fetching bitrate: " + error);
        }
      
        });
}
function re_updateBitrate() {
    updateBitrate();
    setInterval(updateBitrate, 5000);
};

function update_users() {
  $.ajax({
      url: "/get_users",  // Update this URL with the endpoint of your Flask backend
      method: "GET",
      dataType: "json",
      success: function(data) {
          // Update the users in the HTML element
          $("#bsusers1").html(data.bsusers1);
          $("#bsusers2").html(data.bsusers2);
          $("#bsusers3").html(data.bsusers3);
          $("#bsusers4").html(data.bsusers4);
          $("#bsusers5").html(data.bsusers5);
          console.log(bsusers1,bsusers2,bsusers3,bsusers4,bsusers5)
      },
      error: function(xhr, status, error) {
          console.error("Error fetching users: " + error);
      }
    
      });
}

function re_update_users() {
  update_users();
  var number = (3 + Math.floor(Math.random() * 6))*1000;
  setInterval(update_users, number);
};


function update_status_color() {
  var status = $(".tablestatus1").text().trim();
  if (status == "UP") {
      $(".tablestatus1").css("color","#00D23B")
  }
  if (status == "DOWN"){
      $(".tablestatus1").css("color","#FF0000")
  }
  var status = $(".tablestatus2").text().trim();
  if (status == "UP") {
      $(".tablestatus2").css("color","#00D23B")
  }
  if (status == "DOWN"){
      $(".tablestatus2").css("color","#FF0000")
  }
  var status = $(".tablestatus3").text().trim();
  if (status == "UP") {
      $(".tablestatus3").css("color","#00D23B")
  }
  if (status == "DOWN"){
      $(".tablestatus3").css("color","#FF0000")
  }
  var status = $(".tablestatus4").text().trim();
  if (status == "UP") {
      $(".tablestatus4").css("color","#00D23B")
  }
  if (status == "DOWN"){
      $(".tablestatus4").css("color","#FF0000")
  }
  var status = $(".tablestatus5").text().trim();
  if (status == "UP") {
      $(".tablestatus5").css("color","#00D23B")
  }
  if (status == "DOWN"){
      $(".tablestatus5").css("color","#FF0000")
  }
};

function re_update_status_color(){
    update_status_color();
    setInterval(update_status_color, 5000);
}





function change_power(switchId){
  
  $.ajax({
    url: "/power/" + switchId,  // Update this URL with the endpoint of your Flask backend
    method: "GET",
    dataType: "json",
    success: function(data) {
        // Update the bitrate in the HTML element
        $("#bsstatus1").html(data.bsstatus1);
        $("#bsstatus2").html(data.bsstatus2);
        $("#bsstatus3").html(data.bsstatus3);
        $("#bsstatus4").html(data.bsstatus4);
        $("#bsstatus5").html(data.bsstatus5);
        console.log(bsstatus1,bsstatus2,bsstatus3,bsstatus4,bsstatus5)
    },
    error: function(xhr, status, error) {
        console.error("Error fetching bitrate: " + error);
    }
  
  });
}


function update_status() {
    $.ajax({
        url: "/get_status",  // Update this URL with the endpoint of your Flask backend
        method: "GET",
        dataType: "json",
        success: function(data) {
            //  update the statuses
            $("#bsstatus1").html(data.bsstatus1);
            $("#bsstatus2").html(data.bsstatus2);
            $("#bsstatus3").html(data.bsstatus3);
            $("#bsstatus4").html(data.bsstatus4);
            $("#bsstatus5").html(data.bsstatus5);

            console.log(bsstatus1,bsstatus2,bsstatus3,bsstatus4,bsstatus5)
        },
        error: function(xhr, status, error) {
            console.error("Error fetching bitrate: " + error);
        }
      
        });
}
function re_update_status() {
    update_status();
    //setInterval(update_status, 2000);
};

// Function to store the checkbox value in local storage
function store_checkbox_value(checkbox,id) {
    // Get the checkbox state
    const isChecked = checkbox.checked;
    
    // Store the checkbox state in local storage
    sessionStorage.setItem('powerButtonState'+id, isChecked);
}

// Check if the button state is stored in local storage
function page_load_checkbox(){
    const storedPowerButtonState1 = sessionStorage.getItem('powerButtonState1');
    const storedPowerButtonState2 = sessionStorage.getItem('powerButtonState2');
    const storedPowerButtonState3 = sessionStorage.getItem('powerButtonState3');
    const storedPowerButtonState4 = sessionStorage.getItem('powerButtonState4');
    const storedPowerButtonState5 = sessionStorage.getItem('powerButtonState5');
    // Set initial state based on local storage
    if (storedPowerButtonState1 === 'false') {
        document.getElementById('powerb1').checked = false;
    } else {
        document.getElementById('powerb1').checked = true;
    }
    if (storedPowerButtonState2 === 'false') {
        document.getElementById('powerb2').checked = false;
    } else {
        document.getElementById('powerb2').checked = true;
    }
    if (storedPowerButtonState3 === 'false') {
        document.getElementById('powerb3').checked = false;
    } else {
        document.getElementById('powerb3').checked = true;
    }
    if (storedPowerButtonState4 === 'false') {
        document.getElementById('powerb4').checked = false;
    } else {
        document.getElementById('powerb4').checked = true;
    }
    if (storedPowerButtonState5 === 'false') {
        document.getElementById('powerb5').checked = false;
    } else {
        document.getElementById('powerb5').checked = true;
    }
};




var karlshamnCoordinates = [56.1714, 14.8640];

// Define the boundaries including Karlshamn at the center
var southWest = L.latLng(karlshamnCoordinates[0] - 0.1, karlshamnCoordinates[1] - 0.1);
var northEast = L.latLng(karlshamnCoordinates[0] + 0.1, karlshamnCoordinates[1] + 0.1);
var bounds = L.latLngBounds(southWest, northEast);


var towerIcon = L.icon({
    iconUrl: 'https://github.com/frankuman/5imFortress/blob/main/frontend/gui/templates/img/tower2.png?raw=true', // URL to your tower icon image
    iconSize: [42, 42], // Size of the icon
    iconAnchor: [16, 32], // Point of the icon which will correspond to marker's location
    popupAnchor: [0, -32] // Point from which the popup should open relative to the iconAnchor
});

// Initialize the map centered at Karlshamn
var map = L.map('map', {
    center: karlshamnCoordinates, // Centered at Karlshamn, Sweden
    zoom: 9, // Zoom level
    maxZoom: 11, // Maximum zoom level
    minZoom: 8, // Minimum zoom level (adjust as needed)
    maxBounds: bounds // Set the maximum boundaries for the map
});


// Add CartoDB dark tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);


// Add markers for each city
var cities = [
    { name: 'Karlskrona', coordinates: [56.1616, 15.5866] },
    { name: 'Ronneby', coordinates: [56.2106, 15.2776] },
    { name: 'Olofström', coordinates: [56.2777, 14.5309] },
    { name: 'Karlshamn', coordinates: karlshamnCoordinates },
    { name: 'Sölvesborg', coordinates: [56.0500, 14.5750] }
];

// cities.forEach(function(city) {
//     L.marker(city.coordinates).addTo(map).bindPopup(city.name);
// });

cities.forEach(function(city) {
    L.marker(city.coordinates, { icon: towerIcon }).addTo(map).bindPopup(city.name);
});

   
function get_logs(){
    // Use jQuery's AJAX function to load the content of the text file
    $.ajax({
        url: '/loggers/get_log',
        method: "GET",
        dataType: 'json',
        success: function(data) {
            
            $('#log1').text(data.bslog1); //
            $('#log2').text(data.bslog2);
            $('#log3').text(data.bslog3);
            $('#log4').text(data.bslog4);
            $('#log5').text(data.bslog5);
            $('#log6').text(data.systemlog);

        },
        error: function() {
            console.log('Error loading text file.');
        }
    });
};

function re_get_log() {
    get_logs();
    setInterval(get_logs, 2000);
};



