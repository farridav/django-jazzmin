window.onload = function() {
    selects = document.getElementsByClassName(
        "select2 select2-container select2-container--admin-autocomplete"
    )
    for (const select of selects) {
        select.setAttribute(
            "class",
            "select2 select2-container select2-container--default select2-container--focus"
        )
    }
}