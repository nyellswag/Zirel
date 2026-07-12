(() => {
  const root = document.querySelector("[data-faq]");
  if (!root) return;
  const items = [...root.querySelectorAll("[data-faq-item]")];
  const categories = [...root.querySelectorAll("[data-faq-category]")];
  const links = [...root.querySelectorAll(".zfq-sidebar nav a")];
  const progress = root.querySelector("[data-faq-progress]");
  const counter = root.querySelector("[data-faq-count]");
  const empty = root.querySelector("[data-faq-empty]");
  items.forEach(item => {
    const button = item.querySelector("button");
    const panel = item.querySelector("div");
    button.addEventListener("click", () => {
      const open = button.getAttribute("aria-expanded") !== "true";
      item.classList.toggle("is-open", open);
      button.setAttribute("aria-expanded", String(open));
      panel.hidden = false;
    });
  });
  const updateScroll = () => {
    const maximum = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${maximum > 0 ? scrollY / maximum : 0})`;
    let active = categories[0].id;
    categories.forEach(category => { if (!category.hidden && category.getBoundingClientRect().top <= innerHeight * .4) active = category.id; });
    links.forEach(link => link.classList.toggle("is-active", link.hash === `#${active}`));
  };
  addEventListener("scroll", updateScroll, { passive: true });
  addEventListener("resize", updateScroll);
  const search = root.querySelector("[data-faq-search]");
  const runSearch = () => {
    const query = search.value.toLowerCase().replace(/\s+/g, " ").trim();
    let visible = 0;
    categories.forEach(category => {
      let categoryVisible = 0;
      category.querySelectorAll("[data-faq-item]").forEach(item => {
        const match = !query || item.textContent.toLowerCase().includes(query);
        item.hidden = !match;
        if (match) { visible += 1; categoryVisible += 1; }
      });
      category.hidden = categoryVisible === 0;
    });
    counter.textContent = `${visible} question${visible === 1 ? "" : "s"}`;
    empty.hidden = visible !== 0;
    updateScroll();
  };
  search.addEventListener("input", runSearch);
  search.addEventListener("keydown", event => { if (event.key === "Escape") { search.value = ""; runSearch(); } });
  updateScroll();
})();
