var t = $('#payment_table').DataTable({
  ajax: '/payment_table',
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
      { data: 'ep_name' },
      { data: 'insurance_commission' },
      { data: 'fd_commission' },
      { data: 'mf_commission' },
      { data: 'total_earned_commission' },
      { data: 'total_paid_commission' },
      { data: 'total_due_commission' },
      { data: null },
  ],
  columnDefs: [
    { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8] },
    {
      targets: [8], render: function (a, b, data, d){
        // console.log(d)
        html = `<a class="btn btn-primary history" href="/payout_history/${data.id}" target="_blank"><i class="fa fa-history" aria-hidden="true"></i>&nbsp;Payout History</a>`
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
  data = $(this).serializeArray()
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
    error: function(response) {
      toastr.error("Something went wrong")
    }
  });
});

$("#refresh_table").click(function (e) { 
  e.preventDefault();
  t.ajax.reload();
  toastr.info("Table Refreshed")
});

// $("body").on("click",".history", function () {
//   let id = $(this).data("id")
//   history_table.ajax.reload(`/get_ep_pay_out/${id}`)
// });

// $('#edit_pay_out_modal').on('shown.bs.modal', function (e) {
//   $("#pay_out_history_modal").modal("toggle")
// })


// $('#edit_pay_out_modal').on('hide.bs.modal', function (e) {
//   $("#pay_out_history_modal").modal("toggle")
// })