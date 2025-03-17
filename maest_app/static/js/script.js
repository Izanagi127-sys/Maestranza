

/* inicio base */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
/* fin base */





/* inicio navbar  */

document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.getElementById("mobile-menu");
    const navbarNav = document.querySelector(".navbar-nav");

    menuToggle.addEventListener("click", function() {
        menuToggle.classList.toggle("active");
        navbarNav.classList.toggle("active");
    });
});


/* fin navbar  */