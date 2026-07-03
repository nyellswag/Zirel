document.addEventListener("DOMContentLoaded", () => {
  const passwordInput = document.querySelector("#password");
  const meter = document.querySelector("[data-password-strength]");
  const label = document.querySelector("[data-strength-label]");

  if (!passwordInput || !meter || !label) {
    return;
  }

  const states = ["strength-weak", "strength-fair", "strength-good", "strength-strong"];

  function updateStrength() {
    const password = passwordInput.value;
    let score = 0;

    if (password.length >= 8) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/\d/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;

    meter.classList.remove(...states);

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
