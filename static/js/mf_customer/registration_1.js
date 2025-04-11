// $("body").on('change','#cust_pan_img', function () {

//     var file_data = $(this)[0].files[0]
//     let fileType = $(this)[0].files[0].type;
//     let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
//     if (validExtensions.includes(fileType)) {
//         let fileReader = new FileReader(); //creating new FileReader object
//         fileReader.onload = () => {
//             let fileURL = fileReader.result;
//         };
//         fileReader.readAsDataURL(file_data);
//     } else {
//         toastr.error("This is not an Image File")
//     }
// });

var email_regex = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/
var phone_regex = /[0-9]{10}/


$("#first_proceed_btn").click(function () {
    acc_type = $("#acc_type").val()
    pan_img = $("#pan_img").val()
    pan_no = $("#pan_no").val()
    var pan_regex = /[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}/
    // if (acc_type != null && pan_img != '' && pan_no = "") {
        
    // }
    if (acc_type == null) {
        toastr.error("Please select Account Type")
    }
    else if (pan_img == "") {
        toastr.error("Please Upload Pancard Image")
        // return false
    }
    else if (pan_regex.test(pan_no) == false) {
        toastr.error("Please Enter valid Pancard No format eg:- ABCDE1234N")
        console.log("2");
        // return false
    }
    else{
        select_attr = $(this)
        select_id = this.id
        toastr.success("Success")
        unlock_cust(select_attr,select_id)
    }
});

$("#registration1_form").submit(function (e) { 
    e.preventDefault();
    select_attr = $(this)
    select_id = this.id
    data = $(this).serializeArray();

    data.push({name: 'acc_type', value: $("#acc_type").val()})
    data.push({name: 'pan_no', value: $("#pan_no").val()})
    password = $("#password").val()
    password1 = $("#password1").val()
    // if (email_regex.test($("#email").val()) == false) {
    //     toastr.error("Please Enter Valid Email Id")
    // }
    if (password == password1) {
        $.ajax({
            type: "post",
            url: "/registration1",
            data: data,
            success: function (response) {
                toastr.success(response.user_id)
                unlock_cust(select_attr,select_id)
                $("#user_id").val(response.user_id)
            },
            error: function (response) {
                // console.log("response",response);
                toastr.error(response.responseJSON.error)
                console.log("error");
            },
        });
    }
    else{
        toastr.error("Create Password and Confirm Password must be same")
    }
    
});