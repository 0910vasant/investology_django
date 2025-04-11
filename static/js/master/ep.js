var t

t = $('#ep_table_data').DataTable( {
  ajax: '/load_ep_data',

  columns: [
      { data: null },
      
      { data: 'RM__NAME' },
      { data: 'LOGIN__EMPLOYEE_CODE' },
    //   { data:  null },
      { data:  "NAME" },
      { data:  "LOGIN__USERNAME" },
      { data: 'PAN_NO' },
    //   { data: 'NAME' },
      { data: 'DOB' },
      { data: 'PHONE' },
      { data: 'MOB_NO' },
      { data: 'EMAIL' },
      { data: 'BANK_NAME' },
      
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9,10,11] },
    //   {
    //     targets: [3],
    //         render: function (a, b, data, d) {
    //           let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Name: ${data.NAME} <br> Username: ${data.LOGIN__USERNAME}</p>`
    //           return html;
    //         },
    //   },
      {
          // puts a button in the last column
        // targets: [1], render: function (a, b, data, d){
        //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
        //   console.log("data.CREATED_DATE",data.CREATED_DATE);
        //   console.log("html",html);
        // return html
        // },
        targets: [11], render: function (a, b, data, d){
            // console.log(d)
            html1 = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <!--<a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal" href="#"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
                            <hr class="drop-hr">-->
                            <a class="dropdown-item" href="/edit_ep/${data.id}"><i class="fa fa-edit"></i> Edit</a>`
            html2 = `<hr class="drop-hr">
                        <a class="dropdown-item open_cl" data-toggle="modal" href="javascript:void(0);" data-id=${data.id} data-target="#loginModal3"><i class="fa fa-user" aria-hidden="true"></i>Create Login</a>`
            html3 = `</div>
                    </div>`
            html4 = `<hr class="drop-hr">
                <a class="dropdown-item fp" data-toggle="modal" href="javascript:void(0);" data-u_type="ep" data-id=${data.id} data-target="#forgot_password_modal"><i class="fas fa-question" aria-hidden="true"></i>Fogot Password</a>
                <hr class="drop-hr">
                <a class="dropdown-item edit_epcode" data-toggle="modal" href="javascript:void(0);" data-id=${data.LOGIN__id} data-target="#change_epcode_modal"><i class="fa fa-edit" aria-hidden="true"></i>Edit Ep Code</a>`
            if (data.CREATE_LOGIN == false) {
                html = html1 + html2 + html3
            }
            else{
                html = html1 + html4 + html3
            }
            return html
        },
      },
  ],
  } );
  t.on( 'order.dt search.dt', function () {
      t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          // console.log(i,cell)
          cell.innerHTML = i+1;
      } );
  } ).draw();

$("body").on("click",".open_cl", function () {
    user_id = $(this).data("id")
    console.log("dajdjsad",user_id);
    $("#user_id").val(user_id)
});


$('#loginModal3').on('hidden.bs.modal', function (e) {
    $(".create_login").trigger("reset")
})

$("#add_ep_form").on("submit", function (e) {
    e.preventDefault();
    // data = $(this).serializeArray()
    data = new FormData(this)
    $.ajax({
      type: "post",
      url: "/add_ep",
      cache: false,
      processData: false,
      contentType: false,
      enctype: 'multipart/form-data',
      data: data,
      success: function (response) {
        toastr.success(response.message);
        window.location.href="/easy_partner_master"
      },
      error: function (response) {
        toastr.error(response.responseJSON.error);
      },
    });
});

$("#edit_ep_form").on("submit", function (e) {
    // console.log("enter ediy");
    e.preventDefault();
    id = $("#edit_id").val()
    // data = $(this).serializeArray()
    data = new FormData(this)
    $.ajax({
        type: "post",
        url: `/edit_ep/${id}`,
        cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        data: data,
        success: function (response) {
            toastr.success(response.message);
            window.location.href="/easy_partner_master"
        },
        error: function (response) {
            toastr.error(response.responseJSON.error);
        },
    });
});


$("body").on("click",".edit_epcode", function () {
  let id = $(this).data("id")
  // console.log("entered",id);
  $("#change_epcode_form").prop("action",`/edit_user_ep_code/${id}`)
  $.ajax({
      type: "post",
      url: `/get_user_ep_code/${id}`,
      success: function (response) {
        console.log("response",response);
        $("#change_epcode_form #ep_name").val(response.name);
        $("#change_epcode_form #ep_code").val(response.ep_code);
      },
      error: function (response){
          // console.log("error",response);
      }
  });
});

$("#change_epcode_form").on('submit', function (e) {
e.preventDefault()
data = $(this).serializeArray()
url = $(this).attr('action');
$.ajax({
  type: "post",
  url: url,
  data : data ,
  success: function (response) {
    $("#change_epcode_modal").modal("toggle");
    t.ajax.reload(null,false)
    toastr.success(response)
  },
  error: function (response) {
    toastr.error(response.responseJSON)
    console.log("error");
  },
});
});