document.addEventListener("DOMContentLoaded", () => {

    const messages = document.querySelectorAll('.message:not(.persistent)');

    messages.forEach((msg, index) => {

        setTimeout(() => {

            msg.style.opacity = "0";
            msg.style.transform = "translateY(-8px)";

            setTimeout(() => msg.remove(), 300);

        }, 4000 + index * 300);

    });

});

const notificationToggle =
    document.getElementById("notificationToggle");

const notificationDropdown =
    document.getElementById("notificationDropdown");

if (notificationToggle && notificationDropdown) {

    notificationToggle.addEventListener(
        "click",
        function (e) {

            e.stopPropagation();

            notificationDropdown.classList.toggle(
                "is-open"
            );
        }
    );

    notificationDropdown.addEventListener(
        "click",
        function (e) {
            e.stopPropagation();
        }
    );

    document.addEventListener(
        "click",
        function () {

            notificationDropdown.classList.remove(
                "is-open"
            );
        }
    );
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

document.addEventListener("DOMContentLoaded", function () {

    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
    const csrftoken = csrfInput ? csrfInput.value : null;

    const dropdown = document.getElementById("notificationDropdown");

    if (dropdown) {
        dropdown.addEventListener("click", function (event) {

            const dismissBtn = event.target.closest("[data-mark-read-url]");

            if (dismissBtn) {
                const url = dismissBtn.dataset.markReadUrl;
                const item = dismissBtn.closest(".notification-item");

                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                }).then(function (response) {
                    if (response.ok && item) {
                        item.remove();

                        const badge = document.querySelector(".notification-count");
                        if (badge) {
                            const current = parseInt(badge.textContent.trim(), 10) || 0;
                            const updated = current - 1;

                            if (updated > 0) {
                                badge.textContent = updated;
                            } else {
                                badge.remove();
                            }
                        }
                    }
                });
            }

            const markAllBtn = event.target.closest("[data-mark-all-url]");

            if (markAllBtn) {
                const url = markAllBtn.dataset.markAllUrl;

                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                }).then(function (response) {
                    if (response.ok) {
                        document.querySelectorAll(".notification-item").forEach(function (item) {
                            item.remove();
                        });

                        const badge = document.querySelector(".notification-count");
                        if (badge) badge.remove();

                        markAllBtn.remove();
                    }
                });
                
            }

        });
    }

});