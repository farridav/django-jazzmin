window.addEventListener('load', function(){
    document.querySelector('body').classList.add("loaded")
    
    const navItems = document.querySelectorAll('ul.nav-sidebar li.nav-item');

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            document.querySelector('body').classList.remove("loaded")  
        });
    });
});