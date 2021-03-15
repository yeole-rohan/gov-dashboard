var $ = jQuery.noConflict();

$(document).ready(function(){
  $("#id_first_name").attr('placeholder', 'Grampanchayat Name');
  $("#id_last_name").attr('placeholder', 'Block Name');
  $("#id_email").attr('placeholder', 'Email ');
  $("#id_phone_number").attr('placeholder', 'Mobile Number');
  $("#id_password1").attr('placeholder', 'Password');
  $("#id_password2").attr('placeholder', 'Confirm Password');
  $('#id_username').attr('placeholder', 'User ID');
  $('#id_password').attr('placeholder', 'Enter Password');
  
  $("#id_district").change(function () {
    var url = $("#register").attr("data-cities-url");  // get the url of the `load_cities` view
    var districtId = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
        'district': districtId       // add the country id to the GET parameters
        },
        success: function (data) { 
             // `data` is the return of the `load_cities` view function
        $("#id_taluka").html(data);  // replace the contents of the city input with the data that came from the server
        }
    });

    });
    $("#id_taluka").change(function () {
    var url = $("#register").attr("data-taluka-url");  // get the url of the `load_cities` view
    var talukaID = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
        'taluka': talukaID       // add the country id to the GET parameters
        },
        success: function (data) { 
         // `data` is the return of the `load_cities` view function
        $("#id_panchayat").html(data);  // replace the contents of the city input with the data that came from the server
        }
    });
    });
}( jQuery ) );