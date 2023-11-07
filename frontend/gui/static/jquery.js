// "Controllers" Tower Functions
// Changing, storing and updating information
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
            sessionStorage.setItem('bitrate1', data.bitrate1 + " Mbps" );
            sessionStorage.setItem('bitrate2', data.bitrate2  + " Mbps");
            sessionStorage.setItem('bitrate3', data.bitrate3 + " Mbps" );
            sessionStorage.setItem('bitrate4', data.bitrate4 + " Mbps" );
            sessionStorage.setItem('bitrate5', data.bitrate5 + " Mbps" );
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
function page_load_bitrate(){
    const storedbitrate1 = sessionStorage.getItem('bitrate1');
    const storedbitrate2 = sessionStorage.getItem('bitrate2');
    const storedbitrate3 = sessionStorage.getItem('bitrate3');
    const storedbitrate4 = sessionStorage.getItem('bitrate4');
    const storedbitrate5 = sessionStorage.getItem('bitrate5');
        
    bitratevalue1 = storedbitrate1
    if(bitratevalue1 == null){
        bitratevalue1 = "Unknown"
    }
    bitratevalue2 = storedbitrate2
    if(bitratevalue2 == null){
        bitratevalue2 = "Unknown"
    }
    bitratevalue3 = storedbitrate3
    if(bitratevalue3 == null){
        bitratevalue3 = "Unknown"
    }
    bitratevalue4 = storedbitrate4
    if(bitratevalue4 == null){
        bitratevalue4 = "Unknown"
    }
    bitratevalue5 = storedbitrate5
    if(bitratevalue5 == null){
        bitratevalue5 = "Unknown"
    }
    document.getElementById("bitrate1").innerHTML = bitratevalue1 //displays this value to the html page
    document.getElementById("bitrate2").innerHTML = bitratevalue2 //displays this value to the html page
    document.getElementById("bitrate3").innerHTML = bitratevalue3 //displays this value to the html page
    document.getElementById("bitrate4").innerHTML = bitratevalue4 //displays this value to the html page
    document.getElementById("bitrate5").innerHTML = bitratevalue5 //displays this value to the html page
};

function send_current_gain() {
    const storedGainValue1 = sessionStorage.getItem('GainValue1');
    const storedGainValue2 = sessionStorage.getItem('GainValue2');
    const storedGainValue3 = sessionStorage.getItem('GainValue3');
    const storedGainValue4 = sessionStorage.getItem('GainValue4');
    const storedGainValue5 = sessionStorage.getItem('GainValue5');
    
    gainvalue1 = storedGainValue1
    if(gainvalue1 == null){
        gainvalue1 = 0
    }
    gainvalue2 = storedGainValue2
    if(gainvalue2 == null){
        gainvalue2 = 0
    }
    gainvalue3 = storedGainValue3
    if(gainvalue3 == null){
        gainvalue3 = 0
    }
    gainvalue4 = storedGainValue4
    if(gainvalue4 == null){
        gainvalue4 = 0
    }
    gainvalue5 = storedGainValue5
    if(gainvalue5 == null){
        gainvalue5 = 0
    }
    $.ajax({
            url: "/change_gain/" +  gainvalue1 + "/" + gainvalue2 + "/" + gainvalue3 + "/" + gainvalue4 + "/" + gainvalue5,
            method: "POST",
            dataType: "json",
            success: function(data) {
                // Handle success if needed
            },
            error: function(xhr, status, error) {
                console.error("Error sending gain: " + error);
            }
    });
    // for (let bs_id = 1; bs_id <= 5; bs_id++) {
    //     const storedGainValue = sessionStorage.getItem('GainValue' + bs_id);
    //     if (storedGainValue) {
    //         $.ajax({
    //             url: "/change_gain/" + bs_id + "/" + storedGainValue,
    //             method: "POST",
    //             dataType: "json",
    //             success: function(data) {
    //                 // Handle success if needed
    //             },
    //             error: function(xhr, status, error) {
    //                 console.error("Error sending gain: " + error);
    //             }
    //         });
    //     }
    // }
}
function re_send_current_gain() {
    send_current_gain();
    setInterval(send_current_gain, 3000);
};

