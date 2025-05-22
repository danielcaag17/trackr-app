document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".stats-toggle-btn");

    toggleButtons.forEach(button => {
        const targetId = button.getAttribute("data-target");
        const panel = document.getElementById(targetId);

        if (!panel) return;

        button.addEventListener("click", () => {
            const isExpanded = button.getAttribute("aria-expanded") === "true";

            // Toggle classes
            panel.classList.toggle("open");
            panel.classList.toggle("collapsed");

            // Update aria-expanded
            button.setAttribute("aria-expanded", (!isExpanded).toString());

            // Opcional: Cambiar el texto del botón
            const showText = button.getAttribute("data-show-text") || "Show details";
            const hideText = button.getAttribute("data-hide-text") || "Hide details";
            button.textContent = isExpanded ? showText : hideText;
        });
    });
});
