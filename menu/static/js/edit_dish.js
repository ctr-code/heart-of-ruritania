/* jshint esversion: 6 */
/* global bootstrap */
(() => {
    "use strict";
    // If the delete button is present, show a confirmation modal when it is clicked
    const deleteDish = document.getElementById("deleteDish");
    if (deleteDish) {
        deleteDish.addEventListener("click", () => {
            const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
            deleteModal.show();
        });
    }
})();
