(function () {
  const toggle = document.getElementById("imecx-avatar-toggle");
  const dropdown = document.getElementById("imecx-avatar-dropdown");
  if (!toggle || !dropdown) return;

  function openDropdown() {
    dropdown.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    dropdown.setAttribute("aria-hidden", "false");
  }

  function closeDropdown() {
    dropdown.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    dropdown.setAttribute("aria-hidden", "true");
  }

  toggle.addEventListener("click", (event) => {
    event.stopPropagation();
    const isOpen = dropdown.classList.contains("open");
    isOpen ? closeDropdown() : openDropdown();
  });

  document.addEventListener("click", (event) => {
    if (!dropdown.contains(event.target) && event.target !== toggle) {
      closeDropdown();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeDropdown();
  });
})();