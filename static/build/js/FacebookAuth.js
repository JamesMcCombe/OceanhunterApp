var FBLogin, getUserProfile, login_url, postUserProfile;

login_url = settings.LOGIN_URL;

FBLogin = function() {
  window.top.location.href = login_url;
};

getUserProfile = function(callback) {
  return FB.getLoginStatus(function(resp) {
    console.log(resp);
    if (resp.status === "connected") {
      FB.api("/v2.1/me", function(response) {
        if (response && !response.error) {
          return callback(response);
        } else {
          console.log("error");
          console.log(response);
        }
      });
    } else {
      window.top.location.href = login_url;
    }
  });
};

postUserProfile = function(data) {
  return $.ajax({
    url: "/accounts/fbuser/",
    method: "GET",
    data: data
  }).done(function() {
    console.log("done");
    window.top.location.href = settings.DOMAIN_NAME;
  }).fail(function() {
    console.log("fail");
  });
};

//# sourceMappingURL=FacebookAuth.js.map
