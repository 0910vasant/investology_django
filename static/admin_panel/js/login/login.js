$('#show_password').click(function(){
    if ($(this).is(':checked')) {
        console.log("enter if");
        $('#password').attr('type', 'text')
    } else {
        console.log("enter else");
        $('#password').attr('type', 'password')
    }
});