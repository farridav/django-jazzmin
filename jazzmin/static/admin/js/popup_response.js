(function() {
    'use strict';

    let windowRef = window;
    let windowName, widgetName;
    let openerRef = windowRef.opener;
    if (!openerRef) {
        // related modal is active
        openerRef = windowRef.parent;
        windowName = windowRef.name;
        widgetName = windowName.replace(/^(change|add|delete|lookup)_/, '');
        if (typeof(openerRef.id_to_windowname) === 'function') {
            // django < 3.1 compatibility
            widgetName = openerRef.id_to_windowname(widgetName);
        }
        windowRef = {
            name: widgetName,
            close: function() {
                openerRef.dismissRelatedObjectModal();
            }
        };
    }

    // select before last iframe content window if exists else select openerRef
    let openerRef2;
    var iframeHTMLCollection = openerRef.document.getElementsByTagName('iframe');
    if (iframeHTMLCollection.length >= 2) {
        var beforeLastIframeIndex = iframeHTMLCollection.length - 2;
        openerRef2 = iframeHTMLCollection[beforeLastIframeIndex].contentWindow;
    } else {
        openerRef2 = openerRef;
    }

    // default django popup_response.js
    const initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
    switch (initData.action) {
        case 'change':
            if (typeof(openerRef.dismissChangeRelatedObjectPopup) === 'function') {
                openerRef2.dismissChangeRelatedObjectPopup(windowRef, initData.value, initData.obj, initData.new_value);
            }
            break;
        case 'delete':
            if (typeof(openerRef.dismissDeleteRelatedObjectPopup) === 'function') {
                openerRef2.dismissDeleteRelatedObjectPopup(windowRef, initData.value);
            }
            break;
        default:
            if (typeof(openerRef.dismissAddRelatedObjectPopup) === 'function') {
                openerRef2.dismissAddRelatedObjectPopup(windowRef, initData.value, initData.obj);
            }
            else if (typeof(openerRef.dismissAddAnotherPopup) === 'function') {
                // django 1.7 compatibility
                openerRef2.dismissAddAnotherPopup(windowRef, initData.value, initData.obj);
            }
            break;
    }

})();
