(() => {
  document.querySelectorAll(".entity-composer-page").forEach(page => {
    const form = page.querySelector(".entity-composer-form");
    if (!form) return;
    form.querySelectorAll("textarea").forEach(textarea => {
      if (!textarea.maxLength || textarea.maxLength < 0) textarea.maxLength = 1000;
      const counter = document.createElement("small"); counter.className = "zec-counter";
      const update = () => { counter.textContent = `${textarea.value.length} / ${textarea.maxLength}`; };
      textarea.insertAdjacentElement("afterend", counter); textarea.addEventListener("input", update); update();
    });
    const actions = form.querySelector(".form-card-actions");
    if (actions) { const hint=document.createElement("span"); hint.className="zec-shortcut"; hint.innerHTML="Submit <kbd>Ctrl/Cmd + Enter</kbd>"; actions.append(hint); }
    const clearInvalid = field => { field.classList.remove("is-zec-invalid"); field.closest(".zf-select")?.classList.remove("is-zec-invalid"); };
    form.querySelectorAll("input,textarea,select").forEach(field => { field.addEventListener("input",()=>clearInvalid(field)); field.addEventListener("change",()=>clearInvalid(field)); });
    form.addEventListener("submit", event => {
      const invalid = [...form.querySelectorAll(":invalid")];
      if (!invalid.length) return;
      event.preventDefault();
      invalid.forEach(field => { field.classList.add("is-zec-invalid"); field.closest(".zf-select")?.classList.add("is-zec-invalid"); });
      const first = invalid[0]; const custom = first.closest(".zf-select")?.querySelector(".zf-select-button"); (custom || first).focus();
    });
    form.addEventListener("keydown", event => { if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) { event.preventDefault(); form.requestSubmit(); } });
  });
})();
