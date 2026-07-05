document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-password-toggle]").forEach((button) => {
    const target = document.querySelector(button.dataset.passwordToggle);
    if (!target) return;

    button.addEventListener("click", () => {
      const isVisible = target.type === "text";
      target.type = isVisible ? "password" : "text";
      button.classList.toggle("is-visible", !isVisible);
      button.setAttribute("aria-pressed", String(!isVisible));
      button.setAttribute("aria-label", isVisible ? "Show password" : "Hide password");
    });
  });

  const passwordInput = document.querySelector("#password");
  const meter = document.querySelector("[data-password-strength]");
  const label = document.querySelector("[data-strength-label]");
  const reqLength = document.querySelector('[data-password-req="length"]');
  const reqNumber = document.querySelector('[data-password-req="number"]');
  const reqUpper = document.querySelector('[data-password-req="upper"]');

  if (!passwordInput || !meter || !label) {
    return;
  }

  const states = ["strength-weak", "strength-fair", "strength-good", "strength-strong"];

  function updateStrength() {
    const password = passwordInput.value;
    const hasLength = password.length >= 8;
    const hasLowercase = /[a-z]/.test(password);
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);
    let score = 0;

    if (hasLength) score += 1;
    if (hasLowercase) score += 1;
    if (hasUppercase) score += 1;
    if (hasNumber) score += 1;
    if (hasSpecial) score += 1;

    meter.classList.remove(...states);
    if (reqLength) reqLength.classList.toggle("met", hasLength);
    if (reqNumber) reqNumber.classList.toggle("met", hasNumber || hasSpecial);
    if (reqUpper) reqUpper.classList.toggle("met", hasUppercase);

    if (!password) {
      label.textContent = "Enter password";
      return;
    }

    if (score <= 2) {
      meter.classList.add("strength-weak");
      label.textContent = "Weak";
    } else if (score === 3) {
      meter.classList.add("strength-fair");
      label.textContent = "Fair";
    } else if (score === 4) {
      meter.classList.add("strength-good");
      label.textContent = "Good";
    } else {
      meter.classList.add("strength-strong");
      label.textContent = "Strong";
    }
  }

  passwordInput.addEventListener("input", updateStrength);
  updateStrength();
});
