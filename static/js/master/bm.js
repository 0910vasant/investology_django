var t

t = $('#bm_table_data').DataTable( {
  ajax: '/load_bm_data',

  columns: [
      { data: null },
      { data: "PAN_NO" },
      { data: 'LOGIN__EMPLOYEE_CODE' },
      // { data:  null },
      { data:  "NAME" },
      { data:  "LOGIN__USERNAME" },
      { data: 'DOB' },
      { data: 'PHONE' },
      { data: 'MOB_NO' },
      { data: 'EMAIL' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9] },
      // {
      //   targets: [3],
      //       render: function (a, b, data, d) {
      //           let html
      //           html1 = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Name: ${data.NAME}`
      //           html2 = `<br>Username: ${data.LOGIN__USERNAME}</p>`

      //           if (data.LOGIN__USERNAME == null) {
      //               html = html1
      //           } else {
      //               html = html1 + html2
      //           }
      //         return html;
      //       },
      // },
      {
          // puts a button in the last column
        // targets: [1], render: function (a, b, data, d){
        //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
        //   console.log("data.CREATED_DATE",data.CREATED_DATE);
        //   console.log("html",html);
        // return html
        // },
        targets: [9], render: function (a, b, data, d){
            // console.log(d)
            let html
            html1 = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                             <!--<a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
                            <hr class="drop-hr"> -->
                            <a class="dropdown-item" href="/edit_branch_manager/${data.id}"><i class="fa fa-edit"></i> Edit</a>`
            html2 = `<hr class="drop-hr">
                        <a class="dropdown-item open_cl" data-toggle="modal" href="javascript:void(0);" data-id=${data.id} data-target="#loginModal1"><i class="fa fa-user" aria-hidden="true"></i>Create Login</a>`
            
            html3 = `<hr class="drop-hr">
                    <a class="dropdown-item fp" data-toggle="modal" href="javascript:void(0);" data-u_type="bm" data-id=${data.id} data-target="#forgot_password_modal"><i class="fas fa-question" aria-hidden="true"></i>Fogot Password</a>`

            html4 = `</div>
                </div>`
            if (data.CREATE_LOGIN == false) {
                html = html1 + html2 + html4
            }
            else{
                html = html1 + html3 + html4
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
    $("#user_id").val(user_id)
});



$('#loginModal1').on('hidden.bs.modal', function (e) {
    $(".create_login").trigger("reset")
})


$("#add_branch_manager_form").on("submit", function (e) {
    e.preventDefault();
    data = $(this).serializeArray()
    $.ajax({
      type: "post",
      url: "/add_branch_manager",
      data: data,
      success: function (response) {
        toastr.success(response.message);
        window.location.href="/branch_manager_master"
      },
      error: function (response) {
        toastr.error(response.responseJSON.error);
      },
    });
  });

$("#edit_branch_manager_form").on("submit", function (e) {
    // console.log("enter ediy");
    e.preventDefault();
    id = $("#edit_id").val()
    data = $(this).serializeArray()
    $.ajax({
        type: "post",
        url: `/edit_branch_manager/${id}`,
        data: data,
        success: function (response) {
            toastr.success(response.message);
            window.location.href="/branch_manager_master"
        },
        error: function (response) {
            toastr.error(response.responseJSON.error);
        },
    });
});