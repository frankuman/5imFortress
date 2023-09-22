

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

        // Call the updateBitrate function initially to display the initial bitrate
        

        // Set up an interval to regularly update the bitrate (e.g., every 5 seconds)
         // Adjust the interval as needed

