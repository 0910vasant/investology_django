$("#punch_in").click(function (e) { 
    e.preventDefault();
    $.ajax({
        // type : "post",
        url  : "/punch_in",
        success: function (response) {
            toastr.success(response.message)
            t.ajax.reload(null,false)
        //   $(`#${modal_id}`).modal("toggle");
            // window.location.reload()
            // window.location.href = `/dashboard`
        },
        error: function (response) {
            toastr.error(response.responseJSON.error)
        },
    });
});

// console.log("enter punch in");