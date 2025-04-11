var url = window.location.pathname
var id = url.split("/").at(-1)

var t = $('#pay_out_history_table').DataTable({
  ajax: `/get_ep_pay_out/${id}`,
  dom: 'lBfrtip',
  buttons: [
    {
      text: '<span><i class="fa fa-refresh" aria-hidden="true"></i>&nbsp;Refresh</span>',
      className: 'btn btn-primary ml-2',
      action: function ( e, dt, node, config ) {
        dt.ajax.reload();
        toastr.success("Table Refreshed")
      }
    }
  ],
  columns: [
      { data: null },
      { data: 'AMOUNT' },
      { data: 'TRANSACTION_CHECK_NO' },
      { data: 'TRANSACTION_DATE' },
      { data: null },
  ],
  columnDefs: [
    { className: 'text-center', targets: [0,1,2,3,4] },
    {
      targets: [4], render: function (a, b, data, d){
        html = `
        <div class="dropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Action
          </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="will-change: transform;">
        <a class="dropdown-item edit" data-toggle="modal" href="javascript:void(0);" data-id="${data.id}" data-target="#edit_pay_out_modal"><i class="fa fa-edit" aria-hidden="true"></i>Edit</a>
        <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>
      </div>`
       return html
      },
    }
  ]
});
t.on( 'order.dt search.dt', function () {
  t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
      // console.log(i,cell)
      cell.innerHTML = i+1;
  } );
} ).draw();


$.ajax({
  type: "get",
  url: "/all_ep",
  success: function (response) {
    let html = [`<option value="">Select EP</option>`]
    $.each(response, function (i, v) {
      html.push(`<option value="${v.id}">Name: ${v.NAME} | Username: ${v.USERNAME}</option>`)
    });
    $(".ep").html(html.join(""))
  }
});

$("#add_pay_out_form").submit(function (e) { 
  e.preventDefault();
  let data = $(this).serializeArray();
  $.ajax({
    type: "post",
    url: "/add_pay_out",
    data: data,
    success: function (response) {
      toastr.success(response)
      $("#add_pay_out_modal").modal("hide")
      $("#add_pay_out_form").trigger("reset")
      t.ajax.reload()
    },
    error: function(response){
      toastr.error("Something went wrong")
    }
  });
});

$("body").on("click",".edit", function () {
  let id = $(this).data("id")
  $.ajax({
    type: "get",
    url: `/get_pay_out/${id}`,
    success: function (response) {
      $("#edit_pay_out_form #id").val(response[0].id).change()
      $("#edit_pay_out_form #ep").val(response[0].EP_id).change()
      $("#edit_pay_out_form #amount").val(response[0].AMOUNT).change()
      $("#edit_pay_out_form #transaction_check_no").val(response[0].TRANSACTION_CHECK_NO).change()
      $("#edit_pay_out_form #transaction_date").val(response[0].TRANSACTION_DATE).change()
    }
  });
});


$("#edit_pay_out_form").submit(function (e) { 
  e.preventDefault();
  let data = $(this).serializeArray();
  $.ajax({
    type: "post",
    url: "/edit_pay_out",
    data: data,
    success: function (response) {
      toastr.success(response)
      $("#edit_pay_out_modal").modal("hide")
      $("#edit_pay_out_form").trigger("reset")
      t.ajax.reload()
    },
    error: function(response){
      toastr.error("Something went wrong")
    }
  });
});

$("body").on("click",".delete", function () {
  let id = $(this).data("id");
  $.ajax({
    type: "get",
    url: `/delete_pay_out/${id}`,
    success: function (response) {
      toastr.success(response)
      t.ajax.reload()
    },
    error: function (response){
      toastr.error("Something went wrong")
    }
  });
});