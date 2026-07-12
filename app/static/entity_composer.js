(() => {
  const composers = document.querySelectorAll("[data-entity-composer]");

  composers.forEach((composer) => {
    const form = composer.querySelector("form");
    const nameInput = form?.querySelector('[name="name"]');
    const descriptionInput = form?.querySelector('[name="description"]');
    const previewName = composer.querySelector("[data-preview-name]");
    const previewDescription = composer.querySelector("[data-preview-description]");
    const previewMeta = composer.querySelector("[data-preview-meta]");
    const progress = composer.querySelector("[data-form-progress]");
    const progressText = composer.querySelector("[data-form-progress-text]");
    const watchedFields = form ? Array.from(form.querySelectorAll("input:not([type=hidden]), textarea, select")) : [];

    if (!form || !nameInput) return;

    const valueOr = (element, fallback) => element?.value.trim() || fallback;

    const update = () => {
      if (previewName) previewName.textContent = valueOr(nameInput, composer.dataset.nameFallback || "Untitled entity");
      if (previewDescription) {
        previewDescription.textContent = valueOr(
          descriptionInput,
          "Add a description to give this part of the world more context."
        );
      }

      const metaFields = (composer.dataset.metaFields || "")
        .split(",")
        .map((name) => name.trim())
        .filter(Boolean)
        .map((name) => form.querySelector(`[name="${name}"]`))
        .filter((field) => field && field.value.trim())
        .map((field) => {
          if (field.tagName === "SELECT") return field.options[field.selectedIndex]?.text.trim();
          return field.value.trim();
        });

      if (previewMeta) {
        previewMeta.textContent = metaFields.length ? metaFields.join("  /  ") : composer.dataset.metaFallback || "Details appear here";
      }

      const completed = watchedFields.filter((field) => field.value.trim()).length;
      const percent = watchedFields.length ? Math.round((completed / watchedFields.length) * 100) : 0;
      if (progress) progress.style.width = `${percent}%`;
      if (progressText) progressText.textContent = `${percent}% complete`;
    };

    watchedFields.forEach((field) => {
      field.addEventListener("input", update);
      field.addEventListener("change", update);
    });
    update();
  });
})();
