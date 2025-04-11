$("#sip_lumpsum_calculator").submit(function (e) { 
    e.preventDefault();
    let data = $(this).serializeArray()
    sip_lumpsum(data)
});

$(document).ready(function () {
    data = $("#sip_lumpsum_calculator").serializeArray()
    sip_lumpsum(data)
});

function sip_lumpsum(data) { 
    $.ajax({
        url: "/sip_lumpsum_calc",
        data: data,
        success: function (response) {
            // console.log("response",response);
            $("#invested_amt").val(response.invest_amt)
            $("#est_return").val(response.est_return)
            $("#expected_amt").val(response.futureValue)
        },
        error: function (response) {
            toastr.success("Something went wrong")
        }
    });
}
