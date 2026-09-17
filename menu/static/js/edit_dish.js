(() => {
    "use strict";
    const deleteDish = document.getElementById("deleteDish");
    if (deleteDish) {
        deleteDish.addEventListener("click", () => {
            const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
            deleteModal.show();
        });
    }
})();
