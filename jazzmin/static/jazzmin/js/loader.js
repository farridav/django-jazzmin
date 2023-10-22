window.addEventListener('load', function(){
    document.querySelector('body').classList.add("loaded")
    
    const allItems = document.querySelectorAll(
        'ul.nav-sidebar, li.nav-item, th.sorting div.text, th.sorting_asc div.text, th.sorting_desc div.text'
    );

    allItems.forEach(item => {
        item.addEventListener('click', function() {
            document.querySelector('body').classList.remove("loaded")  
        });
    });
});