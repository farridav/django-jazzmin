/**
 * --------------------------------------------
 * AdminLTE Layout.js
 * License MIT
 * --------------------------------------------
 */

const Layout = (($) => {
  /**
   * Constants
   * ====================================================
   */

  const NAME               = 'Layout'
  const DATA_KEY           = 'lte.layout'
  const EVENT_KEY          = `.${DATA_KEY}`
  const JQUERY_NO_CONFLICT = $.fn[NAME]

  const Event = {
    SIDEBAR: 'sidebar'
  }

  const Selector = {
    HEADER         : '.main-header',
    MAIN_SIDEBAR   : '.main-sidebar',
    SIDEBAR        : '.main-sidebar .sidebar',
    CONTENT        : '.content-wrapper',
    BRAND          : '.brand-link',
    CONTENT_HEADER : '.content-header',
    WRAPPER        : '.wrapper',
    CONTROL_SIDEBAR: '.control-sidebar',
    CONTROL_SIDEBAR_CONTENT: '.control-sidebar-content',
    CONTROL_SIDEBAR_BTN: '[data-widget="control-sidebar"]',
    LAYOUT_FIXED   : '.layout-fixed',
    FOOTER         : '.main-footer',
    PUSHMENU_BTN   : '[data-widget="pushmenu"]',
    LOGIN_BOX      : '.login-box',
    REGISTER_BOX   : '.register-box'
  }

  const ClassName = {
    HOLD           : 'hold-transition',
    SIDEBAR        : 'main-sidebar',
    CONTENT_FIXED  : 'content-fixed',
    SIDEBAR_FOCUSED: 'sidebar-focused',
    LAYOUT_FIXED   : 'layout-fixed',
    NAVBAR_FIXED   : 'layout-navbar-fixed',
    FOOTER_FIXED   : 'layout-footer-fixed',
    LOGIN_PAGE     : 'login-page',
    REGISTER_PAGE  : 'register-page',
    CONTROL_SIDEBAR_SLIDE_OPEN: 'control-sidebar-slide-open',
    CONTROL_SIDEBAR_OPEN: 'control-sidebar-open',
  }

  const Default = {
    scrollbarTheme : 'os-theme-light',
    scrollbarAutoHide: 'l',
    panelAutoHeight: true,
    loginRegisterAutoHeight: true,
  }

  /**
   * Class Definition
   * ====================================================
   */

  class Layout {
    constructor(element, config) {
      this._config  = config
      this._element = element

      this._init()
    }

    // Public

    fixLayoutHeight(extra = null) {
      let control_sidebar = 0

      if ($('body').hasClass(ClassName.CONTROL_SIDEBAR_SLIDE_OPEN) || $('body').hasClass(ClassName.CONTROL_SIDEBAR_OPEN) || extra == 'control_sidebar') {
        control_sidebar = $(Selector.CONTROL_SIDEBAR_CONTENT).height()
      }

      const heights = {
        window: $(window).height(),
        header: $(Selector.HEADER).length !== 0 ? $(Selector.HEADER).outerHeight() : 0,
        footer: $(Selector.FOOTER).length !== 0 ? $(Selector.FOOTER).outerHeight() : 0,
        sidebar: $(Selector.SIDEBAR).length !== 0 ? $(Selector.SIDEBAR).height() : 0,
        control_sidebar: control_sidebar,
      }

      const max = this._max(heights)
      let offset = this._config.panelAutoHeight

      if (offset === true) {
        offset = 0;
      }

      if (offset !== false) {
        if (max == heights.control_sidebar) {
          $(Selector.CONTENT).css('min-height', (max + offset))
        } else if (max == heights.window) {
          $(Selector.CONTENT).css('min-height', (max + offset) - heights.header - heights.footer)
        } else {
          $(Selector.CONTENT).css('min-height', (max + offset) - heights.header)
        }
      }

      if ($('body').hasClass(ClassName.LAYOUT_FIXED)) {
        if (offset !== false) {
          $(Selector.CONTENT).css('min-height', (max + offset) - heights.header - heights.footer)
        }

        if (typeof $.fn.overlayScrollbars !== 'undefined') {
          $(Selector.SIDEBAR).overlayScrollbars({
            className       : this._config.scrollbarTheme,
            sizeAutoCapable : true,
            scrollbars : {
              autoHide: this._config.scrollbarAutoHide, 
              clickScrolling : true
            }
          })
        }
      }
    }

    fixLoginRegisterHeight() {
      if ($(Selector.LOGIN_BOX + ', ' + Selector.REGISTER_BOX).length === 0) {
        $('body, html').css('height', 'auto')
      } else if ($(Selector.LOGIN_BOX + ', ' + Selector.REGISTER_BOX).length !== 0) {
        let box_height = $(Selector.LOGIN_BOX + ', ' + Selector.REGISTER_BOX).height()

        if ($('body').css('min-height') !== box_height) {
          $('body').css('min-height', box_height)
        }
      }
    }

    // Private

    _init() {
      // Activate layout height watcher
      this.fixLayoutHeight()

      if (this._config.loginRegisterAutoHeight === true) {      
        this.fixLoginRegisterHeight()
      } else if (Number.isInteger(this._config.loginRegisterAutoHeight)) {      
        setInterval(this.fixLoginRegisterHeight, this._config.loginRegisterAutoHeight);
      }

      $(Selector.SIDEBAR)
        .on('collapsed.lte.treeview expanded.lte.treeview', () => {
          this.fixLayoutHeight()
        })

      $(Selector.PUSHMENU_BTN)
        .on('collapsed.lte.pushmenu shown.lte.pushmenu', () => {
          this.fixLayoutHeight()
        })

      $(Selector.CONTROL_SIDEBAR_BTN)
        .on('collapsed.lte.controlsidebar', () => {
          this.fixLayoutHeight()
        })
        .on('expanded.lte.controlsidebar', () => {
          this.fixLayoutHeight('control_sidebar')
        })

      $(window).resize(() => {
        this.fixLayoutHeight()
      })

      $('body.hold-transition').removeClass('hold-transition')
    }

    _max(numbers) {
      // Calculate the maximum number in a list
      let max = 0

      Object.keys(numbers).forEach((key) => {
        if (numbers[key] > max) {
          max = numbers[key]
        }
      })

      return max
    }

    // Static

    static _jQueryInterface(config = '') {
      return this.each(function () {
        let data = $(this).data(DATA_KEY)
        const _options = $.extend({}, Default, $(this).data())

        if (!data) {
          data = new Layout($(this), _options)
          $(this).data(DATA_KEY, data)
        }

        if (config === 'init' || config === '') {
          data['_init']()
        } else if (config === 'fixLayoutHeight' || config === 'fixLoginRegisterHeight') {
          data[config]()
        }
      })
    }
  }

  /**
   * Data API
   * ====================================================
   */

  $(window).on('load', () => {
    Layout._jQueryInterface.call($('body'))
  })

  $(Selector.SIDEBAR + ' a').on('focusin', () => {
    $(Selector.MAIN_SIDEBAR).addClass(ClassName.SIDEBAR_FOCUSED);
  })

  $(Selector.SIDEBAR + ' a').on('focusout', () => {
    $(Selector.MAIN_SIDEBAR).removeClass(ClassName.SIDEBAR_FOCUSED);
  })

  /**
   * jQuery API
   * ====================================================
   */

  $.fn[NAME] = Layout._jQueryInterface
  $.fn[NAME].Constructor = Layout
  $.fn[NAME].noConflict = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return Layout._jQueryInterface
  }

  return Layout
})(jQuery)

export default Layout
