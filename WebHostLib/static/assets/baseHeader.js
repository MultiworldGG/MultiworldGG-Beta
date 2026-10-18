(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        // Mobile menu toggle
        const button = document.getElementById("base-header-mobile-menu-button");
        const menu = document.getElementById("base-header-mobile-menu");

        if (button && menu) {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                menu.classList.toggle("open");
            });

            // Close mobile menu when clicking outside
            document.addEventListener("click", function (e) {
                if (!menu.contains(e.target) && !button.contains(e.target)) {
                    menu.classList.remove("open");
                }
            });
        }

        // Mark current page in nav (best-effort match against pathname)
        const path = window.location.pathname;
        document.querySelectorAll(".nav-item").forEach(function (item) {
            const href = item.getAttribute("href");
            if (href && path.startsWith(href) && href !== "/") {
                item.classList.add("active");
            }
        });

        // Avatar active state when on /me
        if (path === "/me" || path.startsWith("/me/")) {
            document.querySelector(".nav-avatar")?.classList.add("active");
        }
    });
})();
