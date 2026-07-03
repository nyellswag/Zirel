document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-filter-list]").forEach((list) => {
    const searchInput = list.querySelector("[data-list-search]");
    const typeFilter = list.querySelector("[data-list-type-filter]");
    const severityFilter = list.querySelector("[data-list-severity-filter]");
    const categoryFilter = list.querySelector("[data-list-category-filter]");
    const roleFilter = list.querySelector("[data-list-role-filter]");
    const reasonFilter = list.querySelector("[data-list-reason-filter]");
    const items = Array.from(list.querySelectorAll("[data-list-item]"));
    const countDisplay = list.querySelector("[data-list-count]");
    const emptyState = list.querySelector("[data-list-empty]");
    const label = list.dataset.listLabel || "items";

    const applyFilters = () => {
      const query = (searchInput?.value || "").trim().toLowerCase();
      const selectedType = typeFilter?.value || "";
      const selectedSeverity = severityFilter?.value || "";
      const selectedCategory = categoryFilter?.value || "";
      const selectedRole = roleFilter?.value || "";
      const selectedReason = reasonFilter?.value || "";
      let visibleCount = 0;

      items.forEach((item) => {
        const searchText = (item.dataset.searchText || "").toLowerCase();
        const relationType = item.dataset.relationType || "";
        const severity = item.dataset.severity || "";
        const category = item.dataset.category || "";
        const role = item.dataset.role || "";
        const reason = item.dataset.reason || "";
        const matchesSearch = !query || searchText.includes(query);
        const matchesType = !selectedType || relationType === selectedType;
        const matchesSeverity = !selectedSeverity || severity === selectedSeverity;
        const matchesCategory = !selectedCategory || category === selectedCategory;
        const matchesRole = !selectedRole || role === selectedRole;
        const matchesReason = !selectedReason || reason === selectedReason;
        const isVisible = matchesSearch && matchesType && matchesSeverity && matchesCategory && matchesRole && matchesReason;

        item.hidden = !isVisible;
        if (isVisible) {
          visibleCount += 1;
        }
      });

      if (countDisplay) {
        countDisplay.textContent = `Showing ${visibleCount} of ${items.length} ${label}`;
      }

      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
    };

    searchInput?.addEventListener("input", applyFilters);
    typeFilter?.addEventListener("change", applyFilters);
    severityFilter?.addEventListener("change", applyFilters);
    categoryFilter?.addEventListener("change", applyFilters);
    roleFilter?.addEventListener("change", applyFilters);
    reasonFilter?.addEventListener("change", applyFilters);
    applyFilters();
  });
});