// function update(){
//     send_current_gain();
//     updateBitrate();
//     update_status();
// }
// function re_update(){
//     setInterval(update, 1000);
// }
function send_current_gain_t(callback) {
    // Simulated asynchronous operation
    setTimeout(function() {
        send_current_gain();
        callback();
    }, 1000);
}

function updateBitrate_t(callback) {
    // Simulated asynchronous operation
    setTimeout(function() {
        updateBitrate();
        callback();
    }, 1000);
}

function update_status_t() {
    // Your update_status function
    update_status();
}

function update() {
    send_current_gain_t(function() {
        updateBitrate_t(function() {
            update_status_t();
        });
    });
}

function re_update() {
    setInterval(update, 1000);
}

function ChangeGain(id) {
    GainElement = "Gain"+id
    RangeElement = "GainValue"+id
    var val = document.getElementById(GainElement).value //gets the oninput value
    document.getElementById(RangeElement).innerHTML = val+"% GAIN" //displays this value to the html page
    console.log(val)

    // Store the checkbox state in local storage
    sessionStorage.setItem('GainValue'+id, val);
}
function page_load_gainvalue(){
    const storedGainValue1 = sessionStorage.getItem('GainValue1');
    gainvalue1 = storedGainValue1
    if(gainvalue1 == null){
        gainvalue1 = 0
    }
    document.getElementById("GainValue1").innerHTML = gainvalue1+"% GAIN" //displays this value to the html page
    document.getElementById("Gain1").value = gainvalue1 //displays this value to the html page

    const storedGainValue2 = sessionStorage.getItem('GainValue2');
    gainvalue2 = storedGainValue2
    if(gainvalue2 == null){
        gainvalue2 = 0
    }
    document.getElementById("GainValue2").innerHTML = gainvalue2+"% GAIN" //displays this value to the html page
    document.getElementById("Gain2").value = gainvalue2 //displays this value to the html page

    const storedGainValue3 = sessionStorage.getItem('GainValue3');
    gainvalue3 = storedGainValue3
    if(gainvalue3 == null){
        gainvalue3 = 0
    }
    document.getElementById("GainValue3").innerHTML = gainvalue3+"% GAIN" //displays this value to the html page
    document.getElementById("Gain3").value = gainvalue3 //displays this value to the html page

    const storedGainValue4 = sessionStorage.getItem('GainValue4');
    gainvalue4 = storedGainValue4
    if(gainvalue4 == null){
        gainvalue4 = 0
    }
    document.getElementById("GainValue4").innerHTML = gainvalue4+"% GAIN" //displays this value to the html page
    document.getElementById("Gain4").value = gainvalue4 //displays this value to the html page

    const storedGainValue5 = sessionStorage.getItem('GainValue5');
    gainvalue5 = storedGainValue5
    if(gainvalue5 == null){
        gainvalue5 = 0
    }
    document.getElementById("GainValue5").innerHTML = gainvalue5+"% GAIN" //displays this value to the html page
    document.getElementById("Gain5").value = gainvalue5 //displays this value to the html page

    // Set initial state based on local storage

};
function ShowSettings(id){
    // show information and settings for the selected 'id' in bottom of controllers
    if (id == 1) {
        document.getElementById("GainValue1").hidden = false;
        document.getElementById("GainValue2").hidden = true;
        document.getElementById("GainValue3").hidden = true;
        document.getElementById("GainValue4").hidden = true;
        document.getElementById("GainValue5").hidden = true;
        document.getElementById("Gain1").hidden = false;
        document.getElementById("Gain2").hidden = true;
        document.getElementById("Gain3").hidden = true;
        document.getElementById("Gain4").hidden = true;
        document.getElementById("Gain5").hidden = true;

        document.getElementById("TowerSelect1").hidden = false;
        document.getElementById("TowerSelect2").hidden = true;
        document.getElementById("TowerSelect3").hidden = true;
        document.getElementById("TowerSelect4").hidden = true;
        document.getElementById("TowerSelect5").hidden = true;

        document.getElementById("a1-1").hidden = false;
        document.getElementById("a1-2").hidden = false;
        document.getElementById("a1-3").hidden = false;
        document.getElementById("a1-4").hidden = false;
        
        document.getElementById("a2-1").hidden = true;
        document.getElementById("a2-2").hidden = true;
        document.getElementById("a2-3").hidden = true;
        document.getElementById("a2-4").hidden = true;

        document.getElementById("a3-1").hidden = true;
        document.getElementById("a3-2").hidden = true;
        document.getElementById("a3-3").hidden = true;
        document.getElementById("a3-4").hidden = true;

        document.getElementById("a4-1").hidden = true;
        document.getElementById("a4-2").hidden = true;
        document.getElementById("a4-3").hidden = true;
        document.getElementById("a4-4").hidden = true;
        
        document.getElementById("a5-1").hidden = true;
        document.getElementById("a5-2").hidden = true;
        document.getElementById("a5-3").hidden = true;
        document.getElementById("a5-4").hidden = true;
    }
    
    if (id == 2) {
        document.getElementById("GainValue1").hidden = true;
        document.getElementById("GainValue2").hidden = false;
        document.getElementById("GainValue3").hidden = true;
        document.getElementById("GainValue4").hidden = true;
        document.getElementById("GainValue5").hidden = true;
        document.getElementById("Gain1").hidden = true;
        document.getElementById("Gain2").hidden = false;
        document.getElementById("Gain3").hidden = true;
        document.getElementById("Gain4").hidden = true;
        document.getElementById("Gain5").hidden = true;

        document.getElementById("TowerSelect1").hidden = true;
        document.getElementById("TowerSelect2").hidden = false;
        document.getElementById("TowerSelect3").hidden = true;
        document.getElementById("TowerSelect4").hidden = true;
        document.getElementById("TowerSelect5").hidden = true;

        document.getElementById("a1-1").hidden = true;
        document.getElementById("a1-2").hidden = true;
        document.getElementById("a1-3").hidden = true;
        document.getElementById("a1-4").hidden = true;

        document.getElementById("a2-1").hidden = false;
        document.getElementById("a2-2").hidden = false;
        document.getElementById("a2-3").hidden = false;
        document.getElementById("a2-4").hidden = false;

        document.getElementById("a3-1").hidden = true;
        document.getElementById("a3-2").hidden = true;
        document.getElementById("a3-3").hidden = true;
        document.getElementById("a3-4").hidden = true;

        document.getElementById("a4-1").hidden = true;
        document.getElementById("a4-2").hidden = true;
        document.getElementById("a4-3").hidden = true;
        document.getElementById("a4-4").hidden = true;
        
        document.getElementById("a5-1").hidden = true;
        document.getElementById("a5-2").hidden = true;
        document.getElementById("a5-3").hidden = true;
        document.getElementById("a5-4").hidden = true;
    }
    if (id == 3) {
        document.getElementById("GainValue1").hidden = true;
        document.getElementById("GainValue2").hidden = true;
        document.getElementById("GainValue3").hidden = false;
        document.getElementById("GainValue4").hidden = true;
        document.getElementById("GainValue5").hidden = true;
        document.getElementById("Gain1").hidden = true;
        document.getElementById("Gain2").hidden = true;
        document.getElementById("Gain3").hidden = false;
        document.getElementById("Gain4").hidden = true;
        document.getElementById("Gain5").hidden = true;

        document.getElementById("TowerSelect1").hidden = true;
        document.getElementById("TowerSelect2").hidden = true;
        document.getElementById("TowerSelect3").hidden = false;
        document.getElementById("TowerSelect4").hidden = true;
        document.getElementById("TowerSelect5").hidden = true;

        document.getElementById("a1-1").hidden = true;
        document.getElementById("a1-2").hidden = true;
        document.getElementById("a1-3").hidden = true;
        document.getElementById("a1-4").hidden = true;

        document.getElementById("a2-1").hidden = true;
        document.getElementById("a2-2").hidden = true;
        document.getElementById("a2-3").hidden = true;
        document.getElementById("a2-4").hidden = true;
        
        document.getElementById("a3-1").hidden = false;
        document.getElementById("a3-2").hidden = false;
        document.getElementById("a3-3").hidden = false;
        document.getElementById("a3-4").hidden = false;
        
        document.getElementById("a4-1").hidden = true;
        document.getElementById("a4-2").hidden = true;
        document.getElementById("a4-3").hidden = true;
        document.getElementById("a4-4").hidden = true;
        
        document.getElementById("a5-1").hidden = true;
        document.getElementById("a5-2").hidden = true;
        document.getElementById("a5-3").hidden = true;
        document.getElementById("a5-4").hidden = true;
    }
    if (id == 4) {
        document.getElementById("GainValue1").hidden = true;
        document.getElementById("GainValue2").hidden = true;
        document.getElementById("GainValue3").hidden = true;
        document.getElementById("GainValue4").hidden = false;
        document.getElementById("GainValue5").hidden = true;
        document.getElementById("Gain1").hidden = true;
        document.getElementById("Gain2").hidden = true;
        document.getElementById("Gain3").hidden = true;
        document.getElementById("Gain4").hidden = false;
        document.getElementById("Gain5").hidden = true;

        document.getElementById("TowerSelect1").hidden = true;
        document.getElementById("TowerSelect2").hidden = true;
        document.getElementById("TowerSelect3").hidden = true;
        document.getElementById("TowerSelect4").hidden = false;
        document.getElementById("TowerSelect5").hidden = true;
        
        document.getElementById("a1-1").hidden = true;
        document.getElementById("a1-2").hidden = true;
        document.getElementById("a1-3").hidden = true;
        document.getElementById("a1-4").hidden = true;
        
        document.getElementById("a2-1").hidden = true;
        document.getElementById("a2-2").hidden = true;
        document.getElementById("a2-3").hidden = true;
        document.getElementById("a2-4").hidden = true;

        document.getElementById("a3-1").hidden = true;
        document.getElementById("a3-2").hidden = true;
        document.getElementById("a3-3").hidden = true;
        document.getElementById("a3-4").hidden = true;

        document.getElementById("a4-1").hidden = false;
        document.getElementById("a4-2").hidden = false;
        document.getElementById("a4-3").hidden = false;
        document.getElementById("a4-4").hidden = false;
        
        document.getElementById("a5-1").hidden = true;
        document.getElementById("a5-2").hidden = true;
        document.getElementById("a5-3").hidden = true;
        document.getElementById("a5-4").hidden = true;
    }
    if (id == 5) {
        document.getElementById("GainValue1").hidden = true;
        document.getElementById("GainValue2").hidden = true;
        document.getElementById("GainValue3").hidden = true;
        document.getElementById("GainValue4").hidden = true;
        document.getElementById("GainValue5").hidden = false;
        document.getElementById("Gain1").hidden = true;
        document.getElementById("Gain2").hidden = true;
        document.getElementById("Gain3").hidden = true;
        document.getElementById("Gain4").hidden = true;
        document.getElementById("Gain5").hidden = false;

        document.getElementById("TowerSelect1").hidden = true;
        document.getElementById("TowerSelect2").hidden = true;
        document.getElementById("TowerSelect3").hidden = true;
        document.getElementById("TowerSelect4").hidden = true;
        document.getElementById("TowerSelect5").hidden = false;

        document.getElementById("a1-1").hidden = true;
        document.getElementById("a1-2").hidden = true;
        document.getElementById("a1-3").hidden = true;
        document.getElementById("a1-4").hidden = true;
        
        document.getElementById("a2-1").hidden = true;
        document.getElementById("a2-2").hidden = true;
        document.getElementById("a2-3").hidden = true;
        document.getElementById("a2-4").hidden = true;

        document.getElementById("a3-1").hidden = true;
        document.getElementById("a3-2").hidden = true;
        document.getElementById("a3-3").hidden = true;
        document.getElementById("a3-4").hidden = true;

        document.getElementById("a4-1").hidden = true;
        document.getElementById("a4-2").hidden = true;
        document.getElementById("a4-3").hidden = true;
        document.getElementById("a4-4").hidden = true;
        
        document.getElementById("a5-1").hidden = false;
        document.getElementById("a5-2").hidden = false;
        document.getElementById("a5-3").hidden = false;
        document.getElementById("a5-4").hidden = false;
    }
};
function store_checkbox_value(checkbox, id) {
    // Get the checkbox state
    const isChecked = checkbox.checked;
    
    // Store the checkbox state in local storage
    sessionStorage.setItem('powerButtonState'+id, isChecked);
};

