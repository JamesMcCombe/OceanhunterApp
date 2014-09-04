settings = 
	APP_ID: 1492664544305345
	DOMAIN_NAME: "http://oceanhunter.node.co.nz"
	LOGIIN_CALLBACK_URL: "/fbcb"
	
settings.LOGIN_URL = "https://www.facebook.com/v2.0/dialog/oauth?client_id=" + settings.APP_ID + "&scope=publish_actions,user_friends&redirect_uri=" + settings.DOMAIN_NAME + settings.LOGIIN_CALLBACK_URL;
