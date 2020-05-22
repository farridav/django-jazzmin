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
    $('a[href="' + window.location.pathname + '"]').addClass('active');

    $('.actions select').addClass('form-control');
    
    $('[data-widget=pushmenu]').bind('click', function () {
        var menuClosed = getCookie('jazzy_menu') === 'closed';
        if (!menuClosed) {
            setCookie('jazzy_menu', 'closed');
        } else {
            setCookie('jazzy_menu', 'open');
        }
    });

});