// Check if the button state is stored in local storage
function page_load_checkbox(){
    const storedPowerButtonState1 = sessionStorage.getItem('powerButtonState1');
    const storedPowerButtonState2 = sessionStorage.getItem('powerButtonState2');
    const storedPowerButtonState3 = sessionStorage.getItem('powerButtonState3');
    const storedPowerButtonState4 = sessionStorage.getItem('powerButtonState4');
    const storedPowerButtonState5 = sessionStorage.getItem('powerButtonState5');
    // Set initial state based on local storage
};


function change_apower(id) {
    $.ajax({
            url: "/antenna_pow/" + id,
            method: "POST",
            dataType: "json",
            success: function(data) {
                // Handle success if needed
            },
            error: function(xhr, status, error) {
                console.error("Error sending antenna power: " + error);
            }
    });
};
function page_load_apower(){
    const aButtonState11 = sessionStorage.getItem('aButtonState11');
    const aButtonState12 = sessionStorage.getItem('aButtonState12');
    const aButtonState13 = sessionStorage.getItem('aButtonState13');
    const aButtonState14 = sessionStorage.getItem('aButtonState14');
    if(aButtonState11 == 'false'){
        document.getElementById("onoff1-1").checked = false
    }
    else{
        document.getElementById("onoff1-1").checked = true
    }
    if(aButtonState12 == "false"){
        document.getElementById("onoff1-2").checked = false
    }
    else{
        document.getElementById("onoff1-2").checked = true
    }
    if(aButtonState13 == "false"){
        document.getElementById("onoff1-3").checked = false
    }
    else{
        document.getElementById("onoff1-3").checked = true
    }
    if(aButtonState14 == "false"){
        document.getElementById("onoff1-4").checked = false
    }
    else{
        document.getElementById("onoff1-4").checked = true
    }


    const aButtonState21 = sessionStorage.getItem('aButtonState21');
    const aButtonState22 = sessionStorage.getItem('aButtonState22');
    const aButtonState23 = sessionStorage.getItem('aButtonState23');
    const aButtonState24 = sessionStorage.getItem('aButtonState24');
    if(aButtonState21 == 'false'){
        document.getElementById("onoff2-1").checked = false
    }
    else{
        document.getElementById("onoff2-1").checked = true
    }
    if(aButtonState22 == "false"){
        document.getElementById("onoff2-2").checked = false
    }
    else{
        document.getElementById("onoff2-2").checked = true
    }
    if(aButtonState23 == "false"){
        document.getElementById("onoff2-3").checked = false
    }
    else{
        document.getElementById("onoff2-3").checked = true
    }
    if(aButtonState24 == "false"){
        document.getElementById("onoff2-4").checked = false
    }
    else{
        document.getElementById("onoff2-4").checked = true
    }

    const aButtonState31 = sessionStorage.getItem('aButtonState31');
    const aButtonState32 = sessionStorage.getItem('aButtonState32');
    const aButtonState33 = sessionStorage.getItem('aButtonState33');
    const aButtonState34 = sessionStorage.getItem('aButtonState34');
    if(aButtonState31 == 'false'){
        document.getElementById("onoff3-1").checked = false
    }
    else{
        document.getElementById("onoff3-1").checked = true
    }
    if(aButtonState32 == "false"){
        document.getElementById("onoff3-2").checked = false
    }
    else{
        document.getElementById("onoff3-2").checked = true
    }
    if(aButtonState33 == "false"){
        document.getElementById("onoff3-3").checked = false
    }
    else{
        document.getElementById("onoff3-3").checked = true
    }
    if(aButtonState34 == "false"){
        document.getElementById("onoff3-4").checked = false
    }
    else{
        document.getElementById("onoff3-4").checked = true
    }
    const aButtonState41 = sessionStorage.getItem('aButtonState41');
    const aButtonState42 = sessionStorage.getItem('aButtonState42');
    const aButtonState43 = sessionStorage.getItem('aButtonState43');
    const aButtonState44 = sessionStorage.getItem('aButtonState44');
    if(aButtonState41 == 'false'){
        document.getElementById("onoff4-1").checked = false
    }
    else{
        document.getElementById("onoff4-1").checked = true
    }
    if(aButtonState42 == "false"){
        document.getElementById("onoff4-2").checked = false
    }
    else{
        document.getElementById("onoff4-2").checked = true
    }
    if(aButtonState43 == "false"){
        document.getElementById("onoff4-3").checked = false
    }
    else{
        document.getElementById("onoff4-3").checked = true
    }
    if(aButtonState44 == "false"){
        document.getElementById("onoff4-4").checked = false
    }
    else{
        document.getElementById("onoff4-4").checked = true
    }
    const aButtonState51 = sessionStorage.getItem('aButtonState51');
    const aButtonState52 = sessionStorage.getItem('aButtonState52');
    const aButtonState53 = sessionStorage.getItem('aButtonState53');
    const aButtonState54 = sessionStorage.getItem('aButtonState54');
    if(aButtonState51 == 'false'){
        document.getElementById("onoff5-1").checked = false
    }
    else{
        document.getElementById("onoff5-1").checked = true
    }
    if(aButtonState52 == "false"){
        document.getElementById("onoff5-2").checked = false
    }
    else{
        document.getElementById("onoff5-2").checked = true
    }
    if(aButtonState53 == "false"){
        document.getElementById("onoff5-3").checked = false
    }
    else{
        document.getElementById("onoff5-3").checked = true
    }
    if(aButtonState54 == "false"){
        document.getElementById("onoff5-4").checked = false
    }
    else{
        document.getElementById("onoff5-4").checked = true
    }
    // Set initial state based on local storage
};
function store_apower_value(checkbox, id) {
    // Get the checkbox state
    const isaChecked = checkbox.checked;

    // Store the checkbox state in local storage
    sessionStorage.setItem('aButtonState'+id, isaChecked);
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
};

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
};

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
};

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
};
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
    iconUrl: 'https://github.com/frankuman/5imFortress/blob/main/frontend/gui/templates/img/113141.png?raw=true', // URL to your tower icon image
    iconSize: [60, 120], // Size of the icon
    iconAnchor: [32, 92], // Point of the icon which will correspond to marker's location
    popupAnchor: [0, -64] // Point from which the popup should open relative to the iconAnchor
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

    map.on('zoomend', function() {
        var zoomLevel = map.getZoom();
        var scaleFactor = zoomLevel; // Adjust as needed
        marker.iconSize = [30 * scaleFactor, 60 * scaleFactor];
    });
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
