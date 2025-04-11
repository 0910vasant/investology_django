$("#sip_calculator").submit(function (e) { 
    e.preventDefault();
    let data = $(this).serializeArray()
    sip_calculator(data)
});

$(document).ready(function () {
    data = $("#sip_calculator").serializeArray()
    sip_calculator(data)
});

function sip_calculator(data) { 
    $.ajax({
        url: "/sip_calc",
        data: data,
        success: function (response) {
            $("#invested_amt").val(response.invest_amt)
            $("#est_return").val(response.est_return)
            $("#expected_amt").val(response.futureValue)
        },
        error: function (response) {
            toastr.success("Something went wrong")
        }
    });
}

