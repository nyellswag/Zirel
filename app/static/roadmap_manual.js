(() => {
  const root = document.querySelector("[data-roadmap-manual]");
  if (!root) return;
  const progress = root.querySelector("[data-roadmap-progress]");
  const phases = [...root.querySelectorAll(".zrm-phase")];
  const links = [...root.querySelectorAll("[data-roadmap-link]")];
  const update = () => {
    const maximum = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${maximum > 0 ? scrollY / maximum : 0})`;
    let active = phases[0].id;
    phases.forEach(phase => { if (phase.getBoundingClientRect().top <= innerHeight * .48) active = phase.id; });
    links.forEach(link => link.classList.toggle("is-active", link.hash === `#${active}`));
  };
  addEventListener("scroll", update, { passive: true });
  addEventListener("resize", update);
  update();
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) phases.forEach(phase => phase.classList.add("is-visible"));
  else {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add("is-visible"); }), { threshold: .12 });
    phases.forEach(phase => observer.observe(phase));
  }
})();
