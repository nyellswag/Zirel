(() => {
  const form = document.querySelector("#beta-application-form");
  if (!form) return;
  const $ = selector => form.querySelector(selector);
  const out = name => document.querySelector(`[data-ba-${name}]`);
  const toast = document.querySelector("[data-ba-toast]");
  const draftKey = "zirel_beta_application_draft_v1";

  const value = name => form.elements[name]?.value?.trim() || "";
  const checked = name => form.querySelector(`[name="${name}"]:checked`)?.value || "";
  const tools = () => [...form.querySelectorAll('[name="current_tools"]:checked')].map(x => x.value);
  const showToast = text => { toast.textContent = text; toast.hidden = false; setTimeout(() => { toast.hidden = true; }, 2200); };
  const data = () => ({name:value("name"),email:value("email"),timezone:value("timezone"),role:checked("role"),experience:value("experience"),active_projects:value("active_projects"),frustration:value("frustration"),alpha_comfort:checked("alpha_comfort"),heard_from:value("heard_from"),beta_goal:value("beta_goal"),feedback_frequency:checked("feedback_frequency"),current_tools:tools(),application_terms:Boolean(form.elements.application_terms?.checked),product_updates:Boolean(form.elements.product_updates?.checked)});

  const update = () => {
    const d=data();
    out("avatar").textContent=d.name?.[0]?.toUpperCase()||"?";out("name").textContent=d.name||"—";out("email").textContent=d.email||"—";out("role").textContent=d.role||"—";out("timezone").textContent=d.timezone||"—";out("experience").textContent=d.experience||"—";out("projects").textContent=d.active_projects||"—";out("alpha").textContent=d.alpha_comfort||"—";out("feedback").textContent=d.feedback_frequency||"—";
    const copy=out("copy");copy.hidden=!d.frustration;out("frustration").textContent=d.frustration.length>130?d.frustration.slice(0,130)+"…":d.frustration;
    const toolWrap=out("tools-preview");toolWrap.hidden=!d.current_tools.length;toolWrap.querySelector("div").replaceChildren(...d.current_tools.map(t=>{const i=document.createElement("i");i.textContent=t;return i;}));
    const required=[d.name,d.email,d.role,d.experience,d.active_projects,d.frustration,d.alpha_comfort,d.beta_goal,d.feedback_frequency,d.application_terms];const optional=[d.timezone,d.heard_from,d.current_tools.length,d.product_updates];const score=Math.min(100,Math.round(required.filter(Boolean).length/required.length*85+optional.filter(Boolean).length/optional.length*15));out("strength").textContent=`${score}%`;out("strength-label").textContent=`${score}%`;out("strength-fill").style.width=`${score}%`;
  };
  form.querySelectorAll("textarea[maxlength]").forEach(ta=>{const counter=document.querySelector(`[data-counter-for="${ta.id}"]`);const count=()=>{counter.textContent=`${ta.value.length} / ${ta.maxLength}`;ta.style.height="auto";ta.style.height=`${ta.scrollHeight}px`;};ta.addEventListener("input",count);count();});
  form.addEventListener("input",update);form.addEventListener("change",update);
  document.querySelector("[data-ba-draft]")?.addEventListener("click",()=>{localStorage.setItem(draftKey,JSON.stringify(data()));showToast("Draft saved");});
  document.querySelector("[data-ba-discard]")?.addEventListener("click",event=>{const clear=()=>{form.reset();localStorage.removeItem(draftKey);update();showToast("Application cleared");};if(window.ZirelConfirm)window.ZirelConfirm.open({message:"Discard all entered application data?",acceptLabel:"Discard application",trigger:event.currentTarget,onConfirm:clear});else clear();});
  try{const d=JSON.parse(localStorage.getItem(draftKey)||"null");if(d){Object.entries(d).forEach(([key,val])=>{if(Array.isArray(val)){val.forEach(v=>{const el=form.querySelector(`[name="${key}"][value="${v}"]`);if(el)el.checked=true;});}else if(typeof val==="boolean"){if(form.elements[key])form.elements[key].checked=val;}else{const el=form.elements[key];if(el){if(el instanceof RadioNodeList){const radio=form.querySelector(`[name="${key}"][value="${val}"]`);if(radio)radio.checked=true;}else el.value=val;}}});}}
  catch(_){}
  update();
})();
