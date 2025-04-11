$(document).ready(function () {
    tabacoo_user()
    alcohol_user()
    medical_history()
});

$(".tobacco_user").change(function () {
    tabacoo_user()
});

function tabacoo_user() {
    t_user = $("input[name='tobacco_user']:checked").val();

    html = `<div class="col-md-4 col-lg-4 t_user">
                <div class="form-group">
                    <label>Please Provide Quantity<small class="text-danger">*</small></label>
                    <input type="text" class="form-control" id="tobacco_qty" name="tobacco_qty" placeholder="Please Provide Quantity" value="" required>
                </div>
            </div>
            <div class="col-md-4 col-lg-4 t_user">
                <div class="form-group">
                    <label>How many do you consuming<small class="text-danger">*</small></label>
                    <input type="text" class="form-control" id="tobacco_consume" name="tobacco_consume" placeholder="how many do you consuming" value="" required>
                </div>
            </div>`

    if (t_user == "yes") {
        $(".tobacco_user_div").after(html)
    } else {
        $(".t_user").remove()
    }
}

$(".alcohol_user").change(function () {
    alcohol_user()
});

function alcohol_user() {
    a_user = $("input[name='alcohol_user']:checked").val();

    html = `<div class="col-md-4 col-lg-4 a_user">
                <div class="form-group">
                    <label>Please Provide Quantity<small class="text-danger">*</small></label>
                    <input type="text" class="form-control" id="alcohol_qty" name="alcohol_qty" placeholder="Please Provide Quantity" value="" required>
                </div>
            </div>
            <div class="col-md-4 col-lg-4 a_user">
                <div class="form-group">
                    <label>How many do you consuming<small class="text-danger">*</small></label>
                    <input type="text" class="form-control" id="alcohol_consume" name="alcohol_consume" placeholder="how many do you consuming" value="" required>
                </div>
            </div>`

    if (a_user == "yes") {
        $(".alcohol_user_div").after(html)
    } else {
        $(".a_user").remove()
    }
}

$(".medical_history").change(function () {
    medical_history()
});

function medical_history() {
    m_user = $("input[name='medical_history']:checked").val();

    html = `<div class="col-md-4 col-lg-4 m_user">
                <div class="form-group">
                    <label>Please Provide Details<small class="text-danger">*</small></label>
                    <input type="text" class="form-control" id="medical_dtl" name="medical_dtl" placeholder="Please Provide Details" value="" required>
                </div>
            </div>`

    if (m_user == "yes") {
        $(".medical_history_div").after(html)
    } else {
        $(".m_user").remove()
    }
}

$("#add_customer").on("submit", function (e) {
    e.preventDefault();
    data = new FormData(this);
    // for(let[key,value] of data){
    //     console.log("from_data",`${key}`,`${value}`);
    // }
    $.ajax({
      type: "post",
      url: "/add_customer",
      cache: false,
      processData: false,
      contentType: false,
      enctype: "multipart/form-data",
      data: data,
      success: function (response) {
        toastr.success(response.message);
        window.location.href="/customer"
      },
      error: function (response) {
        toastr.error(response.responseJSON.error);
      },
    });
  });


