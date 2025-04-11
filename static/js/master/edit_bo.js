$("#edit_bo_form").submit(function (e) {
  e.preventDefault();
  let id = window.location.pathname.split("/")[2]
  // console.log("id",id);
  data = new FormData(this)
  // let data = $(this).serializeArray()
  // console.log(data);
  $.ajax({
    type: "post",
    url: `/edit_bo_api/${id}`,
    cache: false,
    processData: false,
    contentType: false,
    enctype: 'multipart/form-data',
    data: data,
    success: function (response) {
      toastr.success(response.message)
      // setTimeout(function () {
      //   window.location.href = "/bo"
      // },1000)
    }
  });
});