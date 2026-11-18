// ===================================
// CAMPUSCONNECT JAVASCRIPT
// ===================================


// 1. Welcome Message

document.addEventListener("DOMContentLoaded", function () {

    console.log("CampusConnect Website Loaded Successfully!");

});


// 2. Smooth Scrolling

document.querySelectorAll('a[href^="#"]').forEach(function (link) {

    link.addEventListener("click", function (event) {

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth"
            });

        }

    });

});


// 3. Feature Card Animation

const cards = document.querySelectorAll(".feature-card");

const observer = new IntersectionObserver(function (entries) {

    entries.forEach(function (entry) {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

}, {
    threshold: 0.15
});

cards.forEach(function (card) {

    observer.observe(card);

});


// 4. Back To Top Button

const topButton = document.createElement("button");

topButton.innerHTML = "↑";

topButton.className = "back-to-top";

topButton.setAttribute("aria-label", "Back to top");

document.body.appendChild(topButton);

window.addEventListener("scroll", function () {

    if (window.scrollY > 300) {

        topButton.classList.add("visible");

    } else {

        topButton.classList.remove("visible");

    }

});

topButton.addEventListener("click", function () {

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});


// 5. Current Year

const copyright = document.querySelector(".copyright p");

if (copyright) {

    copyright.innerHTML =
        "© " + new Date().getFullYear() +
        " CampusConnect. Built for students, powered by innovation.";

}


// 6. Navbar Active Link

const currentPath = window.location.pathname;

document.querySelectorAll("nav a").forEach(function (link) {

    if (link.getAttribute("href") === currentPath) {

        link.classList.add("active");

    }

});


// 7. Button Click Animation

document.querySelectorAll(".primary-btn, .secondary-btn, .cta-btn, .login-btn")
.forEach(function (button) {

    button.addEventListener("click", function () {

        this.style.opacity = "0.8";

        setTimeout(() => {

            this.style.opacity = "1";

        }, 200);

    });

});