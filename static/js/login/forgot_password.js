$("#forgot_password_form").submit(function (e) { 
    e.preventDefault();
    data = $(this).serializeArray()
    console.log("data",data);
    new_pass = data[3].value
    conf_pass = data[4].value
    if (new_pass == conf_pass) {
        $.ajax({
            type : "post",
            url  : "/forgot_password",
            data : data ,
            success: function (response) {
                $("#forgot_password_modal").modal("toggle");
                toastr.success(response.message)
                // window.location.reload()
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

$('#forgot_password_modal').on('hidden.bs.modal', function (e) {
    $("#forgot_password_form").trigger("reset")
})

$("body").on("click",".fp", function () {
    user_id = $(this).data("id")
    user_type = $(this).data("u_type")

    console.log(user_id,user_type);
    $("#forgot_password_form #f_user_id").val(user_id)
    $("#forgot_password_form #f_user_type").val(user_type)
});


