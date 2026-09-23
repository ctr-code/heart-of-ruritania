/* jshint esversion: 6 */
/* global bootstrap */
(() => {
    "use strict";
    // If the form is being submitted the buttons must be disabled
    var submitting = false;
    // Input element for the number of guests
    const gc = document.getElementById("guest_count");
    // Only enable time slots with space for the given number of guests
    function updateButtons() {
        const guest_count = Number.parseInt(gc.value);
        for (const button of document.querySelectorAll("td button")) {
            button.disabled = submitting || isNaN(guest_count) || guest_count <= 0 || button.dataset.max < guest_count;
        }
    }
    // Function to disable all the buttons and submit the form to the correct url
    function onSubmit (e) {
        submitting = true;
        updateButtons();
        const form = document.querySelector("form");
        form.action = e.currentTarget.formAction;
        form.submit();
    }
    // Initialise the buttons now (when the page is loading)
    for (const button of document.querySelectorAll("td button")) {
        // When a button is clicked disable all the buttons
        button.addEventListener("click", onSubmit);
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
