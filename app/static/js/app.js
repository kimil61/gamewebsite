document.addEventListener('DOMContentLoaded', function () {
    var menuButton = document.getElementById('user-menu-button');
    var menu = document.querySelector('[role="menu"]');

    menuButton.addEventListener('click', function () {
        if (menu.style.display === 'none' || menu.style.display === '') {
            menu.style.display = 'block';
        } else {
            menu.style.display = 'none';
        }
    });
});
