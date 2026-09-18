(() => {
    "use strict";

    function enableButtons() {
        // Enable/disable the up/down buttons according to their position
        for (const button of document.querySelectorAll(".menu-arrange-up")) {
            const tr = button.parentElement.parentElement;
            button.disabled = !tr.previousElementSibling;
        }
        for (const button of document.querySelectorAll(".menu-arrange-down")) {
            const tr = button.parentElement.parentElement;
            button.disabled = !tr.nextElementSibling;
        }
    }

    function swapOrders(tr1, tr2) {
        // Swap the hidden order values of two table rows

        // Get the input controls
        const input1 = tr1.querySelector("input");
        const input2 = tr2.querySelector("input");
        // Swap the values
        const value = input1.getAttribute("value");
        input1.setAttribute("value", input2.getAttribute("value"));
        input2.setAttribute("value", value);
    }

    // Need to move whole table rows so buttons can stay focused.

    for (const button of document.querySelectorAll(".menu-arrange-up")) {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const tr = e.currentTarget.parentElement.parentElement;
            const prev = tr.previousElementSibling;
            // Don't detach the current element to ensure its buttons can retain focus
            tr.parentElement.insertBefore(prev, tr.nextElementSibling);
            swapOrders(tr, prev);
            enableButtons();
        });
    }
    for (const button of document.querySelectorAll(".menu-arrange-down")) {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const tr = e.currentTarget.parentElement.parentElement;
            const next = tr.nextElementSibling;
            // Don't detach the current element to ensure its buttons can retain focus
            tr.parentElement.insertBefore(next, tr);
            swapOrders(tr, next);
            enableButtons();
        });
    }
    enableButtons();
})();
