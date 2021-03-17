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
    $('#confirm1').attr("disabled", !this.checked);
    $('#id_yes_no').click(function() {
        $("#confirm1").attr("disabled", !this.checked);
    });
    $('#confirm2').attr("disabled", !this.checked);
    $('#id_yes_no').click(function() {
        $("#confirm2").attr("disabled", !this.checked);
    });
    $('#confirm3').attr("disabled", !this.checked);
    $('#id_yes_no').click(function() {
        $("#confirm3").attr("disabled", !this.checked);
    });
      $( "input[name='utrno'], input[name='utr']" ).change(function() {
        $l = $(this).val().length
        console.log($l);
        if ($l == 16) {
            $(".sel-rtgs.pay").removeAttr('disabled');
        }else{
            alert("please enter 16 Digits Number, You entered " + $l)
        }
      });

      
      $( "input[name='document']" ).change(function() {
        $l = $(this).val().length
        console.log($l);
        if ($l > 0) {
            $(".pay").removeAttr('disabled');
        }else{
            alert("please upload file")
        }
      });
      $( "input[name='files']" ).change(function() {
        $l = $(this).val().length
        console.log($l);
        if ($l > 0) {
            $(".pay").removeAttr('disabled');
        }else{
            alert("please upload file")
        }
      });
}( jQuery ) );