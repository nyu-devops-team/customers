$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_first_name").val(res.first_name);
        $("#customer_last_name").val(res.last_name);
        $("#customer_email").val(res.email);
        $("#customer_address").val(res.address);
        if (res.active == true) {
            $("#customer_active").val("true");
        } else {
            $("#customer_active").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_first_name").val("");
        $("#customer_last_name").val("");
        $("#customer_email").val("");
        $("#customer_address").val("");
        $("#customer_active").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        var first_name = $("#customer_first_name").val();
        var last_name = $("#customer_last_name").val();
        var email = $("#customer_email").val();
        var address = $("#customer_address").val();
        var customer_active = $("#customer_active").val() == "true";

        var data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "active": customer_active
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {
        console.log("ppj")
        var customer_id = $("#customer_id").val();
        var first_name = $("#customer_first_name").val();
        var last_name = $("#customer_last_name").val();
        var email = $("#customer_email").val();
        var address = $("#customer_address").val();
        var customer_active = $("#customer_active").val() == "true";

        var data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "active": customer_active
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Suspend a Customer
    // ****************************************

    $("#suspend-btn").click(function () {
        var customer_id = $("#customer_id").val();


        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id + "/suspend",
                contentType: "application/json"
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("You successfully suspended the customer!")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    
    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });
    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {
        var queryString = ""

        var first_name = $("#customer_first_name").val();
        var last_name = $("#customer_last_name").val();
        var email = $("#customer_email").val();
        var address = $("#customer_address").val();
        var customer_active = $("#customer_active").val() == "true";

        if (first_name) {
            queryString = "first_name=" + first_name;
        } else if (last_name) {
            queryString = "last_name=" + last_name;
        } else if (email) {
            queryString = "email=" + email;
        } else if (address) {
            queryString = "address=" + address;
        } else if (customer_active) {
            queryString = "active=" + customer_active;
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:15%">First Name</th>'
            header += '<th style="width:15%">Last Name</th>'
            header += '<th style="width:20%">Email</th>'
            header += '<th style="width:30%">Address</th>'
            header += '<th style="width:10%">Active</th></tr>'
            $("#search_results").append(header);
            var firstCustomer = "";
            for (var i = 0; i < res.length; i++) {
                var customer = res[i];
                var row = "<tr><td>" + customer.id + "</td><td>" + customer.first_name +
                    "</td><td>" + customer.last_name + "</td><td>" + customer.email +
                    "</td><td>" + customer.address + "</td><td>" + customer.active + "</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            $("#search_results").append('</table>');
            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });


})
