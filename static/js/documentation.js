
const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("sidebarOverlay");

function openSidebar() {
    sidebar.classList.add("open");
    overlay.classList.add("show");
    menuToggle.setAttribute("aria-expanded", "true");
}

function closeSidebar() {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
    menuToggle.setAttribute("aria-expanded", "false");
}

menuToggle.addEventListener("click", () => {
    if (sidebar.classList.contains("open")) {
        closeSidebar();
    } else {
        openSidebar();
    }
});

overlay.addEventListener("click", closeSidebar);

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeSidebar();
    }
});
