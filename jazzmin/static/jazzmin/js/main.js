(function($) {
    'use strict';

    function setCookie(key, value) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (value * 24 * 60 * 60 * 1000));
        document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + '; SameSite=Strict;path=/';
    }

    function getCookie(key) {
        const keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
        return keyValue ? keyValue[2] : null;
    }

    function handleMenu() {
        $('[data-widget=pushmenu], [data-lte-toggle=sidebar]').on('click', function () {
            const menuClosed = getCookie('jazzy_menu') === 'closed';
            if (!menuClosed) {
                setCookie('jazzy_menu', 'closed');
            } else {
                setCookie('jazzy_menu', 'open');
            }
        });
    }


    function setActiveLinks() {
        /*
         Set the currently active menu item based on the current url, or failing that, find the parent
         item from the breadcrumbs
         */
        const url = window.location.pathname;
        const $breadcrumb = $('.breadcrumb a').last();
        const $link = $('a[href="' + url + '"]');
        const $parent_link = $('a[href="' + $breadcrumb.attr('href') + '"]');

        if ($link.length) {
            $link.addClass('active');
        } else if ($parent_link.length) {
            $parent_link.addClass('active');
        };

        const $a_active = $('a.nav-link.active');
        const $main_li_parent = $a_active.closest('li.nav-item.has-treeview');
        const $ul_child = $main_li_parent.children('ul');

        $ul_child.show();
        $main_li_parent.addClass('menu-is-opening menu-open');
    };

    function initThemeChooser() {
        const $themeSelect = $('#jazzmin-theme-select');
        const $modeSelect = $('#jazzmin-mode-select');

        if (!$themeSelect.length && !$modeSelect.length) {
            return;
        }

        // Restore saved theme from localStorage
        const savedTheme = localStorage.getItem('jazzmin-theme');
        if (savedTheme && $themeSelect.length) {
            $themeSelect.val(savedTheme);
        }

        // Restore saved mode from localStorage
        const savedMode = localStorage.getItem('jazzmin-theme-mode');
        if (savedMode && $modeSelect.length) {
            $modeSelect.val(savedMode);
        }

        // Theme switching — #jazzmin-theme link is always present in the DOM
        $themeSelect.on('change', function () {
            const newTheme = $(this).val();
            const $themeCSS = $('#jazzmin-theme');
            const base = $themeCSS.data('theme-base');

            if (newTheme === 'default') {
                $themeCSS.removeAttr('href');
            } else {
                $themeCSS.attr('href', base + '/' + newTheme + '/bootstrap.min.css');
            }

            $('body').removeClass(function (index, className) {
                return (className.match(/(^|\s)theme-\S+/g) || []).join(' ');
            }).addClass('theme-' + newTheme);

            localStorage.setItem('jazzmin-theme', newTheme);
        });

        // Color scheme switching
        $modeSelect.on('change', function () {
            const mode = $(this).val();
            var resolved = mode === 'auto'
                ? (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
                : mode;
            document.documentElement.setAttribute('data-bs-theme', resolved);
            localStorage.setItem('jazzmin-theme-mode', mode);
        });

        // Keep dropdown open when interacting with selects
        $('#jazzy-theme-chooser').on('click', function (e) {
            e.stopPropagation();
        });
    }

    $(document).ready(function () {
        // Set active status on links
        setActiveLinks()

        // When we use the menu, store its state in a cookie to preserve it
        handleMenu();

        // Theme chooser (navbar dropdown)
        initThemeChooser();

        // Add minimal changelist styling to templates that we have been unable to override (e.g MPTT)
        // Needs to be here and not in change_list.js because this is the only JS we are guaranteed to run
        // (as its included in base.html)
        const $changeListTable = $('#changelist .results table');
        if ($changeListTable.length && !$changeListTable.hasClass('table table-striped')) {
            $changeListTable.addClass('table table-striped');
        };
    });

})(jQuery);
