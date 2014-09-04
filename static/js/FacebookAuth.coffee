login_url = settings.LOGIN_URL

FBLogin = ()->
    window.top.location.href = login_url 
    return
getUserProfile = (callback)->
    FB.getLoginStatus (resp)->
        console.log resp
        if resp.status is "connected"
            FB.api "/v2.1/me", (response)->
                if response and !response.error
                    callback response
                else
                    console.log "error"
                    console.log response
                    return
        else
            window.top.location.href = login_url
        return

postUserProfile = (data)->
    $.ajax
        url: "/accounts/fbuser/"
        method: "GET"
        data: data
    .done ->
        console.log  "done"
        window.top.location.href = settings.DOMAIN_NAME
        return
    .fail ->
        console.log "fail"
        return
