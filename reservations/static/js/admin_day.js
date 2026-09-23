/* jshint esversion: 6 */
/* global bootstrap */
(() => {
    "use strict";
    // Function to show the delete confirmation modal
    function confirmDelete (e) {
        const modalElement = document.getElementById("deleteModal");
        // Update the form to delete the correct reservation
        modalElement.querySelector("form").action = e.currentTarget.dataset.action;
        const deleteModal = new bootstrap.Modal(modalElement);
        deleteModal.show();
    }
    // Initialise the delete buttons
    for (const button of document.querySelectorAll("td button")) {
        // When a button is clicked disable all the buttons
        button.addEventListener("click", confirmDelete);
    }
})();
