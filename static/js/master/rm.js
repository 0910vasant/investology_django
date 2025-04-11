var t

t = $('#rm_table_data').DataTable( {
  ajax: '/load_rm_data',

  columns: [
      { data: null },
      { data: 'BRANCH__NAME' },
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
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9,10] },
    //   {
    //     targets: [3],
    //         render: function (a, b, data, d) {
    //             let html
    //             html1 = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Name: ${data.NAME}`
    //             html2 = `<br>Username: ${data.LOGIN__USERNAME}</p>`

    //             if (data.LOGIN__USERNAME == null) {
    //                 html = html1
    //             } else {
    //                 html = html1 + html2
    //             }
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
        targets: [10], render: function (a, b, data, d){
            // console.log(d)
        html1 = `<div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Action
                    </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <!-- <a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal" href="#"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
                        <hr class="drop-hr"> -->
                        <a class="dropdown-item" href="/edit_relationship_manager/${data.id}"><i class="fa fa-edit"></i> Edit</a>`
        html2 = `<hr class="drop-hr">
                    <a class="dropdown-item open_cl" data-toggle="modal" href="javascript:void(0);" data-id=${data.id} data-target="#loginModal2"><i class="fa fa-user" aria-hidden="true"></i>Create Login</a>`
        html3 = `</div>
                </div>`
        html4 = `<hr class="drop-hr">
            <a class="dropdown-item fp" data-toggle="modal" href="javascript:void(0);" data-u_type="rm" data-id=${data.id} data-target="#forgot_password_modal"><i class="fas fa-question" aria-hidden="true"></i>Fogot Password</a>`

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
    $("#user_id").val(user_id)
});

$('#loginModal2').on('hidden.bs.modal', function (e) {
    $(".create_login").trigger("reset")
})

$("#add_rm_form").on("submit", function (e) {
    e.preventDefault();
    data = $(this).serializeArray()
    $.ajax({
      type: "post",
      url: "/add_relationship_manager",
      data: data,
      success: function (response) {
        toastr.success(response.message);
        window.location.href="/relationship_manager_master"
      },
      error: function (response) {
        toastr.error(response.responseJSON.error);
      },
    });
});

$("#edit_rm_form").on("submit", function (e) {
    // console.log("enter ediy");
    e.preventDefault();
    id = $("#edit_id").val()
    data = $(this).serializeArray()
    $.ajax({
        type: "post",
        url: `/edit_relationship_manager/${id}`,
        data: data,
        success: function (response) {
            toastr.success(response.message);
            window.location.href="/relationship_manager_master"
        },
        error: function (response) {
            toastr.error(response.responseJSON.error);
        },
    });
});
