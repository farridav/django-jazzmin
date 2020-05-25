function prependCalendarIcon() {

    $(".datetime").each(function(index, element) {
        var vDateField = $(element).find('input.vDateField')[0];
        var vTimeField = $(element).find('input.vTimeField')[0];

        $(element).replaceWith(
            '<p class="datetime">' +
            '<div class="input-group">' +
            '<div class="input-group-prepend">' +
            '<span class="input-group-text">' +
            '<i class="far fa-calendar-alt"></i></span></div>' +
            '<input type="text" name="' + vDateField.name + '" class="vDateField form-control float-right" id="' + vDateField.id + '">' +
            '<div class="input-group">' +
            '<div class="input-group-prepend">' +
            '<span class="input-group-text">' +
            '<i class="far fa-clock"></i></span></div>' +
            '<input type="text" name="' + vTimeField.name + '" class="vTimeField form-control float-right" id="' + vTimeField.id + '">' +
            '</div></p>'
        )
    });
}

$(document).ready(function() {
    prependCalendarIcon();
});

