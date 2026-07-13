(() => {
  const modal = document.querySelector("[data-zconfirm]");
  if (!modal) return;
  const messageNode = modal.querySelector("[data-zconfirm-message]");
  const accept = modal.querySelector("[data-zconfirm-accept]");
  let callback = null;
  let returnFocus = null;
  const close = () => { modal.hidden = true; callback = null; returnFocus?.focus?.(); };
  const open = ({ message, onConfirm, trigger, acceptLabel = "Delete permanently" }) => {
    callback = onConfirm; returnFocus = trigger || document.activeElement;
    messageNode.textContent = message || "This action cannot be undone.";
    accept.textContent = acceptLabel; modal.hidden = false; accept.focus();
  };
  window.ZirelConfirm = { open, close };
  modal.querySelectorAll("[data-zconfirm-cancel]").forEach(button => button.addEventListener("click", close));
  accept.addEventListener("click", () => { const action = callback; modal.hidden = true; callback = null; action?.(); });
  modal.addEventListener("click", event => { if (event.target === modal) close(); });
  document.addEventListener("keydown", event => { if (!modal.hidden && event.key === "Escape") close(); });

  const extract = source => source?.match(/confirm\((['"])(.*?)\1\)/)?.[2] || "Delete this item permanently?";
  document.querySelectorAll('form[onsubmit*="confirm("]').forEach(form => {
    const message = extract(form.getAttribute("onsubmit")); form.removeAttribute("onsubmit");
    form.addEventListener("submit", event => { event.preventDefault(); open({message, trigger:event.submitter, onConfirm:()=>form.submit()}); });
  });
  document.querySelectorAll('[onclick*="confirm("]').forEach(button => {
    const message = extract(button.getAttribute("onclick")); button.removeAttribute("onclick");
    button.addEventListener("click", event => {
      event.preventDefault(); const form = button.form || document.getElementById(button.getAttribute("form")); if (!form) return;
      open({message, trigger:button, onConfirm:()=>{ if (button.formAction) form.action=button.formAction; form.submit(); }});
    });
  });
})();
