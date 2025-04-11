$("#login_from").submit(function (e) { 
    e.preventDefault();
    data = $(this).serializeArray()
    $.ajax({
        type : "post",
        url  : "/login",
        data : data ,
        success: function (response) {
            toastr.success(response.message)
            window.location.href = "/"
        //   $(`#${modal_id}`).modal("toggle");
            // window.location.reload()
            // if (user_type == "bo") {
            //     console.log("bo");
            //     // window.location.href = `/attendance`
            // }
            // else{
            //     console.log("no_bo");
            //     // window.location.href = `/dashboard`
            // }
            
        },
        error: function (response) {
            if (response.status==412) {
                toastr.error(response.responseJSON.error)
            }
            if (response.status==500) {
                toastr.error("Something went wrong")
            }
        },
    });
});



// console.log("enter Login");