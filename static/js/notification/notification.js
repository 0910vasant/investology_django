var t

t = $('#notifications_table').DataTable( {
  ajax: '/load_notifications',

  columns: [
      { data: null },
      { data: 'DATE' },
      { data: 'TITLE' },
      { data: 'DESCRIPTION' },
    //   { data: 'NAME' },
    //   { data: null },
  ],
  columnDefs: [
    { className: 'text-center', targets: [0,1,2,3,4] },
    {
        targets: [1], render: function (a, b, data, d){
          // let date = new Date(Date)
          let date = moment(data.CREATED_DATE).format('DD/MM/YYYY');
          return date
        },
    },
    {
        // puts a button in the last column
      // targets: [1], render: function (a, b, data, d){
      //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
      //   console.log("data.CREATED_DATE",data.CREATED_DATE);
      //   console.log("html",html);
      // return html
      // },
        targets: [4], render: function (a, b, data, d){
          // console.log(d)
          html = `<div class="dropdown">
                      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      Action
                      </button>
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item view_data" data-toggle="modal" href="javascript:void(0);" data-id="${data.id}" data-type="${data.TYPE}" data-target="#viewModal"><i class="fa fa-eye" aria-hidden="true"></i>View</a>
                      </div>
                  </div>`
         return html
        },
    }
  ],
  } );
  t.on( 'order.dt search.dt', function () {
      t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          // console.log(i,cell)
          cell.innerHTML = i+1;
      } );
  } ).draw();


// $(".notify_cust_t").change(function (e) {
//     cust_data = [`<option value="" disabled>Please Select Customer</option>`]
//     let cust_type = $(this).val()
//     $.ajax({
//     type: "get",
//     url: `/filter_customer?customer_type=${cust_type}`,
//     success: function (response) {
//         console.log("response",response);
//         t.ajax.reload()
//         if (cust_type == "mf_customer") {
//             $.each(response, function (i, v) {
//                 cust_data.push(`<option value="${v.id}">${v.NAME} || ${v.MOBILE}</option>`)
//             });
//         }
//         if (cust_type == "insurance_customer" || cust_type == "customer_lead") {
//             $.each(response, function (i, v) {
//                 cust_data.push(`<option value="${v.id}">${v.C_NAME} || ${v.MOB_NO}</option>`)
//             });
//         }
//         $("#notify_cust").html(cust_data.join(""))
//     }
//     });
// });



$("#notification_send_form").submit(function (e) { 
    e.preventDefault();
    let data = $(this).serializeArray()
    $.ajax({
        type: "post",
        url: "/send_notification",
        data: data,
        success: function (response) {
            toastr.success(response.message)
            $("#notification_send").modal("toggle")
            t.ajax.reload()
        },
        error: function (response) {
            toastr.success("Something went wrong")
        }
    });
});
// $('#notification_send').on('hidden.bs.modal', function (e) {
//   $("#notification_send_form").trigger("reset")
// })

$('#notification_send').on('hidden.bs.modal', function (e) {
    $("#notification_send_form").trigger("reset")
    $("#notification_send_form .select2").change()
})

  $("body").on("click",".view_data",function () { 
      id = $(this).data("id")
      type = $(this).data("type")
      // console.log("data",data);
      // console.log("type",type);
      // id
      data = []
      $.ajax({
          url: `/get_notification_users/${id}`,
          success: function (response) {
              $("#cust_list tbody").html()
              $.each(response, function (i, v) {
                  data.push(`<tr>
                              <td>${i+1}</td>
                              <td>${v.C_NAME}</td>
                              <td>${v.MOB_NO}</td>
                          </tr>`)
              });
              
              $("#cust_list tbody").html(data.join(""))
          }
      });

  })

$(".cust_t,.user,.u_type").change(function (e) {
    
    let cust_type = $(this).parents(".modal-body").find("#cust_t").val()
    let user = $(this).parents(".modal-body").find("#user").val()
    let u_type = $(this).parents(".modal-body").find("#u_type").val()

    // console.log("cust_type",cust_type);
    // console.log("user",user);
    // console.log("u_type",u_type);
    if (cust_type != "" && cust_type != null  && user != "" && user != null && u_type != "" && u_type != null) {
    //   console.log("enter If");
      $.ajax({
        type: "get",
        url: `/filter_customer`,
        data: {
          "customer_type":cust_type,
          "user":user,
          "u_type":u_type,
        },
        success: function (response) {
          
          let customer_html = [`<option value="" disabled="">Please Select Customer</option>`]
          // if (cust_type == "customer_lead"){
          //   $.each(response, function (i, v) { 
          //     customer_html.push(`<option value="${v.id}">${v.NAME} | ${v.MOBILE}</option>`)
          //   });
          // }
          $.each(response, function (i, v) {
              customer_html.push(`<option value="${v.id}">${v.C_NAME} | ${v.MOB_NO}</option>`)
          });
          $("#notify_cust").html(customer_html.join(""));
        }
      });
    }
});

$("#all_customer").click(function () { 
  if ($('#all_customer').is(":checked")){
    $("#notify_cust option").prop('selected', true);
    $("#notify_cust").change()
  }
  else{
    $("#notify_cust option").prop('selected', false);
    $("#notify_cust").change()
  }
});

$("body").on("change","#notify_cust", function () {
  if ($(this).find("option").length == $(this).find("option:selected").length) {
    $(this).parents("#notification_send_form").find("#all_customer").prop("checked",true)
  }
  else{
    $(this).parents("#notification_send_form").find("#all_customer").prop("checked",false)
  }
});
