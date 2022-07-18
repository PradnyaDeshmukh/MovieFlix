$("form[name=signup_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=login_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});


$("form[name=contact_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/forget_pass/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            $error.text("Email sent").removeClass("error--hidden");
            window.location.href = "/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});


$("form[name=reset_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/reset_pass/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=update_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/update_profile/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            document.getElementById('exampleModal').style.display='none';
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});