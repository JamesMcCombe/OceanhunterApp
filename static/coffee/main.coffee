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
    $('body').on 'mouseover', '[data-action]', (e) ->
      elm = $ e.target
      title = elm.data 'title'
      if title?
        title_wrap = elm.closest('.reveal-modal').find('h2')
        title_wrap.text title
    .on 'mouseout', '[data-action]', (e) ->
      elm = $ e.target
      title_wrap = elm.closest('.reveal-modal').find('h2')
      title = title_wrap.data 'title-origin'
      title_wrap.text title

  bindRevealBlur: ->
    $('body').on 'open.fndtn.reveal', '.oc-reveal-modal-blur', (e) ->
      $('.page-wrap').addClass 'blur'
    $('body').on 'close.fndtn.reveal', '.oc-reveal-modal-blur', (e) ->
      $('.page-wrap').removeClass 'blur'

$ ->
  window.oh = new OceanHunter
  oh.reAdjustFixedBottom()
  oh._showFixedBottom()
