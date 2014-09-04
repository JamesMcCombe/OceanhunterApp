APP_ID = settings.APP_ID;
FB_SHARE = function() {
    var old_href = window.top.location.href;
    if (navigator.userAgent.match('CriOS')) {
        window.open("https://www.facebook.com/dialog/share?app_id=" + APP_ID + "&display=popup&href=" + encodeURIComponent(old_href) + "&redirect_uri=" + encodeURIComponent(old_href) + settings.OPEN_GRAPH_CALLBACK_URL, "_blank");
    } else {
        FB.ui({
            method: 'share',
            href: old_href
        }, function(response) {
            console.log(response);
        });
    }
};
FB_LIKE = function(id) {
    var obj = JSON.stringify({
        object: id
    });
    if (navigator.userAgent.match('CriOS')) {
        window.location.href = "https://www.facebook.com/dialog/share_open_graph?app_id=" + APP_ID + "&display=popup&action_type=og.likes&action_properties=" + encodeURIComponent(obj) + "&redirect_uri=" + encodeURIComponent(settings.DOMAIN_NAME) + "/liked";
    } else {
        FB.ui({
            method: 'share_open_graph',
            action_type: 'og.likes',
            action_properties: obj
        }, function(response) {
            if (response && !response.error) {
                /* handle the result */
                $.ajax({
                    url: '/toggle_state',
                    type: 'GET',
                    data: {
                        attr: 'liked'
                    }
                })
                    .done(function() {
                        $('.like-icon span').toggleClass('icon-thumbs-up').toggleClass('icon-checkmark');
                        $('.like-icon').toggleClass('fblike');
                    });
            }
        });
    }
};
FB_GET_FRIENDS = function(callback) {
    FB.api('me/friends?limit=5000',
        function(response) {
            callback(JSON.stringify(response.data));
        });
};
