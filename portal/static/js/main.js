var $ = jQuery.noConflict();

$(document).ready(function(){
    $("#goverment").attr("disabled", !this.checked);
    $("#id_choose_goverment").click(function() {
        $("#goverment").attr("disabled", !this.checked);
    });
    $("#public").attr("disabled", !this.checked);
    $("#id_choose_local").click(function() {
        $("#public").attr("disabled", !this.checked);
    });
   
}( jQuery ) );