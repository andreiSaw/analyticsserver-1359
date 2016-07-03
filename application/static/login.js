$("#login-button").click(function (event) {
    var username = ('.username-input').val();
    var password = ('.password-input').val();
    if (username == "admin" && password == "admin") {
        event.preventDefault();
        $('form').fadeOut(500);
        $('.wrapper').addClass('form-success');
        setTimeout(function () {
            window.location.replace('/main');
        }, 5000);
    }
});