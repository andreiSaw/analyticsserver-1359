$("#login-button").click(function (event) {
    event.preventDefault();
    var form = $('form');
    var username = $("#username-input").val();
    var password = $("#password-input").val();
    if (username == "admin" && password == "admin") {

        form.fadeOut();
        $('.wrapper').addClass('form-success');
        setTimeout(function () {
            window.location.replace('/main');
        }, 4000);
    }
    else {
        form.effect("shake");
    }
});