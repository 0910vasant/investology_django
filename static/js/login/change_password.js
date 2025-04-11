$("#change_password_form").submit(function (e) { 
    e.preventDefault();
    data = $(this).serializeArray()
    new_pass = $("#new_pass").val()
    old_pass = $("#conf_pass").val()
    if (new_pass == old_pass) {
        $.ajax({
            type : "post",
            url  : "/change_password",
            data : data ,
            success: function (response) {
                toastr.success(response.message)
            //   $(`#${modal_id}`).modal("toggle");
                window.location.reload()
                // window.location.href = `/dashboard`
            },
            error: function (response) {
                toastr.error(response.responseJSON.error)
            },
        });
    }
    else{
        toastr.error("Password And Confirm Paswword must Be same")
    }
});

$('#change_password_modal').on('hidden.bs.modal', function (e) {
    $("#change_password_form").trigger("reset")
})
