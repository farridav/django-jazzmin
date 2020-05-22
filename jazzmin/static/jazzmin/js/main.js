function setCookie(key, value) {
    var expires = new Date();
    expires.setTime(expires.getTime() + (value * 24 * 60 * 60 * 1000));
    document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + '; SameSite=Strict;path=/';
}

function getCookie(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
}

function eraseCookie(key) {
    var keyValue = getCookie(key);
    setCookie(key, keyValue, '-1');
}

$(document).ready(function () {

    // Set the currently active menu item based on the url
    $('a[href="' + window.location.pathname + '"]').addClass('active');

    // Ensure all raw_id_fields have the search icon in them
    $('.related-lookup').append('<i class="fa fa-search"></i>')

    // Allow for styling of selects
    $('.actions select').addClass('form-control');

    // When we use the menu, store its state in a cookie to preserve it
    $('[data-widget=pushmenu]').bind('click', function () {
        var menuClosed = getCookie('jazzy_menu') === 'closed';
        if (!menuClosed) {
            setCookie('jazzy_menu', 'closed');
        } else {
            setCookie('jazzy_menu', 'open');
        }
    });

});
