document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const resizer = document.getElementById("resizer");
    const lockBtn = document.getElementById("lock-resizer-btn");
    const lockIcon = document.getElementById("lock-icon");

    let isResizing = false;
    let isLocked = localStorage.getItem("resizerLocked") === "true";

    // Apply saved sidebar width
    const savedWidth = localStorage.getItem("sidebarWidth");
    if (savedWidth) {
        sidebar.style.width = savedWidth + "px";
    }

    // Apply lock state
    if (isLocked) {
        resizer.style.pointerEvents = "none";
        lockIcon.classList.remove("fa-lock-open");
        lockIcon.classList.add("fa-lock");
    }

    // Toggle lock button
    lockBtn.addEventListener("click", function () {
        isLocked = !isLocked;
        localStorage.setItem("resizerLocked", isLocked);

        if (isLocked) {
            resizer.style.pointerEvents = "none";
            lockIcon.classList.remove("fa-lock-open");
            lockIcon.classList.add("fa-lock");
        } else {
            resizer.style.pointerEvents = "auto";
            lockIcon.classList.remove("fa-lock");
            lockIcon.classList.add("fa-lock-open");
        }
    });

    // Resize logic
    resizer.addEventListener("mousedown", function (e) {
        if (isLocked) return;
        isResizing = true;
        document.body.style.cursor = "ew-resize";
    });

    document.addEventListener("mousemove", function (e) {
        if (!isResizing || isLocked) return;

        const newWidth = e.clientX;
        if (newWidth >= 200 && newWidth <= 500) {
            sidebar.style.width = newWidth + "px";
        }
    });

    document.addEventListener("mouseup", function () {
        if (isResizing) {
            localStorage.setItem("sidebarWidth", parseInt(sidebar.style.width));
        }
        isResizing = false;
        document.body.style.cursor = "default";
    });
});

function toggleFavoritesDropdown() {
    const el = document.getElementById("favorites-dropdown");
    el.style.display = (el.style.display === "none" || el.style.display === "") ? "block" : "none";
}

const toggleBtn = document.getElementById('favoriteToggle');
const sidebarAll = document.getElementById('sidebar-all');
const sidebarFavorites = document.getElementById('sidebar-favorites');

let showFavorites = false;

function toggleFavoritesView() {
    showFavorites = !showFavorites;
    sidebarAll.style.display = showFavorites ? 'none' : 'block';
    sidebarFavorites.style.display = showFavorites ? 'block' : 'none';

    toggleBtn.innerHTML = showFavorites
        ? '<i class="fa-solid fa-star text-warning"></i>'
        : '<i class="fa-regular fa-star"></i>';
}

toggleBtn?.addEventListener('click', toggleFavoritesView);
