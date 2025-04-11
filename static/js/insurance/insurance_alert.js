var t

t = $('#insurance_alert_table').DataTable( {
  ajax: '/load_insurance_alert',

  columns: [
      { data: null },
      { data: 'CUSTOMER__C_NAME' },
      { data: 'CUSTOMER__MOB_NO' },
      { data: 'TYPE_INSURANCE__NAME' },
      { data: 'INSURANCE_PERIOD' },
      { data: 'START_DATE' },
      { data: 'RENEWAL_DATE' },
    //   { data: 'NAME' },
    //   { data: null },
  ],
 
//   columnDefs: [
//       { className: 'text-center', targets: [0,1,2,3,4,5,6,7] },
//       {
//         targets: [7], render: function (a, b, data, d){
//             html = `<div class="dropdown">
//                         <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
//                         Action
//                         </button>
//                         <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
//                             <a class="dropdown-item" href="/edit_insurance_alert/${data.id}"><i class="fa fa-edit"></i> Edit</a>
//                             <hr class="drop-hr">
//                             <a class="dropdown-item delete_modal" href="javascript:void(0);" data-url="/delete_insurance_alert/${data.id}"><i class="fa fa-trash"></i> Delete</a>
//                         </div>
//                     </div>`
//            return html
//         },
//       },
//   ],
  } );
  t.on( 'order.dt search.dt', function () {
      t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          // console.log(i,cell)
          cell.innerHTML = i+1;
      } );
  } ).draw();


$("body").on("click",".delete_modal", function () {
    let url = $(this).data("url")
    console.log("entere",url);
    $.ajax({
        type: "get",
        url: url,
        success: function (response) {
            t.ajax.reload(null,false)
            toastr.success(response.message)
        },
        error: function (response){
            toastr.error(response.responseJSON.error)
            // console.log("error",response);
        }
    });
});

// $("#add_insurace_name_form").submit(function (e) { 
//     e.preventDefault();
//     data = $(this).serializeArray();
//     $.ajax({
//         type: "post",
//         url: "/add_insurance_name",
//         data: data,
//         success: function (response) {
//             $("#add_insurace_name").modal("toggle");
//             t.ajax.reload()
//             toastr.success(response.message)
//         },
//         error: function (response) {
//             // console.log("response",response);
//             toastr.error(response.responseJSON.error)
//             console.log("error");
//         },
//     });
// });

// $('#add_insurace_name').on('hidden.bs.modal', function (e) {
//     $("#add_insurace_name_form").trigger("reset")
// })
// $("#edit_insurace_name_form").on('submit', function (e) {
//     e.preventDefault()
//     data = $(this).serializeArray()
//     url = $(this).attr('action');
//     $.ajax({
//       type: "post",
//       url: url,
//       data : data ,
//       success: function (response) {
//         $("#edit_insurace_name").modal("toggle");
//         t.ajax.reload(null,false)
//         toastr.success(response.message)
//       },
//       error: function (response) {
//         toastr.error(response.responseJSON.error)
//         console.log("error");
//       },
//     });
//   });

// $("body").on("click",".edit_modal", function () {
//     let id = $(this).data("id")
//     // console.log("entered",id);
//     url = `/edit_insurance_name/${id}`

//     $("#edit_insurace_name_form").prop("action",url)
//     $.ajax({
//         type: "get",
//         url: url,
//         success: function (response) {
//           console.log("response",response[0].NAME);
//           $("#edit_insurace_name_form #insurance_name").val(response[0].NAME);
//         },
//         error: function (response){
//             // console.log("error",response);
//         }
//     });
// });