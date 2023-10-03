

function updateBitrate() {
    $.ajax({
        url: "/get_bitrate",  // Update this URL with the endpoint of your Flask backend
        method: "GET",
        dataType: "json",
        success: function(data) {
            // Update the bitrate in the HTML element
            $("#bitrate1").html(data.bitrate1 + " Mbps");
            $("#bitrate2").html(data.bitrate2 + " Mbps");
            console.log(bitrate1,bitrate2)
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
          console.log(bsusers1,bsusers2)
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
        console.log(bsusers1,bsusers2)
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
            // Update the bitrate in the HTML element
            $("#bsstatus1").html(data.bsstatus1);
            $("#bsstatus2").html(data.bsstatus2);
            console.log(bsusers1,bsusers2)
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

// function get_check(){
//     let isChecked = localStorage.getItem("checkedbox");
//     // now set it
//     $('#checkbox').prop('checked', isChecked)
// };

// function change_checked(checkbox) {
//     localStorage.setItem("checkedbox", checkbox.prop('checked'));
//     $("form").submit();
// };
