$("#registration6_form").submit(function (e) { 
		e.preventDefault();
		select_attr = $(this)
		select_id = this.id
		data = new FormData(this)
		data.append("user_id", $("#user_id").val());

		for(let[key,value] of data){
			console.log("from_data",`${key}`,`${value}`);
		}
		trc = $("#tax_resident_of_any_other_country option:selected").text();
		nominee_or_not = $("input[name='want_nominee']:checked").val();
		if(nominee_or_not == "yes"){
			nominee_data = []
			$.each($(".clone_nominee"), function (i, v) {
					nominee_data.push({
						'nominee_name': $(v).children().find("#nominee_name").val(),
						'nominee_dob': $(v).children().find("#nominee_dob").val(),
						'relationship_with_client': $(v).children().find("#relationship_with_client").val(),
						'nominee_pan': $(v).children().find("#nominee_pan").val(),
						'nominee_is_minor': $(v).children().find("#nominee_is_minor").val(),
						'guardian_name': $(v).children().find("#guardian_name").val(),
						'guardian_relation': $(v).children().find("#guardian_relation").val(),
						'guardian_dob': $(v).children().find("#guardian_dob").val(),
						'nominee_percentage': $(v).children().find("#nominee_percentage").val(),
					})
			});
			data.append("nominees", JSON.stringify(nominee_data));
		}
		if (trc == "Yes") {
			temp = []
			$.each($(".clone_tax_detail"), function (i, v) {
					let other_country = $(v).children().find(".other_tax_country").val()
					let oit = $(v).children().find(".other_identification_type").val()
					if (other_country == undefined) {
							other_country = None
					}
					if (other_identification_type == undefined) {
							other_identification_type = None
					}
					// temp.push(JSON.parse(JSON.stringify{
					// temp = JSON.parse(JSON.stringify(temp))
					temp.push({
							'country': $(v).children().find(".tax_countries").val(),
							'other_country': other_country,
							'tax_reference_number':$(v).children().find("#tax_reference_number").val(),
							'identification_type':$(v).children().find(".identification_type").val(),
							'other_identification_type': other_identification_type
					})
			});
			data.append("tax_countries", JSON.stringify(temp));
			console.log("tempdata",temp)
		} else {
				console.log("else");
		}
		$.ajax({
		    type: "post",
		    url: "/registration6",
		    data: data,
		    processData: false,
		    contentType: false,
		    enctype: 'multipart/form-data',
		    success: function (response) {
		        toastr.success(response)
		        unlock_cust(select_attr,select_id)
		        // $("#user_id").val(response.user_id)
		    },
		    error: function (response) {
		        // console.log("response",response);
		        toastr.error(response.responseJSON.error)
		        console.log("error");
		    },
		});
});



$("#country_of_birth").change(function () { 
		text = $(this).find(":selected").text()
		if (text == "Others") {
				// a = $(this).parent().siblings(".other_country_div").show(100)
				a = $(this).parents(".col-md-4").siblings(".other_birth_c_div")
				a.show(300)
				a.children().find("#other_citizenship").prop('required', true)
		}
		else{
				a = $(this).parents(".col-md-4").siblings(".other_birth_c_div")
				a.hide(300)
				a.children().find("#other_citizenship").prop('required', false)
		}
});

$("#citizenship").change(function () { 
		text = $(this).find(":selected").text()
		if (text == "Others") {
				// a = $(this).parent().siblings(".other_country_div").show(100)
				a = $(this).parents(".col-md-4").siblings(".other_citizenship_div")
				a.show(300)
				a.children().find("#other_citizenship").prop('required', true)
		}
		else{
				a = $(this).parents(".col-md-4").siblings(".other_citizenship_div")
				a.hide(300)
				a.children().find("#other_citizenship").prop('required', false)
		}
});

$("#nationality").change(function () { 
		text = $(this).find(":selected").text()
		if (text == "Others") {
				// a = $(this).parent().siblings(".other_country_div").show(100)
				a = $(this).parents(".col-md-4").siblings(".other_nationality_div")
				a.show(300)
				a.children().find("#other_nationality").prop('required', true)
		}
		else{
				a = $(this).parents(".col-md-4").siblings(".other_nationality_div")
				a.hide(300)
				a.children().find("#other_nationality").prop('required', false)
		}
});

$(".want_nominee").click(function () { 
		check = $("input[name='want_nominee']:checked").val();
		console.log("check",check);
		if (check == "yes") {
				load_nominee_form()
				$(".clone_nominee_form").slideDown(500)
		}
		else{
				$(".clone_nominee_form").slideUp(500)
				$("#add_nominee_form").show(300)
				// $(".remove_nominee_form").parents(".clone_nominee").remove()
				$(".clone_nominee").remove()
		}
});



function load_nominee_form() {
		html = `<div class="row_card row clone_nominee">
								<div class="col-12 col-md-12 col-lg-12">
										<h4>Nominee - 1 </h4>
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
												<a class="add_plus add_nominee_form" id="add_nominee_form" href="javascript:void(0)" onclick="clone_nominee_form();">
														<i class="bx bx-plus"></i> 
														</a>
										</div>
								</div>
						</div>`
		$(".clone_nominee_form").append(html)
}


function load_other_tax_country() {
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
								<div class="col-lg-2 col-md-2" align="right">
										<div class="form-group">
												<a class="add_plus add_tax_dtl_form" id="" href="javascript:void(0)" onclick="clone_tax_dtl_form();">
														<i class="bx bx-plus"></i> 
														</a>
										</div>
								</div>
						</div>`
				$(".tax_details").append(html)
	}

$("body").on("change",".id_type", function () {
		text = $(this).find(":selected").text()
		if (text == "Others") {
				a = $(this).parents(".col-md-4").siblings(".other_identification_type_div")
				a.show(300)
				a.children().find("#other_identification_type").prop('required', true)
		}
		else{
				a = $(this).parents(".col-md-4").siblings(".other_identification_type_div")
				a.hide(300)
				a.children().find("#other_identification_type").prop('required', false)
		}
});

$("body").on("change",".tax_countries", function () {
		text = $(this).find(":selected").text()
		console.log("enter",text);
		if (text == "Others") {
				a = $(this).parents(".col-md-4").siblings(".other_country_div")
				a.show(300)
				a.children().find("#other_tax_country").prop('required', true)
		}
		else{
				a = $(this).parents(".col-md-4").siblings(".other_country_div")
				a.hide(300)
				a.children().find("#other_tax_country").prop('required', false)

		}
});

$("#tax_resident_of_any_other_country").change(function () { 
		value = $(this).find(':selected').val()
		if (value == "yes") {
				load_other_tax_country()
				l_c = "last"
				id_type = "last"
				load_country(l_c)
				load_identification_type(id_type)
				$(".tax_details").slideDown(500)
		}
		else{
				// $(".tax_details").hide(500)
				$(".other_country_div").hide(100)
				$(".other_identification_type_div").hide(200)

				$(".tax_details").slideUp(500)
				$(".clone_tax_detail").remove()
		}
});