$(".create_login").submit(function (e) {
    e.preventDefault();
    data = $(this).serializeArray()

    // modal_id = $(this).parents(".modal").attr("id")
    
    password = data[4].value
    password1 = data[5].value

    console.log("data",data);
    if (password == password1) {
        $.ajax({
            type : "post",
            url  : "/create_user_login",
            data : data ,
            success: function (response) {
              toastr.success(response.message)
            //   $(`#${modal_id}`).modal("toggle");
              // window.location.reload()
              $(".create_login").trigger("reset")
              $("#loginModal1").modal("hide")
              t.ajax.reload()
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


