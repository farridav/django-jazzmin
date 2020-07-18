function setCookie(key, value) {
    var expires = new Date();
    expires.setTime(expires.getTime() + (value * 24 * 60 * 60 * 1000));
    document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + '; SameSite=Strict;path=/';
}

function getCookie(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
}

function handleMenu() {
    $('[data-widget=pushmenu]').bind('click', function () {
        var menuClosed = getCookie('jazzy_menu') === 'closed';
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
    } else if ($parent_link.length){
        $parent_link.addClass('active');
    }
}

$(document).ready(function () {
    // Set active status on links
    setActiveLinks()

    // When we use the menu, store its state in a cookie to preserve it
    handleMenu();
});
