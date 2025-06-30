(function($) {
    function filterDashboardModels() {
        $("#model-filter-dashboard").on("input", function() {
            const filter = $(this).val().toLowerCase();

            $("#card-container > * > .card").each(function() {
                let appHasMatch = false;
                const $appCard = $(this);
                const $rows = $appCard.find("table > tbody > tr");

                $rows.each(function() {
                    const modelName = $(this).find("td:first-child > a").text().toLowerCase();
                    const isMatch = modelName.includes(filter);

                    $(this).toggle(isMatch);
                    if (isMatch) appHasMatch = true;
                });

                $appCard.toggle(appHasMatch);
            });
        });
    };

    $(document).ready(function() {
        filterDashboardModels();
    });
})(jQuery);