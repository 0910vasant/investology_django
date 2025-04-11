

$("#pan_img,#second_pan_img,#third_pan_img").change(function (e) {
    
    e.preventDefault();
    var formData = new FormData();

    id = this.id
    console.log("id",id);
    if (id == "pan_img") {
        formData.append('pan_img', $('input[name=pan_img]')[0].files[0]);
    }
    if (id == "second_pan_img") {
        formData.append('pan_img', $('input[name=second_pan_img]')[0].files[0]);
    }
    if (id == "third_pan_img") {
        formData.append('pan_img', $('input[name=third_pan_img]')[0].files[0]);
    }

    
    $.ajax({
        type: "post",
        url: "/scan_pan",
        data: formData,
        // cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function (response) {
            if (id == "pan_img") {
                $("#pan_no").val(response.pan_no)
            }
            if (id == "second_pan_img") {
                $("#secondary_pan_holder").val(response.pan_no)
            }
            if (id == "third_pan_img") {
                $("#third_pan_holder").val(response.pan_no)
            }
            
            toastr.success("Please check pan no it is not rigth then edit")
        },
        error: function (response) {
            if (response.status == "412") {
                console.log("response",response);
                toastr.info(response.responseJSON.message)
            }
            else{
                toastr.error(response.responseJSON)
            }
            // console.log("error",response.responseJSON.error);
        },
    });
});