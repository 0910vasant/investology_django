$('#add_demat_account').on('hidden.bs.modal', function (e) {
    $("#add_account_form").trigger("reset")
    $("#add_account_form .select2").val("").change()
})

$("#add_account_form").submit(function (e) {
    e.preventDefault();
    data = $(this).serializeArray()

    $.ajax({
        type: "post",
        url: "/add_demat_account",
        data: data,
        success: function (response) {
        toastr.success(response)
        $("#add_demat_account").modal("toggle")
        t.ajax.reload()
        },
        error: function (response){
        toastr.error(response.responseJSON)
        }
    });
});

$("body").on("click",".edit_modal", function () {
    let id = $(this).data("id")
    $("#edit_account_form").prop("action",`/edit_demat_account/${id}`)
    $.ajax({
        url: `/get_demat_account/${id}`,
        success: function (response) {
          let data = response[0]
          $("#edit_account_form #customer").val(data.DEMAT_CUST_id).change()
          if(data.DEPOSITORY_TYPE == "nsdl"){
            $(`#edit_account_form input[name=depositary_type][value="nsdl"]`).prop('checked',true)
          }
        //   $("#edit_account_form #depositary_type").val(data.DEPOSITORY_TYPE)
          $("#edit_account_form #acc_no").val(data.ACC_NO)
          $("#edit_account_form #client_id").val(data.CLIENT_ID)
          $("#edit_account_form #commission").val(data.COMMISSION)
        },
        error: function (response){
            // console.log("error",response);
        }
    });
});


$("#edit_account_form").submit(function (e) {
  e.preventDefault();
  data = $(this).serializeArray()
  url = $(this).attr("action");
  $.ajax({
    type: "post",
    url: url,
    data: data,
    success: function (response) {
      toastr.success(response)
      $("#edit_demat_account").modal("toggle")
      t.ajax.reload()
    },
    error: function (response){
      toastr.error(response.responseJSON)
    }
  });
});