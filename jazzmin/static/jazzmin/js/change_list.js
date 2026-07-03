(function() {
    'use strict';

    function applySearchFilterBehavior(element) {
        element.addEventListener('change', function () {
            const selectedOption = element.options[element.selectedIndex];
            const selectName = selectedOption ? selectedOption.dataset.name : null;

            if (selectName) {
                element.setAttribute('name', selectName);
            } else {
                element.removeAttribute('name');
            }
        });
        element.dispatchEvent(new Event('change'));
    }

    function initSearchFilters() {
        document.querySelectorAll('.search-filter').forEach(applySearchFilterBehavior);
        document.querySelectorAll('.search-filter-mptt').forEach(applySearchFilterBehavior);
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.related-lookup').forEach(function (el) {
            const icon = document.createElement('i');
            icon.className = 'fa fa-search';
            el.appendChild(icon);
        });
        document.querySelectorAll('.actions select').forEach(function (el) {
            el.classList.add('form-select');
        });

        initSearchFilters();
    });
})();