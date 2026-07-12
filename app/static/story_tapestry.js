(() => {
  const svgNS = "http://www.w3.org/2000/svg";
  const random = (min, max) => Math.random() * (max - min) + min;

  document.querySelectorAll("[data-story-tapestry]").forEach((widget) => {
    const stage = widget.querySelector("[data-tapestry-stage]");
    const canvas = widget.querySelector("[data-tapestry-particles]");
    const svg = widget.querySelector("[data-tapestry-svg]");
    const cursor = widget.querySelector("[data-tapestry-cursor]");
    const tooltip = widget.querySelector("[data-tapestry-tooltip]");
    const tooltipType = widget.querySelector("[data-tapestry-tooltip-type]");
    const tooltipTitle = widget.querySelector("[data-tapestry-tooltip-title]");
    const tooltipCopy = widget.querySelector("[data-tapestry-tooltip-copy]");
    const tooltipLink = widget.querySelector("[data-tapestry-tooltip-link]");
    const countLabel = widget.querySelector("[data-tapestry-count]");
    const footerCount = widget.querySelector("[data-tapestry-footer-count]");
    const itemNodes = Array.from(widget.querySelectorAll("[data-tapestry-item]"));
    const relationNodes = Array.from(widget.querySelectorAll("[data-tapestry-relation]"));
    const ctx = canvas?.getContext("2d");
    if (!stage || !canvas || !svg || !ctx) return;

    const items = itemNodes.map((node) => ({ ...node.dataset }));
    const itemMap = new Map(items.map((item) => [item.id, item]));
    const relations = relationNodes.map((node) => ({ ...node.dataset })).filter((relation) => itemMap.has(relation.source) && itemMap.has(relation.target));
    const visibleItems = items.slice(0, window.innerWidth < 768 ? 5 : 8);
    const colors = { Character: "139,92,246", Faction: "94,234,212", Event: "251,191,36" };
    let width = 1;
    let height = 1;
    let particles = [];
    let threads = [];
    let fragmentElements = [];
    let frame = 0;
    let pointer = { x: -999, y: -999, active: false };

    const fragmentPositions = [
      [15, 18], [72, 13], [32, 35], [58, 46],
      [17, 62], [77, 66], [42, 77], [66, 87]
    ];

    const fitCanvas = () => {
      const rect = stage.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = Math.max(1, rect.width);
      height = Math.max(1, rect.height);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      particles = Array.from({ length: width < 400 ? 24 : 40 }, () => ({
        x: random(0, width), y: random(0, height),
        vx: random(-.08, .08), vy: random(-.08, .08),
        radius: random(.6, 1.55), alpha: random(.18, .6),
        color: Math.random() < .55 ? "139,92,246" : "94,234,212"
      }));
    };

    const relationStory = (relation) => {
      const source = itemMap.get(relation.source);
      const target = itemMap.get(relation.target);
      if (!source || !target) return null;
      return {
        type: relation.type.replaceAll("_", " "),
        title: `${source.name} → ${target.name}`,
        copy: relation.copy || `${source.name} ${relation.type.replaceAll("_", " ")} ${target.name}.`,
        href: source.href
      };
    };

    const makeThreadData = () => {
      const stories = relations.length ? relations : visibleItems.slice(1).map((item, index) => ({
        source: visibleItems[index]?.id,
        target: item.id,
        type: "world_thread",
        copy: "A developing thread in this world."
      }));
      const templates = [
        [28, 20, 24, 13, 54, 31, 80, 12], [50, 55, 20, 62, 50, 43, 78, 58],
        [70, 62, 22, 54, 48, 79, 75, 60], [16, 84, 28, 92, 62, 72, 88, 90],
        [40, 34, 16, 26, 58, 50, 92, 38], [85, 30, 72, 12, 38, 42, 6, 22],
        [10, 58, 35, 44, 55, 68, 94, 76], [90, 52, 67, 38, 43, 62, 7, 72],
        [30, 6, 44, 23, 62, 18, 74, 96], [4, 92, 30, 72, 68, 84, 96, 18]
      ];
      threads = Array.from({ length: Math.max(10, stories.length) }, (_, index) => {
        const template = templates[index % templates.length];
        const story = stories[index % Math.max(stories.length, 1)] || null;
        return {
          startX: template[0] / 100 * width,
          startY: template[1] / 100 * height,
          c1x: template[2] / 100 * width,
          c1y: template[3] / 100 * height,
          c2x: template[4] / 100 * width,
          c2y: template[5] / 100 * height,
          endX: template[6] / 100 * width,
          endY: template[7] / 100 * height,
          original: template,
          story,
          color: index % 3,
          width: random(.75, 1.3),
          speed: random(7, 15)
        };
      });
    };

    const addGradient = (defs, id, stops) => {
      const gradient = document.createElementNS(svgNS, "linearGradient");
      gradient.id = id;
      gradient.setAttribute("x1", "0%"); gradient.setAttribute("x2", "100%");
      stops.forEach(([offset, color, opacity]) => {
        const stop = document.createElementNS(svgNS, "stop");
        stop.setAttribute("offset", offset); stop.setAttribute("stop-color", color); stop.setAttribute("stop-opacity", opacity);
        gradient.appendChild(stop);
      });
      defs.appendChild(gradient);
    };

    const pathFor = (thread) => `M ${thread.startX} ${thread.startY} C ${thread.c1x} ${thread.c1y}, ${thread.c2x} ${thread.c2y}, ${thread.endX} ${thread.endY}`;

    const drawThreads = () => {
      svg.replaceChildren();
      const defs = document.createElementNS(svgNS, "defs");
      addGradient(defs, "zt-thread-violet", [["0%", "#8b5cf6", ".3"], ["50%", "#c4b5fd", ".62"], ["100%", "#5eead4", ".28"]]);
      addGradient(defs, "zt-thread-teal", [["0%", "#5eead4", ".28"], ["48%", "#8b5cf6", ".58"], ["100%", "#c4b5fd", ".34"]]);
      addGradient(defs, "zt-thread-gold", [["0%", "#c4b5fd", ".3"], ["52%", "#fbbf24", ".38"], ["100%", "#8b5cf6", ".38"]]);
      svg.appendChild(defs);
      threads.forEach((thread, index) => {
        const path = document.createElementNS(svgNS, "path");
        path.setAttribute("d", pathFor(thread));
        path.setAttribute("stroke", `url(#zt-thread-${["violet", "teal", "gold"][thread.color]})`);
        path.setAttribute("stroke-width", thread.width);
        path.classList.add("zt-thread");
        path.style.animationDuration = `${thread.speed}s`;
        path.dataset.threadIndex = String(index);
        svg.appendChild(path);
      });
    };

    const showTooltip = (story, x, y) => {
      if (!story || !tooltip) return;
      const data = story.source ? relationStory(story) : story;
      if (!data) return;
      tooltipType.textContent = data.type || "World fragment";
      tooltipTitle.textContent = data.title;
      tooltipCopy.textContent = data.copy;
      tooltipLink.href = data.href || "#";
      tooltip.style.left = `${Math.min(width - 238, Math.max(8, x + 12))}px`;
      tooltip.style.top = `${Math.min(height - 148, Math.max(8, y - 36))}px`;
      tooltip.hidden = false;
    };

    const drawFragments = () => {
      fragmentElements.forEach((element) => element.remove());
      fragmentElements = [];
      visibleItems.forEach((item, index) => {
        const [x, y] = fragmentPositions[index];
        const button = document.createElement("button");
        button.type = "button";
        button.className = "zt-word-fragment";
        button.style.left = `${x}%`;
        button.style.top = `${y}%`;
        button.style.setProperty("--zt-fragment-color", colors[item.kind] || "196,181,253");
        button.style.setProperty("--zt-fragment-delay", `${index * 80}ms`);
        button.textContent = item.name;
        button.addEventListener("click", (event) => {
          event.stopPropagation();
          showTooltip({ type: item.kind, title: item.name, copy: item.copy, href: item.href }, x / 100 * width, y / 100 * height);
        });
        stage.appendChild(button);
        fragmentElements.push(button);
      });
    };

    const distanceToThread = (x, y, thread) => {
      let minimum = Infinity;
      for (let step = 0; step <= 20; step += 1) {
        const t = step / 20;
        const mt = 1 - t;
        const px = mt ** 3 * thread.startX + 3 * mt ** 2 * t * thread.c1x + 3 * mt * t ** 2 * thread.c2x + t ** 3 * thread.endX;
        const py = mt ** 3 * thread.startY + 3 * mt ** 2 * t * thread.c1y + 3 * mt * t ** 2 * thread.c2y + t ** 3 * thread.endY;
        minimum = Math.min(minimum, Math.hypot(x - px, y - py));
      }
      return minimum;
    };

    const updateThreadInteraction = () => {
      const paths = svg.querySelectorAll(".zt-thread");
      if (!pointer.active) {
        paths.forEach((path) => path.classList.remove("is-near", "is-far"));
        return;
      }
      const distances = threads.map((thread, index) => ({ index, distance: distanceToThread(pointer.x, pointer.y, thread) })).sort((a, b) => a.distance - b.distance);
      const nearby = new Set(distances.filter((entry, index) => index < 3 && entry.distance < 170).map((entry) => entry.index));
      paths.forEach((path, index) => {
        path.classList.toggle("is-near", nearby.has(index));
        path.classList.toggle("is-far", nearby.size > 0 && !nearby.has(index));
      });
      fragmentElements.forEach((element) => {
        const x = parseFloat(element.style.left) / 100 * width;
        const y = parseFloat(element.style.top) / 100 * height;
        element.classList.toggle("is-near", Math.hypot(pointer.x - x, pointer.y - y) < 90);
      });
    };

    const animateParticles = () => {
      ctx.clearRect(0, 0, width, height);
      particles.forEach((particle) => {
        if (pointer.active) {
          const dx = pointer.x - particle.x;
          const dy = pointer.y - particle.y;
          const distance = Math.hypot(dx, dy);
          if (distance < 110 && distance > 0) {
            const force = (110 - distance) / 110 * .012;
            particle.vx += dx / distance * force;
            particle.vy += dy / distance * force;
          }
        }
        particle.vx *= .986; particle.vy *= .986;
        particle.vx += random(-.006, .006); particle.vy += random(-.006, .006);
        particle.x += particle.vx; particle.y += particle.vy;
        if (particle.x < -4) particle.x = width + 4;
        if (particle.x > width + 4) particle.x = -4;
        if (particle.y < -4) particle.y = height + 4;
        if (particle.y > height + 4) particle.y = -4;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${particle.color},${particle.alpha})`;
        ctx.fill();
      });
      updateThreadInteraction();
      frame = requestAnimationFrame(animateParticles);
    };

    const ripple = (x, y) => {
      const ring = document.createElement("span");
      ring.className = "zt-ripple";
      ring.style.left = `${x}px`; ring.style.top = `${y}px`;
      stage.appendChild(ring);
      window.setTimeout(() => ring.remove(), 1050);
    };

    const rebuild = () => {
      fitCanvas();
      makeThreadData();
      drawThreads();
      drawFragments();
      if (countLabel) countLabel.textContent = `${relations.length || threads.length} threads woven`;
      if (footerCount) footerCount.textContent = `Woven from ${visibleItems.length} fragments`;
    };

    stage.addEventListener("pointermove", (event) => {
      const rect = stage.getBoundingClientRect();
      pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top, active: true };
      cursor.style.left = `${pointer.x}px`; cursor.style.top = `${pointer.y}px`;
      cursor.classList.add("is-visible");
    });
    stage.addEventListener("pointerleave", () => { pointer.active = false; cursor.classList.remove("is-visible"); });
    stage.addEventListener("click", (event) => {
      const rect = stage.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      ripple(x, y);
      const closest = threads.map((thread) => ({ thread, distance: distanceToThread(x, y, thread) })).sort((a, b) => a.distance - b.distance)[0];
      if (closest?.distance < 20 && closest.thread.story) showTooltip(closest.thread.story, x, y);
      else if (tooltip) tooltip.hidden = true;
    });
    widget.querySelector("[data-tapestry-close]")?.addEventListener("click", () => { tooltip.hidden = true; });
    widget.querySelector("[data-tapestry-weave]")?.addEventListener("click", () => {
      stage.classList.add("is-weaving");
      window.setTimeout(() => { rebuild(); stage.classList.remove("is-weaving"); }, 300);
    });

    const observer = new ResizeObserver(() => rebuild());
    observer.observe(stage);
    cancelAnimationFrame(frame);
    animateParticles();
    window.addEventListener("pagehide", () => { observer.disconnect(); cancelAnimationFrame(frame); }, { once: true });
  });
})();
