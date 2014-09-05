window.fbAsyncInit = function() {
    FB.init({
        version: 'v2.1',
        appId: settings.APP_ID,
        status: true,
        xfbml: true,
        cookie: true
    });
    FB.Event.subscribe('auth.authResponseChange', auth_response_change_callback);
    FB.Event.subscribe('auth.statusChange', auth_status_change_callback);

    var auth_response_change_callback = function(response) {
        console.log("auth_response_change_callback");
        console.log(response);
    };
    var auth_status_change_callback = function(response) {
        console.log("auth_status_change_callback: " + response.status);
    };
};

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
