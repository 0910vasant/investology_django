// console.log("user_type",user_type);
// console.log("login_id",login_id);
var filter
if (user_type == "bm" || user_type == "rm") {
  filter = "yes"
}
else{
  filter = "no"
}
// $(document).ready(function () {
//   async:false,
  
// });
url = location.pathname

load_user_type()
function load_user_type() {
  temp = [`<option value="" selected disabled>Select User Type</option>`]
  if (user_type != "bm" || user_type != "rm") {
    if (url == "/attendance") {
      temp.push(`<option value="branch_manager">Branch Manager</option>`)
    }
    else{
      temp.push(`<option value="bm">Easy Investology</option>`)
    }
  }
  temp.push(`<option value="rm">Relationship Manager</option>`,`<option value="ep">Easy Partner</option>`)
  $(".u_type").html(temp.join(""));
}
$(".u_type").change(function () {
  // console.log("enter utype");
    ut = $(this).val()
    c = $(this)
    $.ajax({
      url: `/load_user_type`,
      data: {
        "ut":ut,
      },
      async: false,
      success: function (response) {
        // console.log("data",response);
        let html = [`<option value="" selected="" disabled="">Select User</option>`]
        $.each(response, function (i, v) { 
          html.push(`<option value="${v.id}">Name : ${v.NAME} || Username : ${v.USERNAME}</option>`)
        });
        // console.log(c.parents(".row").find(".user"))
        // console.log("htmlhtml",html);
        c.parents(".row").find(".user").html(html.join("")).change()
      }
    });
});


function load_cust(user,user_type) {
	if (user != null) {
		cust_data = [`<option value="" disabled selected>Please Select Customer</option>`];
		$.ajax({
			// url: `/load_leads?user=${user}`,
			url: `/load_lead_cust?user=${user}`,
			data:{
				"user":user,
				"u_type": user_type
			},
			async: false,
			success: function (response) {
				$.each(response.data, function (i, v) {
					cust_data.push(`<option value="${v.id}">${v.C_NAME} || ${v.MOB_NO}</option>`);
				});
				$(".l_data").html(cust_data.join(""));
			},
		});
	}
}


