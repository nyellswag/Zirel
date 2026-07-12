(() => {
  const page = document.querySelector("[data-import-project]");
  if (!page) return;
  const input = page.querySelector("[data-import-input]");
  const dropzone = page.querySelector("[data-import-dropzone]");
  const title = page.querySelector("[data-import-title]");
  const meta = page.querySelector("[data-import-meta]");
  const status = page.querySelector("[data-import-status]");
  const submit = page.querySelector("[data-import-submit]");

  const renderFile = () => {
    const file = input.files?.[0];
    const valid = Boolean(file && (file.name.toLowerCase().endsWith(".json") || file.type === "application/json"));
    dropzone.classList.toggle("has-file", valid);
    dropzone.classList.toggle("has-error", Boolean(file && !valid));
    title.textContent = file ? file.name : "Choose a Zirel JSON file";
    meta.textContent = file ? `${Math.max(1, Math.round(file.size / 1024))} KB · ${valid ? "Ready to import" : "Unsupported file"}` : "Drop it here or click to browse · .json only";
    status.querySelector("span").textContent = valid ? "File selected and ready" : file ? "Choose a .json export file" : "No file selected";
    status.classList.toggle("is-ready", valid);
    submit.disabled = !valid;
  };

  ["dragenter", "dragover"].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
    event.preventDefault(); dropzone.classList.add("is-dragging");
  }));
  ["dragleave", "drop"].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
    event.preventDefault(); dropzone.classList.remove("is-dragging");
  }));
  dropzone.addEventListener("drop", (event) => {
    if (!event.dataTransfer?.files?.length) return;
    input.files = event.dataTransfer.files;
    renderFile();
  });
  input.addEventListener("change", renderFile);
  renderFile();
})();
