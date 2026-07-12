(function () {
  "use strict";
  var stage = document.querySelector("[data-creator-stage]");
  if (!stage) return;

  var roles = {
    writers: "A workspace for novels, series bibles, and ongoing sagas — keep characters, timelines, and threads coherent across a thousand pages.",
    gms: "Run tabletop campaigns that survive long seasons — keep NPCs, factions, hooks, events, and lore connected as the table changes the world.",
    worldbuilders: "Map cultures, histories, rules, characters, factions, and events as one connected world whose moving parts remain visible.",
    screenwriters: "Trace character arcs, turning points, relationships, and continuity across episodes without losing an important setup or consequence.",
    indie: "Structure narrative entities and connections, review contradictions, and keep portable project data while the game world evolves.",
    narrative: "Design connected story systems with explicit entities, relationships, events, and explainable warnings that remain open to creative judgment."
  };
  var tabs = stage.querySelector("[data-creator-tabs]");
  var chips = Array.from(tabs.querySelectorAll("[data-role]"));
  var pill = stage.querySelector("[data-creator-pill]");
  var copy = stage.querySelector("[data-creator-copy]");
  var headline = stage.querySelector("[data-creator-headline]");
  var spot = stage.querySelector("[data-creator-spot]");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function movePill(target, instant) {
    if (!target || window.matchMedia("(max-width: 1000px)").matches) return;
    var parent = tabs.getBoundingClientRect();
    var rect = target.getBoundingClientRect();
    if (instant) pill.style.transition = "none";
    pill.style.width = rect.width + "px";
    pill.style.transform = "translateX(" + (rect.left - parent.left - 6) + "px)";
    if (instant) requestAnimationFrame(function () { pill.style.transition = ""; });
  }
  function activate(chip) {
    chips.forEach(function (item) {
      var active = item === chip;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-selected", active ? "true" : "false");
    });
    movePill(chip, false);
    copy.classList.add("is-leaving");
    window.setTimeout(function () {
      copy.textContent = roles[chip.dataset.role] || "";
      copy.classList.remove("is-leaving");
    }, reduceMotion ? 0 : 180);
  }
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () { activate(chip); });
    chip.addEventListener("mouseenter", function () { movePill(chip, false); });
  });
  tabs.addEventListener("mouseleave", function () { movePill(tabs.querySelector(".is-active"), false); });
  window.addEventListener("resize", function () { movePill(tabs.querySelector(".is-active"), true); });
  requestAnimationFrame(function () { movePill(tabs.querySelector(".is-active"), true); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(tabs.querySelector(".is-active"), true); });

  if (!reduceMotion) {
    stage.addEventListener("mousemove", function (event) {
      var rect = stage.getBoundingClientRect();
      var x = event.clientX - rect.left;
      var y = event.clientY - rect.top;
      spot.style.left = x + "px";
      spot.style.top = y + "px";
      headline.style.transform = "translate3d(" + ((x / rect.width - .5) * 10) + "px," + ((y / rect.height - .5) * 7) + "px,0)";
    });
    stage.addEventListener("mouseleave", function () { headline.style.transform = "translate3d(0,0,0)"; });
  }
})();
