(() => {
  const KEY = "zirel_cookie_consent_v1";
  const GA_ID = "G-9JG8J2FMPP";
  const banner = document.querySelector("[data-cookie-consent]");
  const modal = document.querySelector("[data-cookie-modal]");
  const analyticsToggle = document.querySelector("[data-cookie-analytics]");
  let analyticsLoaded = false;

  const readChoice = () => {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (_) { return null; }
  };
  const loadAnalytics = () => {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){ window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("consent", "default", { analytics_storage: "granted", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
    window.gtag("config", GA_ID, { anonymize_ip: true });
    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(script);
  };
  const save = (analytics) => {
    localStorage.setItem(KEY, JSON.stringify({ necessary: true, analytics, updatedAt: new Date().toISOString() }));
    banner.hidden = true;
    modal.hidden = true;
    if (analytics) loadAnalytics();
  };
  const openSettings = () => {
    const choice = readChoice();
    analyticsToggle.checked = Boolean(choice && choice.analytics);
    modal.hidden = false;
  };

  document.querySelector("[data-cookie-accept]")?.addEventListener("click", () => save(true));
  document.querySelector("[data-cookie-reject]")?.addEventListener("click", () => save(false));
  document.querySelector("[data-cookie-customize]")?.addEventListener("click", openSettings);
  document.querySelectorAll("[data-cookie-settings]").forEach((button) => button.addEventListener("click", openSettings));
  document.querySelector("[data-cookie-close]")?.addEventListener("click", () => { modal.hidden = true; });
  document.querySelector("[data-cookie-save]")?.addEventListener("click", () => save(analyticsToggle.checked));
  modal?.addEventListener("click", (event) => { if (event.target === modal) modal.hidden = true; });

  const choice = readChoice();
  if (!choice) banner.hidden = false;
  else if (choice.analytics) loadAnalytics();
})();
