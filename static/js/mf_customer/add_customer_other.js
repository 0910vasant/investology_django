// $(".acc_occupation").change(function () { 
//     text = $(this).find(":selected").text()
//     if (text == "Others") {
//         // a = $(this).parent().siblings(".other_country_div").show(100)
//         a = $(this).parents(".col-md-4").siblings(".other_occ_div").show(300)
//     }
//     else{
//         a = $(this).parents(".col-md-4").siblings(".other_occ_div").hide(300)
//     }
// });

function clone_nominee_form() {
    console.log("enter clone");
    from_length = $(".clone_nominee").length
    // console.log("from_length",from_length);
    html = `<div class="row_card row clone_nominee">
                <div class="col-12 col-md-12 col-lg-12">
                    <h4>Nominee - ${from_length + 1} </h4>
                </div>
                <div class="col-md-4 col-lg-4 mt-5">
                    <div class="form-group">
                        <label>Nominee Name <small class="text-danger">*</small></label>
                        <input type="text" id="nominee_name" name="nominee_name" class="form-control" placeholder="Nominee Name" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4 mt-5">
                    <div class="form-group">
                        <label>Nominee DOB <small class="text-danger">*</small></label>
                        <input type="date" id="nominee_dob" name="nominee_dob" class="form-control" placeholder="Nominee DOB" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4 mt-5">
                    <div class="form-group">
                        <label>Relation With Client <small class="text-danger">*</small></label>
                        <input type="text" id="relationship_with_client" name="relationship_with_client" class="form-control" placeholder="Relation With Client" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Nominee Pan No(Optional)</label>
                        <input type="text" id="nominee_pan" name="nominee_pan" class="form-control" placeholder="Nominee Pan No" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>If Nominee is a Minor <small class="text-danger">*</small></label>
                        <select id="nominee_is_minor" name="nominee_is_minor" class="form-control" required>
                            <option value="" selected disable>Select If Nominee is a Minor</option>
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Guardian's Name <small class="text-danger">*</small></label>
                        <input type="text" id="guardian_name" name="guardian_name" class="form-control" placeholder="Guardian's Name" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Guardian's Relation <small class="text-danger">*</small></label>
                        <input id="guardian_relation" name="guardian_relation" type="text" class="form-control" placeholder="Guardian's Relation" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Guardian's DOB <small class="text-danger">*</small></label>
                        <input type="date" id="guardian_dob" name="guardian_dob" class="form-control" placeholder="Guardian's DOB" value="" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Nominee Percentage <small class="text-danger">*</small></label>
                        <input type="text" id="nominee_percentage" name="nominee_percentage" class="form-control" placeholder="Nominee Percentage" value="" required>
                    </div>
                </div>
                <div class="col-lg-10 col-md-10">
                    <div class="form-group">
                    </div>
                </div>
                <div class="col-lg-2 col-md-2" align="right">
                    <div class="form-group">
                        <a class="add_minus remove_nominee_form" id="remove_nominee_form"  href="javascript:void(0)">
                            <i class="bx bx-minus"></i> 
                        </a>
                    </div>
                </div>
                
            </div>`

    if (from_length < 3) {
        $(".clone_nominee_form").append(html)
        // console.log("entere",from_length);
        if (from_length == 2) {
        $("#add_nominee_form").hide()
        toastr.info("Cannot Add more than 3 Nominee")
        }
    }
 }

$("body").on('click','.remove_nominee_form', function () {
    $(this).parent().parent().parent().remove()
    $("#add_nominee_form").show()
});


