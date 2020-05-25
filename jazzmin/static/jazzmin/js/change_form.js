function prependCalendarIcon() {

    $(".datetime").each(function(index, element) {
        var vDateField = $(element).find('input.vDateField')[0];
        var vTimeField = $(element).find('input.vTimeField')[0];

        console.log(vTimeField);

        $(element).replaceWith(
            '<div class="datetime input-group">' +
            '<div class="input-group-prepend">' +
            '<span class="input-group-text">' +
            '<i class="far fa-calendar-alt"></i></span></div>' +
            '<input type="text" name="' + vDateField.name + '" class="form-control float-right" id="' + vDateField.id + '">' +
            '<a href="#" id="calendarlink0"><span class="date-icon" title="Choose a Date"></span></a>' +
            '<div class="input-group-prepend">' +
            '<span class="input-group-text">' +
            '<i class="far fa-clock"></i></span></div>' +
            '<input type="text" name="' + vTimeField.name + '" class="form-control float-right" id="' + vTimeField.id + '">' +
            '</div>'
        )
    });
}

$(document).ready(function() {
    prependCalendarIcon();
});

<a href="#" id="calendarlink0"><span class="date-icon" title="Choose a Date"></span></a>
<a href="#" id="clocklink0"><span class="clock-icon" title="Choose a Time"></span></a>