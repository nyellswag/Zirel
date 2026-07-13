(() => {
  const selector = [".zv2-form-card select", ".entity-composer-form select", ".project-setup-form select", ".auth-form select", ".bfm-feedback-layout select", ".zba-ref-form select"].join(",");
  const closeAll = except => document.querySelectorAll(".zf-select.is-open").forEach(wrapper => { if (wrapper !== except) { wrapper.classList.remove("is-open"); wrapper.querySelector(".zf-select-button")?.setAttribute("aria-expanded", "false"); } });
  const enhance = select => {
    if (select.dataset.zfEnhanced || select.multiple) return;
    select.dataset.zfEnhanced = "true";
    const wrapper = document.createElement("div"); wrapper.className = "zf-select";
    const button = document.createElement("button"); button.type = "button"; button.className = "zf-select-button"; button.setAttribute("aria-haspopup", "listbox"); button.setAttribute("aria-expanded", "false");
    const menu = document.createElement("div"); menu.className = "zf-select-menu"; menu.setAttribute("role", "listbox");
    select.parentNode.insertBefore(wrapper, select); wrapper.append(select, button, menu); select.classList.add("zf-select-native"); select.setAttribute("aria-hidden","true"); select.tabIndex=-1;
    const render = () => {
      menu.replaceChildren();
      [...select.children].forEach(child => {
        if (child.tagName === "OPTGROUP") { const label=document.createElement("div"); label.className="zf-select-group"; label.textContent=child.label; menu.append(label); [...child.children].forEach(addOption); }
        else addOption(child);
      });
      const chosen=select.options[select.selectedIndex]; button.textContent=chosen?.textContent.trim() || "Choose an option"; button.setAttribute("aria-label",`${label?.textContent.trim() || "Select"}: ${button.textContent}`);
    };
    function addOption(option) { const item=document.createElement("button"); item.type="button"; item.className="zf-select-option"; item.role="option"; item.textContent=option.textContent.trim(); item.dataset.value=option.value; item.disabled=option.disabled; item.setAttribute("aria-selected",String(option.selected)); item.classList.toggle("is-selected",option.selected); item.addEventListener("click",()=>{select.value=option.value; select.dispatchEvent(new Event("change",{bubbles:true})); render(); closeAll(); button.focus();}); menu.append(item); }
    button.addEventListener("click",()=>{const open=!wrapper.classList.contains("is-open"); closeAll(wrapper); wrapper.classList.toggle("is-open",open); button.setAttribute("aria-expanded",String(open));});
    button.addEventListener("keydown",event=>{if(["ArrowDown","ArrowUp"].includes(event.key)){event.preventDefault();const options=[...menu.querySelectorAll(".zf-select-option:not(:disabled)")];const index=Math.max(0,options.findIndex(x=>x.classList.contains("is-selected")));const next=event.key==="ArrowDown"?Math.min(options.length-1,index+1):Math.max(0,index-1);select.value=options[next].dataset.value;select.dispatchEvent(new Event("change",{bubbles:true}));render();}if(event.key==="Escape"){closeAll();button.focus();}});
    const label = select.id ? document.querySelector(`label[for="${select.id}"]`) : null;
    label?.addEventListener("click", event => { event.preventDefault(); button.focus(); button.click(); });
    select.addEventListener("change",render); select.form?.addEventListener("reset",()=>setTimeout(render)); render();
  };
  document.querySelectorAll(selector).forEach(enhance);
  document.addEventListener("click",event=>{if(!event.target.closest(".zf-select"))closeAll();});
  document.addEventListener("keydown",event=>{if(event.key==="Escape")closeAll();});
})();
