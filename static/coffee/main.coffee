class OceanHunter
  constructor: ->
    $('input, textarea').placeholder()
    FastClick.attach(document.body)
    $(document).foundation()

    @bindRevealAction()
    @bindRevealBlur()

  # after you change the content in the fixed-to-bottom-wrapper,
  # you have to call this again
  reAdjustFixedBottom: ->
    $('body').css 'padding-bottom', ->
      $('.fixed-to-bottom-wrapper').height()

  _showFixedBottom: ->
    $('.fixed-to-bottom-wrapper')
      .css 'opacity', 1

  bindRevealAction: ->
    $(document).on 'mouseenter', '[data-action]', (e) ->
      elm = $ e.target
      title = elm.data 'title'
      if title?
        title_wrap = elm.closest('.reveal-modal').find('h2')
        title_wrap.text title
    .on 'mouseleave', '[data-action]', (e) ->
      elm = $ e.target
      title_wrap = elm.closest('.reveal-modal').find('h2')
      title = title_wrap.data 'title-origin'
      title_wrap.text title

  bindRevealBlur: ->
    $(document).on 'open.fndtn.reveal', '.oc-reveal-modal-blur', (e) ->
      $('.page-wrap').addClass 'blur'
    $(document).on 'close.fndtn.reveal', '.oc-reveal-modal-blur', (e) ->
      $('.page-wrap').removeClass 'blur'

  isSmallScreen: ->
    $(window).width() <= 640

  isHighDensity: ->
    if window.matchMedia?
      window.matchMedia('only screen and (min-resolution: 124dpi), only screen and (min-resolution: 1.3dppx), only screen and (min-resolution: 48.8dpcm)').matches \
      or window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 1.3), only screen and (-o-min-device-pixel-ratio: 2.6/2), only screen and (min--moz-device-pixel-ratio: 1.3), only screen and (min-device-pixel-ratio: 1.3)').matches
    else if window.devicePixelRatio?
      window.devicePixelRatio > 1.3

  # check if user logined, if not reveal the alert ask user to signup or login
  checkLoginAndAlert: ->
    if not OC.user.logined
      $('#loginAlertModal').foundation('reveal', 'open')
    OC.user.logined

$ ->
  window.oh = new OceanHunter
  oh.reAdjustFixedBottom()
  oh._showFixedBottom()
