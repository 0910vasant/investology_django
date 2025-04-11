// let t_invest = 500000
// mw = 1000 //monthly withdraw
// month = 12
// year = 1 * month
// ri = 10 // Expected Return Rate(Rate Of Intrest)

// swp_calc

// for (let i = 0; i < year; i++) {
//     t_invest = t_invest - mw
//     window.t_invest = t_invest
//     intrest_amt = Math.round((t_invest) * ri /(100 * month))
//     t_invest = intrest_amt + t_invest
//     // console.log("intrest_amt",intrest_amt,"total_invest",Math.round(t_invest));
// }

$("#swp_calculator").submit(function (e) { 
    e.preventDefault();
    let data = $(this).serializeArray()
    swp_calculator(data)
});

$(document).ready(function () {
    data = $("#swp_calculator").serializeArray()
    swp_calculator(data)
});

function swp_calculator(data) { 
    $.ajax({
        url: "/swp_calc",
        data: data,
        success: function (response) {
            $("#invested_amt").val(response.invest_amt)
            $("#withdraw_amt").val(response.withdraw_amt)
            $("#interest_amt").val(response.total_interest)
            $("#expected_amt").val(response.futureValue)
        },
        error: function (response) {
            toastr.success("Something went wrong")
        }
    });
}


