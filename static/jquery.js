

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
function add_active(){
    var this_url = window.location.pathname;
    var list_sidebar_link = $(".menu li a");
    $(list_sidebar_link).each(function (i, item) {
        var the_a = list_sidebar_link[i];
        if (this_url == $(the_a).attr('href')) {
            $(the_a).addClass('active');
        }
    });
};


/* 

// Get all the links in the sidebar
const sidebarLinks = document.querySelectorAll('.sidebar a');

// Loop through the links and check if the data-option matches the current page
sidebarLinks.forEach(link => {
  if (link.getAttribute('data-option') === getCurrentPageOption()) {
    link.classList.add('selected');
  }
});

// Function to extract the current page's option from the URL
function getCurrentPageOption() {
  const currentURL = window.location.href;
  const optionMatches = currentURL.match(/\/([^/]+)$/); // Extracts the last part of the URL
  if (optionMatches && optionMatches[1]) {
    return optionMatches[1].toLowerCase(); // Convert to lowercase for case-insensitive comparison
  }
  return ''; // Default to an empty string if no match is found
}
*/