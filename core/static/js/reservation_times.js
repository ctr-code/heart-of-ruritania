(() => {
    "use strict";
    const gc = document.getElementById("guest_count");
    function updateButtons() {
        const group_count = Number.parseInt(gc.value)
        for (const div of document.querySelectorAll("td div")) {
            const button = div.firstChild
            button.disabled = isNaN(group_count) || group_count === 0 || div.dataset.max < group_count
        }
    }
    gc.addEventListener("input", updateButtons);
    window.addEventListener("load", updateButtons);
    const deleteReservation = document.getElementById("deleteReservation");
    if (deleteReservation) {
        deleteReservation.addEventListener("click", () => {
            const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
            deleteModal.show();
        });
    }
})();
