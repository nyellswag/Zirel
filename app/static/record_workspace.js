(() => {
  document.querySelectorAll("[data-record-workspace]").forEach((workspace) => {
    const collection = workspace.querySelector("[data-record-collection]");
    const viewButtons = workspace.querySelectorAll("[data-record-view]");
    const checkboxes = workspace.querySelectorAll('[data-record-checkbox]');
    const selectedCount = workspace.querySelector("[data-selected-count]");
    const bulkBar = workspace.querySelector("[data-bulk-bar]");

    viewButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const listView = button.dataset.recordView === "list";
        collection?.classList.toggle("is-list-view", listView);
        viewButtons.forEach((candidate) => candidate.classList.toggle("is-active", candidate === button));
      });
    });

    const updateSelection = () => {
      const count = Array.from(checkboxes).filter((checkbox) => checkbox.checked).length;
      if (selectedCount) selectedCount.textContent = String(count);
      bulkBar?.classList.toggle("has-selection", count > 0);
    };

    checkboxes.forEach((checkbox) => checkbox.addEventListener("change", updateSelection));
    updateSelection();
  });
})();
