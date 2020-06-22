(function ($) {
    'use strict'

    var $body = $('body');
    var $footer = $('footer');
    var $sidebar_ul = $('aside#jazzy-sidebar nav ul:first-child');
    var $sidebar = $('aside#jazzy-sidebar');
    var $navbar = $('nav#jazzy-navbar');
    var $logo = $('#jazzy-logo');

    window.ui_changes = window.ui_changes || {}

    // Toggles
    function addListeners() {
        $('#body-small-text').on('click', function () {
            $body.toggleClass('text-sm');
            window.ui_changes['body_small_text'] = this.checked;
        });

        $('#footer-small-text').on('click', function () {
            $footer.toggleClass('text-sm');
            window.ui_changes['footer_small_text'] = this.checked;
        });

        $('#sidebar-nav-small-text').on('click', function () {
            $sidebar_ul.toggleClass('text-sm');
            window.ui_changes['sidebar_nav_small_text'] = this.checked;
        });

        $('#sidebar-nav-flat-style').on('click', function () {
            $sidebar_ul.toggleClass('nav-flat');
            window.ui_changes['sidebar_nav_flat_style'] = this.checked;
        });

        $('#sidebar-nav-legacy-style').on('click', function () {
            $sidebar_ul.toggleClass('nav-legacy');
            window.ui_changes['sidebar_nav_legacy_style'] = this.checked;
        });

        $('#sidebar-nav-compact').on('click', function () {
            $sidebar_ul.toggleClass('nav-compact');
            window.ui_changes['sidebar_nav_compact_style'] = this.checked;
        });

        $('#sidebar-nav-child-indent').on('click', function () {
            $sidebar_ul.toggleClass('nav-child-indent');
            window.ui_changes['sidebar_nav_child_indent'] = this.checked;
        });

        $('#main-sidebar-disable-hover-focus-auto-expand').on('click', function () {
            $sidebar.toggleClass('sidebar-no-expand');
            window.ui_changes['sidebar_disable_expand'] = this.checked;
        });

        $('#no-navbar-border').on('click', function () {
            $navbar.toggleClass('border-bottom-0');
            window.ui_changes['no_navbar_border'] = $navbar.hasClass('border-bottom-0');
        });

        $('#navbar-small-text').on('click', function () {
            $navbar.toggleClass('text-sm');
            window.ui_changes['navbar_small_text'] = this.checked;
        });

        $('#brand-small-text').on('click', function () {
            $logo.toggleClass('text-sm');
            window.ui_changes['brand_small_text'] = this.checked;
        });

        // Colour pickers
        $('#navbar-variants div').on('click', function () {
            $(this).removeClass('inactive').addClass('active').parent().find(
                'div'
            ).not(this).removeClass('active').addClass('inactive');

            var newClasses = $(this).data('classes');

            $navbar.removeClass(function (index, className) {
                return (className.match(/(^|\s)navbar-\S+/g) || []).join(' ');
            }).addClass('navbar-expand ' + newClasses);

            window.ui_changes['navbar'] = newClasses;
        });

        $('#accent-colours div').on('click', function () {
            $(this).removeClass('inactive').addClass('active').parent().find(
                'div'
            ).not(this).removeClass('active').addClass('inactive');

            var newClasses = $(this).data('classes');

            $body.removeClass(function (index, className) {
                return (className.match(/(^|\s)accent-\S+/g) || []).join(' ');
            }).addClass(newClasses);

            window.ui_changes['accent'] = newClasses;
        });

        $('#dark-sidebar-variants div, #light-sidebar-variants div').on('click', function () {
            $(this).removeClass('inactive').addClass('active').parent().find(
                'div'
            ).not(this).removeClass('active').addClass('inactive');

            var newClasses = $(this).data('classes');

            $sidebar.removeClass(function (index, className) {
                return (className.match(/(^|\s)sidebar-[\S|-]+/g) || []).join(' ');
            }).addClass(newClasses);

            window.ui_changes['sidebar'] = newClasses.trim();
        });

        $('#brand-logo-variants div').on('click', function () {
            $(this).removeClass('inactive').addClass('active').parent().find(
                'div'
            ).not(this).removeClass('active').addClass('inactive');

            var newClasses = $(this).data('classes');

            $logo.removeClass(function (index, className) {
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
    }

    function setFromExisting() {
        $('#body-small-text').get(0).checked = window.ui_changes['body_small_text'];
        $('#footer-small-text').get(0).checked = window.ui_changes['footer_small_text'];
        $('#sidebar-nav-small-text').get(0).checked = window.ui_changes['sidebar_nav_small_text'];
        $('#sidebar-nav-legacy-style').get(0).checked = window.ui_changes['sidebar_nav_legacy_style'];
        $('#sidebar-nav-compact').get(0).checked = window.ui_changes['sidebar_nav_compact_style'];
        $('#sidebar-nav-child-indent').get(0).checked = window.ui_changes['sidebar_nav_child_indent'];
        $('#main-sidebar-disable-hover-focus-auto-expand').get(0).checked = window.ui_changes['sidebar_disable_expand'];
        $('#no-navbar-border').get(0).checked = window.ui_changes['no_navbar_border'];
        $('#navbar-small-text').get(0).checked = window.ui_changes['navbar_small_text'];
        $('#brand-small-text').get(0).checked = window.ui_changes['brand_small_text'];

        $('#navbar-variants div, #accent-colours div, #dark-sidebar-variants div, #light-sidebar-variants div, #brand-logo-variants div').addClass('inactive');

        $('#navbar-variants div[data-classes="' + window.ui_changes['navbar'] + '"]').addClass('active');
        $('#accent-colours div[data-classes="' + window.ui_changes['accent'] + '"]').addClass('active');
        $('#dark-sidebar-variants div[data-classes="' + window.ui_changes['sidebar'] + '"]').addClass('active');
        $('#light-sidebar-variants div[data-classes="' + window.ui_changes['sidebar'] + '"]').addClass('active');
        $('#brand-logo-variants div[data-classes="' + window.ui_changes['brand_colour'] + '"]').addClass('active');
    }

    setFromExisting();
    addListeners();

})(jQuery)
