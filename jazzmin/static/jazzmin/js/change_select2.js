window.onload = function() {
    document.querySelectorAll(
        ".select2.select2-container.select2-container--admin-autocomplete"
    ).forEach((select) => {
            select.setAttribute(
                "class", 
                "select2 select2-container select2-container--default select2-container--focus"
            )
            select.setAttribute(
                "style",
                "width: 100%"
            )
        }
    )
}