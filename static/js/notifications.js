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