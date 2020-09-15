function handleCarousel($carousel) {
    const errors = $('.errorlist li', $carousel);
    const hash = document.location.hash;

    // If we have errors, open that tab first
    if (errors.length) {
        const errorCarousel = errors.eq(0).closest('.carousel-item').data('carouselid');
        $carousel.carousel(errorCarousel);

    // If we have a tab hash, open that
    } else if (hash) {
        const activeCarousel = $('.carousel-item[data-target="' + hash + '"]', $carousel).data('carouselid');
        $carousel.carousel(activeCarousel);
    }

    // Update page hash/history on slide
    $carousel.on('slide.bs.carousel', function (e) {
        if (e.relatedTarget.dataset.hasOwnProperty("label")) {
            $('.carousel-fieldset-label', $carousel).text(e.relatedTarget.dataset.label);
        }
        const hash = e.relatedTarget.dataset.target;

        if (history.pushState) {
            history.pushState(null, null, hash);
        } else {
            location.hash = hash;
        }
    });
}

function handleTabs($tabs) {
    const errors = $('.change-form .errorlist li');
    const hash = document.location.hash;

    // If we have errors, open that tab first
    if (errors.length) {
        const tabId = errors.eq(0).closest('.tab-pane').attr('id');
        $('.nav-tabs a[href="#' + tabId + '"]').tab('show');

    // If we have a tab hash, open that
    } else if (hash) {
        $('.nav-tabs a[href="' + hash + '"]', $tabs).tab('show');
    }

    // Change hash for page-reload
    $('.nav-tabs a').on('shown.bs.tab', function (e) {
        e.preventDefault();
        if (history.pushState) {
            history.pushState(null, null, e.target.hash);
        } else {
            location.hash = e.target.hash;
        }
        
        // Fix selector heights
	$('.selector .selector-chosen').each( function(i) {
	    var a = $(this).siblings('.selector-available');
            var s = $(this).find('select').first();
            s.height( a.find('select').first().height() + a.find('p.selector-filter').first().outerHeight() );
            s.css('border-top', s.css('border-bottom') );
        })
    });
}

function handleCollapsible($collapsible) {
    const errors = $('.errorlist li', $collapsible);
    const hash = document.location.hash;

    // If we have errors, open that tab first
    if (errors.length) {
        $('.panel-collapse', $collapsible).collapse('hide');
        errors.eq(0).closest('.panel-collapse').collapse('show');

    // If we have a tab hash, open that
    } else if (hash) {
        $('.panel-collapse', $collapsible).collapse('hide');
        $(hash, $collapsible).collapse('show');
    }

    // Change hash for page-reload
    $collapsible.on('shown.bs.collapse', function (e) {
        if (history.pushState) {
            history.pushState(null, null, '#' + e.target.id);
        } else {
            location.hash = '#' + e.target.id;
        }
    });
}

$(document).ready(function () {
    const $carousel = $('#content-main form #jazzy-carousel');
    const $tabs = $('#content-main form #jazzy-tabs');

    // Stop the height being set to 1px during a JS race condition
    // TODO: Find the JS that is setting this html attribute, and solve the problem properly
    $('.selector .selector-chosen select').removeAttr('style');

    // Ensure all raw_id_fields have the search icon in them
    const $collapsible = $('#content-main form #jazzy-collapsible');
    $('.related-lookup').append('<i class="fa fa-search"></i>');

    // Style the inline fieldset button
    $('.inline-related fieldset.module .add-row a').addClass('btn btn-sm btn-default float-right');

    // Ensure we preserve the tab the user was on using the url hash, even on page reload
    if ($tabs.length) {handleTabs($tabs);}
    else if ($carousel.length) {handleCarousel($carousel);}
    else if ($collapsible.length) {handleCollapsible($collapsible);}
});
