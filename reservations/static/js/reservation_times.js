(() => {
    "use strict";
    // Input element for the number of guests
    const gc = document.getElementById("guest_count");
    // Only enable time slots with space for the given number of guests
    function updateButtons() {
        const guest_count = Number.parseInt(gc.value)
        for (const button of document.querySelectorAll("td button")) {
            const div = button.firstChild
            button.disabled = isNaN(guest_count) || guest_count <= 0 || div.dataset.max < guest_count
        }
    }
    // Update the time slot buttons every time the user edits the guest count
    gc.addEventListener("input", updateButtons);
    // Update the buttons now (when the page is loading)
    updateButtons();
    // Attach deletion confirmation modal to the delete button
    const deleteReservation = document.getElementById("deleteReservation");
    if (deleteReservation) {
        deleteReservation.addEventListener("click", () => {
            const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
            deleteModal.show();
        });
    }
})();
