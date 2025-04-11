var t

t = $('#meeting_table').DataTable( {
  ajax: '/load_meetings',
  columns: [
      { data: null },
      { data: "RM_EP__NAME" },
      { data: "RM_EP__USERNAME" },
      { data: null },
      { data: null },
      { data: null },
      { data: null },
      { data: 'REMARK' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8] },
      // {
      //   targets: [1],
      //       render: function (a, b, data, d) {
      //         // let date = new Date(Date)
      //         let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Username: ${data.RM_EP__USERNAME} <br> Name: ${data.RM_EP__NAME}</p>`
      //         return html;
      //       },
      // },
      // {
      //   targets: [2],
      //     render: function (a, b, data, d) {
      //       console.log("data.TYPE",data.TYPE);
      //       let html
      //       if (data.TYPE == "lead"){
      //         console.log("enter Lead");
      //         html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Name: ${data.LEADS__C_NAME} <br> Mob No: ${data.LEADS__MOB_NO}</p>`
      //       }
      //       if(data.TYPE == "customer"){
      //         html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Name: ${data.I_CUST__C_NAME} <br> Mob No: ${data.I_CUST__MOB_NO}</p>`
      //       }
      //       // let date = new Date(Date)
            
      //       return html;
      //     },
      // },
      {
          targets: [3],
            render: function (a, b, data, d) {
              // console.log("data.TYPE",data.TYPE);
              let html
              if (data.TYPE == "lead"){
                html = data.LEADS__C_NAME
              }
              if(data.TYPE == "customer"){
                html = data.I_CUST__C_NAME
              }
              // let date = new Date(Date)
              
              return html;
            },
        },
        {
          targets: [4],
            render: function (a, b, data, d) {
              // console.log("data.TYPE",data.TYPE);
              let html
              if (data.TYPE == "lead"){
                html = data.LEADS__MOB_NO
              }
              if(data.TYPE == "customer"){
                html = data.I_CUST__MOB_NO
              }
              // let date = new Date(Date)
              
              return html;
            },
        },
      
      {
        targets: [5], render: function (a, b, data, d){
          // let date = new Date(Date)
          let date = moment(data.DATE).format('DD/MM/YYYY');
          return date
        },
      },
      {
        targets: [6], render: function (a, b, data, d){
          let hours = parseInt(data.TIME.slice(0,2))
          let minutes = parseInt(data.TIME.slice(3,5))
          let ampm = hours >= 12 ? 'PM' : 'AM';
          hours = hours % 12;
          hours = hours ? hours : 12;
          minutes = minutes < 10 ? '0'+minutes : minutes;
          let time = `${hours} : ${minutes} ${ampm}`
          return time
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
        targets: [8], render: function (a, b, data, d){
            // console.log(d)
            html = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_meeting_modal" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
                            <hr class="drop-hr">
                            <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>
                        </div>
                    </div>`
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

$("body").on("click",".delete", function () {
  let id = $(this).data('id')
  $.ajax({
    type: "post",
    url: `/delete_meeting`,
    data:{
    "csrfmiddlewaretoken":$("input[name=csrfmiddlewaretoken]").val(),
    "id": id
    },
    success: function (response) {
    toastr.success(response)
    t.ajax.reload()
    },
    error: function (response){
    toastr.error("something went wrong")
    }
  });
});

$("body").on("click",".edit_modal", function () {
    let id = $(this).data("id")
    console.log("entered",id);
    url = `/get_meeting/${id}`
    $.ajax({
        type: "get",
        url: url,
        success: function (response) {
          console.log("response",response);
          // console.log("response",response[0].NAME);
          let data = response[0]
          $("#edit_meeting_form #id").val(data.id)
          $("#edit_meeting_form #followup_date").val(data.DATE)
          $("#edit_meeting_form #followup_time").val(data.TIME)
          $("#edit_meeting_form #remark").val(data.REMARK)
        },
        error: function (response){
            // console.log("error",response);
        }
    });
});



function load_user() {
  user_html = [`<option value="" disabled selected>Please Select EP/RM Type</option>`]
  

  $.ajax({
    url: "/load_ep_data",
    async:false,
    success: function (response) {
      $.each(response.data, function (i, v) {
        user_html.push(`<option data-user-type="ep" value="${v.id}">${v.NAME} || ${v.PHONE} || ep</option>`)
      });
    }
  });

  $.ajax({
    url: "/load_rm_data",
    async:false,
    success: function (response) {
      $.each(response.data, function (i, v) {
        user_html.push(`<option data-user-type="rm" value="${v.id}">${v.NAME} || ${v.PHONE} || rm</option>`)
      });
    }
  });

  $("#user_t").html(user_html.join(""));
 }

//  load_user()

$(".cust_t,.user,.u_type").change(function (e) {

  let cust_type = $(this).parents(".modal-body").find("#cust_t").val()
  let user = $(this).parents(".modal-body").find("#user").val()
  let u_type = $(this).parents(".modal-body").find("#u_type").val()

  // console.log("cust_type",cust_type);
  // console.log("user",user);
  // console.log("u_type",u_type);
  if (cust_type != "" && cust_type != null  && user != "" && user != null && u_type != "" && u_type != null) {
    console.log("enter If");
    $.ajax({
      type: "get",
      url: `/filter_customer`,
      data: {
        "customer_type":cust_type,
        "user":user,
        "u_type":u_type,
      },
      success: function (response) {
        
        let customer_html = [`<option value="" disabled="" selected="">Please Select Customer</option>`]
        // if (cust_type == "customer_lead"){
        //   $.each(response, function (i, v) { 
        //     customer_html.push(`<option value="${v.id}">${v.NAME} | ${v.MOBILE}</option>`)
        //   });
        // }
  
        if (cust_type == "customer" || cust_type == "lead") {
          $.each(response, function (i, v) {
             customer_html.push(`<option value="${v.id}">${v.C_NAME} | ${v.MOB_NO}</option>`)
          });
        }
        $("#cust").html(customer_html.join(""));
      }
    });
  }
});

$("#add_meeting_form").submit(function (e) {
  e.preventDefault();
  data = $(this).serializeArray()
  // console.log(data)
  $.ajax({
    type: "post",
    url: "/add_meeting",
    data: data,
    success: function (response) {
      toastr.success(response)
      $("#add_meeting").modal("toggle")
      $("#add_meeting_form").trigger("reset")
      $(".select2").val("").change()
      t.ajax.reload()
    },
    error: function (response){
      toastr.error("Something went wrong")
    }
  });
});

$('#add_meeting').on('hidden.bs.modal', function (e) {
  $("#add_meeting_form").trigger("reset")
  $("#add_meeting_form .select2").change()
})


$("#edit_meeting_form").submit(function (e) {
  e.preventDefault();
  data = $(this).serializeArray()
  // console.log(data)
  $.ajax({
    type: "post",
    url: "/edit_meeting",
    data: data,
    success: function (response) {
      toastr.success(response)
      $("#edit_meeting_modal").modal("toggle")
      $("#edit_meeting_form").trigger("reset")
      t.ajax.reload()
    },
    error: function (response){
      toastr.error("Something went wrong")
    }
  });
});