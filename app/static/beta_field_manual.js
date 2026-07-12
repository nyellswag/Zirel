(() => {
  const root = document.querySelector("[data-beta-manual]");
  if (!root) return;

  const cursorGlow = root.querySelector(".bfm-cursor-glow");
  const cursorDot = root.querySelector(".bfm-cursor-dot");
  let mouseX = innerWidth / 2;
  let mouseY = innerHeight / 2;
  let glowX = mouseX;
  let glowY = mouseY;
  root.addEventListener("mousemove", event => {
    mouseX = event.clientX;
    mouseY = event.clientY;
    cursorDot.style.left = `${mouseX}px`;
    cursorDot.style.top = `${mouseY}px`;
  });
  const animateCursor = () => {
    glowX += (mouseX - glowX) * .12;
    glowY += (mouseY - glowY) * .12;
    cursorGlow.style.left = `${glowX}px`;
    cursorGlow.style.top = `${glowY}px`;
    requestAnimationFrame(animateCursor);
  };
  animateCursor();
  root.querySelectorAll("a,button,input,textarea,select").forEach(element => {
    element.addEventListener("mouseenter", () => { cursorDot.style.transform = "translate(-50%,-50%) scale(2)"; });
    element.addEventListener("mouseleave", () => { cursorDot.style.transform = "translate(-50%,-50%) scale(1)"; });
  });

  const capabilities = [
    ["01", "Private projects", "Create protected workspaces tied to your account."],
    ["02", "Core entities", "Organize characters, factions, events, and their details."],
    ["03", "Typed relations", "Connect records with explicit, readable relationship types."],
    ["04", "Logic warnings", "Review five rule-based consistency checks with explanations."],
    ["05", "Graph workspace", "Explore your world through Zirel's constellation-style view."],
    ["06", "JSON portability", "Export and import projects for transfer and independent backups."]
  ];
  const capGrid = root.querySelector("[data-beta-capabilities]");
  const pinCount = root.querySelector("[data-beta-pin-state] strong");
  const pinned = new Set();
  capabilities.forEach(([number, title, body], index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "bfm-cap";
    button.setAttribute("aria-expanded", "false");
    button.dataset.pinned = "false";
    button.innerHTML = `<span>${number}</span><h3>${title}</h3><p>${body}</p><small>Pin capability <i>+</i></small>`;
    button.addEventListener("click", () => {
      if (!button.classList.contains("is-open")) {
        button.classList.add("is-open");
        button.setAttribute("aria-expanded", "true");
        return;
      }
      if (pinned.has(index)) {
        pinned.delete(index);
        button.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      } else if (pinned.size < 3) pinned.add(index); else return;
      const isPinned = pinned.has(index);
      button.classList.toggle("is-pinned", isPinned);
      button.dataset.pinned = String(isPinned);
      pinCount.textContent = String(pinned.size);
    });
    capGrid.append(button);
  });

  const steps = ["Create a project named Test World", "Add two characters", "Add one faction and one event", "Create three to five typed relations", "Open Logic Warnings and read an explanation", "Inspect the project in Graph Workspace", "Export the project as JSON and send feedback"];
  const checklist = root.querySelector("[data-beta-checklist]");
  const mission = root.querySelector("[data-beta-mission]");
  steps.forEach((label, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "bfm-check";
    button.setAttribute("aria-pressed", "false");
    button.innerHTML = `<i aria-hidden="true"></i><span aria-hidden="true">0${index + 1}</span><b>${label}</b>`;
    button.addEventListener("click", () => {
      const done = button.getAttribute("aria-pressed") !== "true";
      button.setAttribute("aria-pressed", String(done));
      button.classList.toggle("is-done", done);
      const complete = [...checklist.children].every(item => item.classList.contains("is-done"));
      mission.classList.toggle("is-complete", complete);
      if (complete) fireConfetti();
    });
    checklist.append(button);
  });

  const timerText = root.querySelector("[data-beta-timer]");
  const timerButton = root.querySelector("[data-beta-timer-button]");
  const timerRing = root.querySelector("[data-beta-timer-ring]");
  const duration = 600;
  const circumference = 2 * Math.PI * 58;
  let remaining = duration;
  let timerId = null;
  timerRing.style.strokeDasharray = String(circumference);
  const paintTimer = () => {
    timerText.textContent = `${String(Math.floor(remaining / 60)).padStart(2, "0")}:${String(remaining % 60).padStart(2, "0")}`;
    timerRing.style.strokeDashoffset = String(circumference * (1 - remaining / duration));
  };
  timerButton.addEventListener("click", () => {
    if (remaining === 0) { remaining = duration; paintTimer(); timerButton.textContent = "Start test"; return; }
    if (timerId) { clearInterval(timerId); timerId = null; timerButton.textContent = "Resume test"; return; }
    timerButton.textContent = "Pause test";
    timerId = setInterval(() => {
      remaining -= 1; paintTimer();
      if (remaining === 0) { clearInterval(timerId); timerId = null; timerButton.textContent = "Reset timer"; }
    }, 1000);
  });
  paintTimer();

  const fireConfetti = () => {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const container = root.querySelector("[data-beta-confetti]");
    const colors = ["#8b5cf6", "#6366f1", "#38bdf8", "#22c55e", "#fbbf24"];
    for (let index = 0; index < 48; index += 1) {
      const piece = document.createElement("i");
      piece.style.left = `${Math.random() * 100}%`;
      piece.style.background = colors[index % colors.length];
      piece.style.animationDuration = `${2.2 + Math.random() * 2}s`;
      piece.style.animationDelay = `${Math.random() * .45}s`;
      container.append(piece);
      setTimeout(() => piece.remove(), 4700);
    }
  };

  const limitations = [
    ["Account controls", "medium", "Account management is intentionally limited, including no self-service account deletion yet."],
    ["Consistency coverage", "medium", "Warnings cover five explainable rules and may miss issues. Creative judgment remains yours."],
    ["Artificial intelligence", "low", "AI is not an active core feature of the current product."],
    ["Early beta changes", "medium", "Availability, interface details, and product direction may evolve after testing."],
    ["Long-term storage", "high", "Treat JSON export as part of your routine and keep independent copies of important projects."]
  ];
  const accordion = root.querySelector("[data-beta-limitations]");
  limitations.forEach(([title, severity, body], index) => {
    const item = document.createElement("article");
    item.className = "bfm-limit";
    item.dataset.severity = severity;
    const bodyId = `beta-limit-${index}`;
    item.innerHTML = `<button type="button" aria-expanded="false" aria-controls="${bodyId}"><i aria-hidden="true"></i><span>${severity}</span><b>${title}</b><em aria-hidden="true">⌄</em></button><div id="${bodyId}" hidden><p>${body}</p></div>`;
    const button = item.querySelector("button");
    const panel = item.querySelector("div");
    button.addEventListener("click", () => {
      const open = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(open));
      panel.hidden = false;
      item.classList.toggle("is-open", open);
    });
    accordion.append(item);
  });

  const copyButton = root.querySelector("[data-beta-copy]");
  const copyStatus = root.querySelector("[data-beta-copy-status]");
  copyButton.addEventListener("click", async () => {
    const reminder = "Export important Zirel projects as JSON regularly and keep an independent backup.";
    try {
      await navigator.clipboard.writeText(reminder);
      copyStatus.textContent = "Copied";
      copyButton.textContent = "Reminder copied";
    } catch (_) {
      copyStatus.textContent = "Copy unavailable";
    }
  });

  const chapters = [...root.querySelectorAll("section[id]")];
  const navLinks = [...root.querySelectorAll(".bfm-side-nav a")];
  const progress = root.querySelector("[data-beta-progress]");
  const updateScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
    let active = chapters[0].id;
    chapters.forEach(section => { if (section.getBoundingClientRect().top <= innerHeight * 0.42) active = section.id; });
    navLinks.forEach(link => link.classList.toggle("is-active", link.hash === `#${active}`));
  };
  addEventListener("scroll", updateScroll, { passive: true });
  addEventListener("resize", updateScroll);
  updateScroll();

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add("is-visible"); });
  }, { threshold: .06, rootMargin: "0px 0px -60px 0px" });
  root.querySelectorAll(".bfm-chapter").forEach(chapter => observer.observe(chapter));

  const messages = [["AUTH", "Project ownership checks active"], ["LOGIC", "Five explainable rules ready"], ["GRAPH", "Constellation workspace available"], ["PORTABLE", "JSON export and import ready"]];
  const feed = root.querySelector("[data-beta-feed]");
  let messageIndex = 0;
  let charIndex = 0;
  let deleting = false;
  const updateFeed = () => {
    const [tag, line] = messages[messageIndex];
    charIndex += deleting ? -1 : 1;
    feed.innerHTML = `<p><b>${tag}</b><span>${line.slice(0, charIndex)}</span><i></i></p>`;
    if (!deleting && charIndex >= line.length) { deleting = true; setTimeout(updateFeed, 1500); return; }
    if (deleting && charIndex <= 0) { deleting = false; messageIndex = (messageIndex + 1) % messages.length; }
    setTimeout(updateFeed, deleting ? 28 : 65);
  };
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reducedMotion) updateFeed(); else feed.innerHTML = `<p><b>STATUS</b><span>Working MVP · feedback open</span></p>`;

  const wave = root.querySelector("[data-beta-wave]");
  let waveTick = 0;
  const drawWave = () => {
    const points = [];
    for (let x = 0; x <= 520; x += 10) {
      const envelope = Math.sin(Math.PI * x / 520);
      const y = 30 + Math.sin(x * 0.095 + waveTick) * 12 * envelope + Math.sin(x * 0.031 - waveTick) * 5;
      points.push(`${x === 0 ? "M" : "L"}${x},${y.toFixed(1)}`);
    }
    wave.setAttribute("d", points.join(" "));
    waveTick += 0.055;
    requestAnimationFrame(drawWave);
  };
  if (reducedMotion) wave.setAttribute("d", "M0,30 L90,30 L110,18 L130,42 L150,30 L520,30"); else drawWave();
})();
