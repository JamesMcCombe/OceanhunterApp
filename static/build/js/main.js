var OceanHunter;

OceanHunter = (function() {
  function OceanHunter() {
    this.removeMobileHover();
    $('input, textarea').placeholder();
    FastClick.attach(document.body);
    $(document).foundation();
    this.bindRevealAction();
    this.bindRevealBlur();
  }

  OceanHunter.prototype.reAdjustFixedBottom = function() {
    return $('body').css('padding-bottom', function() {
      return $('.fixed-to-bottom-wrapper').height();
    });
  };

  OceanHunter.prototype._showFixedBottom = function() {
    return $('.fixed-to-bottom-wrapper').css('opacity', 1);
  };

  OceanHunter.prototype.bindRevealAction = function() {
    return $(document).on('mouseenter', '[data-action]', function(e) {
      var elm, title, title_wrap;
      elm = $(e.target);
      title = elm.data('title');
      if (title != null) {
        title_wrap = elm.closest('.reveal-modal').find('h2');
        return title_wrap.text(title);
      }
    }).on('mouseleave', '[data-action]', function(e) {
      var elm, title, title_wrap;
      elm = $(e.target);
      title_wrap = elm.closest('.reveal-modal').find('h2');
      title = title_wrap.data('title-origin');
      return title_wrap.text(title);
    });
  };

  OceanHunter.prototype.bindRevealBlur = function() {
    $(document).on('open.fndtn.reveal', '.oc-reveal-modal-blur', function(e) {
      return $('.page-wrap').addClass('blur');
    });
    return $(document).on('close.fndtn.reveal', '.oc-reveal-modal-blur', function(e) {
      return $('.page-wrap').removeClass('blur');
    });
  };

  OceanHunter.prototype.isSmallScreen = function() {
    return $(window).width() <= 640;
  };

  OceanHunter.prototype.isHighDensity = function() {
    if (window.matchMedia != null) {
      return window.matchMedia('only screen and (min-resolution: 124dpi), only screen and (min-resolution: 1.3dppx), only screen and (min-resolution: 48.8dpcm)').matches || window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 1.3), only screen and (-o-min-device-pixel-ratio: 2.6/2), only screen and (min--moz-device-pixel-ratio: 1.3), only screen and (min-device-pixel-ratio: 1.3)').matches;
    } else if (window.devicePixelRatio != null) {
      return window.devicePixelRatio > 1.3;
    }
  };

  OceanHunter.prototype.checkLoginAndAlert = function() {
    if (!OC.user.logined) {
      $('#loginAlertModal').foundation('reveal', 'open');
    }
    return OC.user.logined;
  };

  OceanHunter.prototype.removeMobileHover = function() {
    var idx, idxs, ignore, rule, stylesheet, _i, _j, _len, _len1, _ref, _ref1, _results;
    if ('createTouch' in document) {
      ignore = /:hover\b/;
      try {
        _ref = document.styleSheets;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          stylesheet = _ref[_i];
          idxs = [];
          _ref1 = stylesheet.cssRules;
          for (idx = _j = 0, _len1 = _ref1.length; _j < _len1; idx = ++_j) {
            rule = _ref1[idx];
            if (rule.type === CSSRule.STYLE_RULE && ignore.test(rule.selectorText)) {
              idxs.unshift(idx);
            }
          }
          _results.push((function() {
            var _k, _len2, _results1;
            _results1 = [];
            for (_k = 0, _len2 = idxs.length; _k < _len2; _k++) {
              idx = idxs[_k];
              _results1.push(stylesheet.deleteRule(idx));
            }
            return _results1;
          })());
        }
        return _results;
      } catch (_error) {}
    }
  };

  return OceanHunter;

})();

$(function() {
  window.oh = new OceanHunter;
  oh.reAdjustFixedBottom();
  oh._showFixedBottom();
  return $('.fixed-to-bottom-wrapper').imagesLoaded(oh.reAdjustFixedBottom);
});

//# sourceMappingURL=main.js.map
