(function($) {
    'use strict';

    $(document).ready(function(){

        // create the function that will close the modal
        function dismissModal() {
            $('#related-modal').modal('hide');
        }

        // assign functions to global variables
        window.dismissRelatedObjectModal = dismissModal;
        window.dismissRelatedLookupPopup = dismissRelatedLookupModal;

        function dismissRelatedLookupModal(win, chosenId) {
            let windowName = win.name;
            let widgetName = windowName.replace(/^(change|add|delete|lookup)_/, '');
            let widgetEl = $('#' + widgetName);
            let widgetVal = widgetEl.val();
            if (widgetEl.hasClass('vManyToManyRawIdAdminField') && Boolean(widgetVal)) {
                widgetEl.val(widgetVal + ', ' + chosenId);
            } else {
                widgetEl.val(chosenId);
            }
            dismissModal();
        }

        function presentRelatedObjectModal(e) {
            let linkEl = $(this);
            let href = (linkEl.attr('href') || '');
            if (href === '') {
                return;
            }

            // open the popup as modal
            e.preventDefault();
            e.stopImmediatePropagation();

            // remove focus from clicked link
            linkEl.blur();

            // use the clicked link id as iframe name
            // it will be available as window.name in the loaded iframe
            let iframeName = linkEl.attr('id');
            let iframeSrc = href;
            const title = linkEl.attr('title');

            if (e.data.lookup !== true) {
                // browsers stop loading nested iframes having the same src url
                // create a random parameter and append it to the src url to prevent it
                // this workaround doesn't work with related lookup url
                let iframeSrcRandom = String(Math.round(Math.random() * 999999));
                if (iframeSrc.indexOf('?') === -1) {
                    iframeSrc += '?_modal=' + iframeSrcRandom;
                } else {
                    iframeSrc += '&_modal=' + iframeSrcRandom;
                }
            }

            if (iframeSrc.indexOf('_popup=1') === -1) {
                if (iframeSrc.indexOf('?') === -1) {
                    iframeSrc += '?_popup=1';
                } else {
                    iframeSrc += '&_popup=1';
                }
            }

            // build the iframe html
            let iframeHTML = '<iframe id="related-modal-iframe" name="' + iframeName + '" src="' + iframeSrc + '" frameBorder="0" class="related-iframe"></iframe>';
            let modalEl = $("#related-modal");
            modalEl.find('.modal-body').html(iframeHTML);
            let iframeEl = modalEl.find('#related-modal-iframe');

            if (e.data.lookup === true) {
                // set current window as iframe opener because
                // the callback is called on the opener window
                iframeEl.on('load', function() {
                    let iframeObj = $(this).get(0);
                    let iframeWindow = iframeObj.contentWindow;
                    iframeWindow.opener = window;
                });
            }

            // the modal css class
            let iframeInternalModalClass = 'related-modal';

            // if the current window is inside an iframe, it means that it is already in a modal,
            // append an additional css class to the modal to offer more customization
            if (window.top !== window.self) {
                iframeInternalModalClass += ' related-modal__nested';
            }

            // Set the modal title based on the opening link
            $('.modal-title', modalEl).html(title);

            // open the modal using bootstrap modal
            modalEl.modal('show');

            return false;
        }

        // listen click events on related links
        function presentRelatedObjectModalOnClickOn(selector, lookup) {
            let el = $(selector);
            el.removeAttr('onclick');
            el.unbind('click');
            el.click({lookup: lookup}, presentRelatedObjectModal);
        }

        function init() {
            presentRelatedObjectModalOnClickOn('a.related-widget-wrapper-link', false);

            // raw_id_fields support
            presentRelatedObjectModalOnClickOn('a.related-lookup', true);

            // django-dynamic-raw-id support - #61
            // https://github.com/lincolnloop/django-dynamic-raw-id
            presentRelatedObjectModalOnClickOn('a.dynamic_raw_id-related-lookup', true);
        }

        // initialise
        init()
    });

})(jQuery);
