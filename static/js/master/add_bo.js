$("#add_bo_form").submit(function (e) {
  e.preventDefault();
  // let data = $(this).serializeArray()
  // let data = $(this).serializeArray()
  data = new FormData(this)
  // console.log(data);
  $.ajax({
    type: "post",
    url: "/add_bo_api",
    cache: false,
    processData: false,
    contentType: false,
    enctype: 'multipart/form-data',
    data: data,
    success: function (response) {
      toastr.success(response.message)
      setTimeout(function () {
        window.location.href="/bo"
      },2000)
    },
    error: function (response) {
      toastr.error(response.responseJSON.error)
    }
  });
});

