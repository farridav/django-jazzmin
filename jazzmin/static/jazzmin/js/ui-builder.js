(function ($) {
    'use strict'

    window.ui_changes = window.ui_changes || {}

    // Toggles
    $('#body-small-text').on('click', function () {
        var $elem = $('body');
        $elem.toggleClass('text-sm');
        window.ui_changes['body_small_text'] = this.checked;
    });

    $('#footer-small-text').on('click', function () {
        var $elem = $('footer');

        $elem.toggleClass('text-sm');
        window.ui_changes['footer_small_text'] = this.checked;
    });

    $('#sidebar-nav-small-text').on('click', function () {
        var $elem = $('aside#jazzy-sidebar nav ul:first-child');

        $elem.toggleClass('text-sm');
        window.ui_changes['sidebar_nav_small_text'] = this.checked;
    });

    $('#sidebar-nav-flat-style').on('click', function () {
        var $elem = $('aside#jazzy-sidebar nav ul:first-child');

        $elem.toggleClass('nav-flat');
        window.ui_changes['sidebar_nav_flat_style'] = this.checked;
    });

    $('#sidebar-nav-legacy-style').on('click', function () {
        var $elem = $('aside#jazzy-sidebar nav ul:first-child');

        $elem.toggleClass('nav-legacy');
        window.ui_changes['sidebar_nav_legacy_style'] = this.checked;
    });

    $('#sidebar-nav-compact').on('click', function () {
        var $elem = $('aside#jazzy-sidebar nav ul:first-child');

        $elem.toggleClass('nav-compact');
        window.ui_changes['sidebar_nav_compact_style'] = this.checked;
    });

    $('#sidebar-nav-child-indent').on('click', function () {
        var $elem = $('aside#jazzy-sidebar nav ul:first-child');

        $elem.toggleClass('nav-child-indent');
        window.ui_changes['sidebar_nav_child_indent'] = this.checked;
    });

    $('#main-sidebar-disable-hover-focus-auto-expand').on('click', function () {
        var $elem = $('aside#jazzy-sidebar');

        $elem.toggleClass('sidebar-no-expand');
        window.ui_changes['sidebar_disable_expand'] = this.checked;
    });

    $('#no-navbar-border').on('click', function () {
        var $elem = $('nav#jazzy-navbar');
        $elem.toggleClass('border-bottom-0');
        window.ui_changes['no_navbar_border'] = $elem.hasClass('border-bottom-0');
    });

    $('#navbar-small-text').on('click', function () {
        var $elem = $('nav#jazzy-navbar');

        $elem.toggleClass('text-sm');
        window.ui_changes['navbar_small_text'] = this.checked;
    });

    $('#brand-small-text').on('click', function () {
        var $elem = $('#jazzy-logo');

        $elem.toggleClass('text-sm');
        window.ui_changes['brand_small_text'] = this.checked;
    });

    // Colour pickers
    $('#navbar-variants div').on('click', function () {
        $(this).removeClass('inactive').addClass('active').parent().find(
            'div'
        ).not(this).removeClass('active').addClass('inactive');

        var $elem = $('nav#jazzy-navbar');
        var newClasses = $(this).data('classes');

        $elem.removeClass(function (index, className) {
            return (className.match(/(^|\s)navbar-\S+/g) || []).join(' ');
        }).addClass('navbar-expand ' + newClasses);

        window.ui_changes['navbar'] = newClasses;
    });

    $('#accent-colours div').on('click', function () {
        $(this).removeClass('inactive').addClass('active').parent().find(
            'div'
        ).not(this).removeClass('active').addClass('inactive');

        var $elem = $('body');
        var newClasses = $(this).data('classes');

        $elem.removeClass(function (index, className) {
            return (className.match(/(^|\s)accent-\S+/g) || []).join(' ');
        }).addClass(newClasses);

        window.ui_changes['accent'] = newClasses;
    });

    $('#dark-sidebar-variants div, #light-sidebar-variants div').on('click', function () {
        $(this).removeClass('inactive').addClass('active').parent().find(
            'div'
        ).not(this).removeClass('active').addClass('inactive');

        var $elem = $('aside#jazzy-sidebar');
        var newClasses = $(this).data('classes');

        $elem.removeClass(function (index, className) {
            return (className.match(/(^|\s)sidebar-[\S|-]+/g) || []).join(' ');
        }).addClass(newClasses);

        window.ui_changes['sidebar'] = newClasses.trim();
    });

    $('#brand-logo-variants div').on('click', function () {
        $(this).removeClass('inactive').addClass('active').parent().find(
            'div'
        ).not(this).removeClass('active').addClass('inactive');

        var $elem = $('#jazzy-logo');
        var newClasses = $(this).data('classes');

        $elem.removeClass(function (index, className) {
            return (className.match(/(^|\s)navbar-\S+/g) || []).join(' ');
        }).addClass(newClasses);

        if (newClasses === "") {
            newClasses = false;
            $(this).parent().find('div').removeClass('active inactive');
        }

        window.ui_changes['brand_colour'] = newClasses;
    });

    $("#codeBox").on('show.bs.modal', function () {
        $('.modal-body code', this).html(
            'JAZZMIN_UI_TWEAKS = ' + JSON.stringify(
            window.ui_changes, null, 4
            ).replace(
            /true/g, 'True'
            ).replace(
            /false/g, 'False'
            )
        );
    });

})(jQuery)
