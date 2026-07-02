(function() {
    'use strict';

    function FixSelectorHeight() {
        document.querySelectorAll('.selector .selector-chosen').forEach(function(selector_chosen) {
            const selector_available = selector_chosen.parentElement.querySelector('.selector-available');
            if (!selector_available) return;

            const selector_chosen_select = selector_chosen.querySelector('select');
            const selector_available_select = selector_available.querySelector('select');
            const selector_available_filter = selector_available.querySelector('p.selector-filter');

            if (selector_chosen_select && selector_available_select) {
                const filterHeight = selector_available_filter ? selector_available_filter.offsetHeight : 0;
                selector_chosen_select.style.height = (selector_available_select.offsetHeight + filterHeight) + 'px';
                selector_chosen_select.style.borderTop = window.getComputedStyle(selector_chosen_select).borderBottom;
            }
        });
    }

    function handleCarousel(carouselEl) {
        const errors = carouselEl.querySelectorAll('.errorlist li');
        const hash = document.location.hash;
        const labelEl = carouselEl.querySelector('.carousel-fieldset-label');

        if (errors.length) {
            const errorCarousel = errors[0].closest('.carousel-item');
            const carouselInstance = bootstrap.Carousel.getOrCreateInstance(carouselEl);
            carouselInstance.to(parseInt(errorCarousel.dataset.carouselid));
            if (labelEl) labelEl.textContent = errorCarousel.dataset.label;
        } else if (hash) {
            const activeCarousel = carouselEl.querySelector(`.carousel-item[data-target="${hash}"]`);
            if (activeCarousel) {
                const carouselInstance = bootstrap.Carousel.getOrCreateInstance(carouselEl);
                carouselInstance.to(parseInt(activeCarousel.dataset.carouselid));
                if (labelEl) labelEl.textContent = activeCarousel.dataset.label;
            }
        }

        carouselEl.addEventListener('slide.bs.carousel', function(e) {
            const next = e.relatedTarget;
            if (labelEl) labelEl.textContent = next.dataset.label;
            document.location.hash = next.dataset.target;
        });
    }

    function handleTabs(tabsEl) {
        const errorTabs = tabsEl.querySelectorAll('.errorlist');
        const hash = window.location.hash;

        if (errorTabs.length) {
            const errorTabId = errorTabs[0].closest('.tab-pane').id;
            const navLink = tabsEl.querySelector(`.nav-link[href="#${errorTabId}"], .nav-link[data-bs-target="#${errorTabId}"]`);
            if (navLink) {
                const tabInstance = bootstrap.Tab.getOrCreateInstance(navLink);
                tabInstance.show();
            }
        } else if (hash) {
            const navLink = tabsEl.querySelector(`.nav-link[href="${hash}"], .nav-link[data-bs-target="${hash}"]`);
            if (navLink) {
                const tabInstance = bootstrap.Tab.getOrCreateInstance(navLink);
                tabInstance.show();
            }
        }

        tabsEl.querySelectorAll('a[data-bs-toggle="tab"]').forEach(function(tabLink) {
            tabLink.addEventListener('shown.bs.tab', function(e) {
                const target = e.target.getAttribute('href') || e.target.dataset.bsTarget;
                if (history.pushState) {
                    history.pushState(null, null, target);
                } else {
                    window.location.hash = target;
                }
            });
        });
    }

    function handleCollapsible(collapsibleEl) {
        const errors = collapsibleEl.querySelectorAll('.errorlist li');
        const hash = document.location.hash;

        if (errors.length) {
            const errorAccordion = errors[0].closest('.accordion-item');
            const collapseEl = errorAccordion.querySelector('.accordion-collapse');
            if (collapseEl) {
                const collapseInstance = bootstrap.Collapse.getOrCreateInstance(collapseEl);
                collapseInstance.show();
            }
        } else if (hash) {
            const activeAccordion = collapsibleEl.querySelector(`.accordion-item[data-target="${hash}"]`);
            if (activeAccordion) {
                const collapseEl = activeAccordion.querySelector('.accordion-collapse');
                if (collapseEl) {
                    const collapseInstance = bootstrap.Collapse.getOrCreateInstance(collapseEl);
                    collapseInstance.show();
                }
            }
        }

        collapsibleEl.addEventListener('shown.bs.collapse', function(e) {
            const item = e.target.closest('.accordion-item');
            if (item) {
                document.location.hash = item.dataset.target;
            }
        });
    }

    function applyNativeSelectFormatting() {
        document.querySelectorAll('select').forEach(function(select) {
            if (select.classList.contains('newsletter-recipients') ||
                select.classList.contains('raw-id-field') ||
                select.closest('.empty-form') ||
                select.style.display === 'none') {
                return;
            }
            select.classList.add('form-select');
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const carouselEl = document.querySelector('#content-main form #jazzy-carousel');
        const tabsEl = document.querySelector('#content-main form #jazzy-tabs');
        const collapsibleEl = document.querySelector('#content-main form #jazzy-collapsible');

        document.querySelectorAll('.related-lookup').forEach(function(el) {
            if (!el.querySelector('.fa-search')) {
                el.insertAdjacentHTML('beforeend', '<i class="fa fa-search ms-1"></i>');
            }
        });

        document.querySelectorAll('.inline-related fieldset.module .add-row a, div.add-row > a').forEach(function(el) {
            el.classList.add('btn', 'btn-sm', 'btn-default', 'float-end');
        });

        if (tabsEl) { handleTabs(tabsEl); }
        else if (carouselEl) { handleCarousel(carouselEl); }
        else if (collapsibleEl) { handleCollapsible(collapsibleEl); }

        applyNativeSelectFormatting();

        // Native event delegation replacing $('body').on('change', ...)
        document.body.addEventListener('change', function(e) {
            const selectWrapper = e.target.closest('.related-widget-wrapper select');
            if (selectWrapper) {
                const customEvent = new CustomEvent('django:update-related', { bubbles: true, cancelable: true });
                selectWrapper.dispatchEvent(customEvent);

                if (!customEvent.defaultPrevented && typeof window.updateRelatedObjectLinks !== 'undefined') {
                    window.updateRelatedObjectLinks(selectWrapper);
                }
            }
        });
    });

    // Native support for listening to Django's dynamic inline additions
    document.addEventListener('formset:added', function() {
        applyNativeSelectFormatting();
        FixSelectorHeight();
    });

})();