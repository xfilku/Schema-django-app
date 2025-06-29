document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebarAccordion');
    const openedId = localStorage.getItem('openSidebarSection');
    if (openedId) {
        const el = document.getElementById(openedId);
        if (el && el.classList.contains('collapse')) {
            new bootstrap.Collapse(el, { toggle: false }).show();
        }
    }
    sidebar.addEventListener('show.bs.collapse', function (event) {
        localStorage.setItem('openSidebarSection', event.target.id);
    });
    sidebar.addEventListener('hide.bs.collapse', function (event) {
        const current = localStorage.getItem('openSidebarSection');
        if (current === event.target.id) {
            localStorage.removeItem('openSidebarSection');
        }
    });
});