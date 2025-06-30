(function($) {
    function filterDashboardModels() {
        $("#model-filter-dashboard").on("input", function() {
            const filter = $(this).val().toLowerCase();
        });
    };

    $(document).ready(function() {
        filterDashboardModels();
    });
})(jQuery);