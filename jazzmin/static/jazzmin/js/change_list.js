$.fn.search_filters = function () {
    $(this).change(function () {
        var $field = $(this);
        var $option = $field.find('option:selected');
        var select_name = $option.data('name');
        if (select_name) {
            $field.attr('name', select_name);
        } else {
            $field.removeAttr('name');
        }
    });
    $(this).trigger('change');
};

$(document).ready(function () {
    // Ensure all raw_id_fields have the search icon in them
    $('.related-lookup').append('<i class="fa fa-search"></i>')

    // Allow for styling of selects
    $('.actions select').addClass('form-control');

    // Make search filters select2 and ensure they work for filtering
    var $ele = $('.search-filter');
    $ele.search_filters();
    $ele.select2();
});
