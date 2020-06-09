(function ($) {
    'use strict'

    window.ui_changes = window.ui_changes || {}

    $('#no-navbar-border').on('click', function () {
        var $elem = $('nav#jazzy-topmenu');
        $elem.toggleClass('border-bottom-0');
        window.ui_changes['no_navbar_border'] = $elem.hasClass('border-bottom-0');
    });

    $('#body-small-text').on('click', function () {
        var $elem = $('body');
        $elem.toggleClass('text-sm');
        window.ui_changes['body_small_text'] = this.checked;
    });

    $('#navbar-small-text').on('click', function () {
        var $elem = $('nav#jazzy-topmenu');
        $elem.toggleClass('text-sm');
        window.ui_changes['navbar_small_text'] = this.checked;
    });

    $('#sidebar-nav-small-text').on('click', function () {
        var $elem = $('aside#jazzy-sidemenu nav ul:first-child');
        $elem.toggleClass('text-sm');
        window.ui_changes['sidebar_nav_small_text'] = this.checked;
    });

    $('#footer-small-text').on('click', function () {
        var $elem = $('footer');
        $elem.toggleClass('text-sm');
        window.ui_changes['footer_small_text'] = this.checked;
    });

    $('#sidebar-nav-flat-style').on('click', function () {
        var $elem = $('aside#jazzy-sidemenu nav ul:first-child');
        $elem.toggleClass('nav-flat');
        window.ui_changes['sidebar_nav_flat_style'] = this.checked;
    });

    $('#sidebar-nav-legacy-style').on('click', function () {
        var $elem = $('aside#jazzy-sidemenu nav ul:first-child');
        $elem.toggleClass('nav-legacy');
        window.ui_changes['sidebar_nav_legacy_style'] = this.checked;
    });

    $('#sidebar-nav-compact').on('click', function () {
        var $elem = $('aside#jazzy-sidemenu nav ul:first-child');
        $elem.toggleClass('nav-compact');
        window.ui_changes['sidebar_nav_compact_style'] = this.checked;
    });

    $('#sidebar-nav-child-indent').on('click', function () {
        var $elem = $('aside#jazzy-sidemenu nav ul:first-child');
        $elem.toggleClass('nav-child-indent');
        window.ui_changes['sidebar_nav_child_indent'] = this.checked;
    });

    $('#main-sidebar-disable-hover-focus-auto-expand').on('click', function () {
        var $elem = $('aside#jazzy-sidemenu');
        $elem.toggleClass('sidebar-no-expand');
        window.ui_changes['sidebar_disable_expand'] = this.checked;
    });

    $('#brand-small-text').on('click', function () {
        var $elem = $('a.brand-link');
        $elem.toggleClass('text-sm');
        window.ui_changes['brand_small_text'] = this.checked;
    });

    $('#navbar-variants div').on('click', function () {
        var newClasses = $(this).data('classes');
        $('nav#jazzy-topmenu').removeClass (function (index, className) {
            return (className.match (/(^|\s)navbar-\S+/g) || []).join(' ');
        }).addClass('navbar-expand ' +  newClasses);

        window.ui_changes['topmenu'] = newClasses.split(' ');
    });

    $('#accent-colours div').on('click', function () {
        var newClasses = $(this).data('classes');

        $('body').removeClass (function (index, className) {
            return (className.match (/(^|\s)accent-\S+/g) || []).join(' ');
        }).addClass(newClasses);

        window.ui_changes['accent'] = newClasses.split(' ');
    });

    $('#dark-sidebar-variants div, #light-sidebar-variants div').on('click', function () {
        var newClasses = $(this).data('classes');

        $('aside#jazzy-sidemenu').removeClass (function (index, className) {
            return (className.match (/(^|\s)sidebar-\S+/g) || []).join(' ');
        }).addClass(newClasses);

        window.ui_changes['sidemenu'] = newClasses.split(' ');
    });

    $('#brand-logo-variants div').on('click', function () {
        var newClasses = $(this).data('classes');

        $('#jazzy-logo').removeClass (function (index, className) {
            return (className.match (/(^|\s)navbar-\S+/g) || []).join(' ');
        }).addClass(newClasses);

        window.ui_changes['brand_colour'] = newClasses.split(' ');
    });

})(jQuery)
