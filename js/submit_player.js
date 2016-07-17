$(document).ready(function(){

    $('#player-message').dialog({
        modal: true,
        autoOpen: false,
        buttons: {
            Ok: function() {
                $(this).dialog("close");
            }
        }
    });



    $('#player-button').on('click', function() {
        var name = $('#fname').val();

        var dataString = 'name=' + name + '&email=' + email + '&subject=' + subject + '&message=' + message;
        $.ajax({
            type: "POST",
            url: "/echo/json",
            data: dataString,
            success: function() {
                $('#player-message').dialog('open');
            }
        });
    });
});