function clone_tax_dtl_form() {
    from_length = $(".clone_tax_detail").length
    html = `<div class="row_card row clone_tax_detail">
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Tax Details Country <small class="text-danger">*</small></label>
                        <select class="form-control country select2 tax_countries"id="tax_countries" name="tax_countries" required>
                        </select>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4 other_country_div" style="display: none;">
                    <div class="form-group">
                        <label>Other Tax Country <small class="text-danger">*</small></label>
                        <input type="text" class="form-control " placeholder="Other Country" value="" id="other_tax_country" name="other_tax_country">
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Tax Reference Number</label>
                        <input type="text" class="form-control" placeholder="Tax Reference Number" value="" id="tax_reference_number" name="tax_reference_number" required>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4">
                    <div class="form-group">
                        <label>Identification Type <small class="text-danger">*</small></label>
                        <select id="identification_type" name="identification_type" class="form-control identification_type id_type select2" required>
                        </select>
                    </div>
                </div>
                <div class="col-md-4 col-lg-4 other_identification_type_div" style="display: none;">
                    <div class="form-group">
                        <label>Other Identification Type <small class="text-danger">*</small></label>
                        <input type="text" class="form-control" placeholder="Other Identification Type" value="" id="other_identification_type" name="other_identification_type">
                    </div>
                </div>
                <div class="col-lg-10 col-md-10">
                    <div class="form-group">
                    </div>
                </div>
                <div class="col-lg-2 col-md-2">
                    <div class="row justify-content-end">
                        <div class="form-group mr-2">
                            <a class="add_plus add_tax_dtl_form" id="" href="javascript:void(0)" onclick="clone_tax_dtl_form();">
                                <i class="bx bx-plus"></i> 
                            </a>
                        </div>
                        <div class="form-group">
                            <a class="add_minus remove_tax_dtl_form" href="javascript:void(0)">
                                <i class="bx bx-minus"></i> 
                            </a>
                        </div>
                    </div>
                </div>
            </div>`

    if (from_length < 10) {
        $(".tax_details").append(html)
        trigger_select()
        l_c = "last"
        id_type = "last"
        load_country(l_c)
        load_identification_type(id_type)
        // console.log("entere",from_length);
        if (from_length == 9) {
        $(".add_tax_dtl_form").hide()
        toastr.info("Cannot Add more than 10 tax Details")
        }
    }
 }

$("body").on('click','.remove_tax_dtl_form', function () {
    // $(this).parent().parent().parent().remove()
    $(this).parents(".clone_tax_detail").remove()
    $(".add_tax_dtl_form").show()
});

// $(".disable-select").click(function () { 
//    toastr.info("Please Submit Previous Form then Unlock it")
// });

// $(".proceed_btn,#first_proceed_btn").click(function () {
//     id = this.id
//     $(this).prop('disabled', true).hide()
//     if (id == "first_proceed_btn"){
//         $(".accordion-section .first_card").removeClass("disable-select")
//         $("#collapseOne").addClass("show");
//         $(".first_card").children().first().find(".fa-lock").addClass('fa-lock-open').removeClass('fa-lock');
//     }
//     else{
//         $(this).prop('disabled', true).hide()
//         accordion = $(this).parents(".card")
//         a = accordion.next().find(".fa-lock").addClass('fa-lock-open').removeClass('fa-lock');
//         show = accordion.next().removeClass("disable-select").find(".collapse").addClass('show')
//         remove_show = accordion.find(".collapse").removeClass('show');

//     }
// });

function unlock_cust(select_attr,select_id) {
    console.log("selected",select_attr);
    console.log("idd",select_id);
    
    if (select_id == "first_proceed_btn"){
        select_attr.prop('disabled', true).hide()
        $(".accordion-section .first_card").removeClass("disable-select")
        $("#collapseOne").addClass("show");
        $(".first_card").children().first().find(".fa-lock").addClass('fa-lock-open').removeClass('fa-lock');
    }
    else{
        // select_attr.prop('disabled', true).hide()
        select_attr.children().find(".proceed_btn").prop('disabled', true).hide()
        accordion = select_attr.parents(".card")
        a = accordion.next().find(".fa-lock").addClass('fa-lock-open').removeClass('fa-lock');
        show = accordion.next().removeClass("disable-select").find(".collapse").addClass('show')
        remove_show = accordion.find(".collapse").removeClass('show');

    }
}