console.log("entre Profile");

$("#edit_profile").click(function () {
    // user_id = $(this).user("id")
    // user_type = $(this).user("type")
    user_id = $(this).attr("user-id")
    user_type = $(this).attr("user-type")

    if (user_type == "bm") {
        url = `/edit_branch_manager/${user_id}`
    }
    else if (user_type == "rm"){
        url = `/edit_relationship_manager/${user_id}`
    }
    else{
        url = `/edit_ep/${user_id}`
    }

    window.location.href = url
    // console.log("user_id",user_id);
    // console.log("user_type",user_type);
});