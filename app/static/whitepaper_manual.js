(() => {
  const root = document.querySelector("[data-whitepaper]");
  if (!root) return;
  const progress = root.querySelector("[data-whitepaper-progress]");
  const sections = [...root.querySelectorAll(".zwp-content > section")];
  const tocItems = [...root.querySelectorAll("[data-whitepaper-item]")];
  const update = () => {
    const maximum = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${maximum > 0 ? scrollY / maximum : 0})`;
    let active = sections[0].id;
    sections.forEach(section => { if (section.getBoundingClientRect().top <= innerHeight * .4) active = section.id; });
    tocItems.forEach(item => item.classList.toggle("is-active", item.querySelector("a").hash === `#${active}`));
  };
  addEventListener("scroll", update, { passive: true });
  addEventListener("resize", update);
  update();
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) sections.forEach(section => section.classList.add("is-visible"));
  else {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add("is-visible"); }), { threshold: .08 });
    sections.forEach(section => observer.observe(section));
  }
})();
