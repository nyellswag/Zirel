(() => {
  document.querySelectorAll("[data-public-form]").forEach(page => {
    const message=page.querySelector("[data-form-message]");
    const counter=page.querySelector("[data-form-counter]");
    if(message&&counter){const update=()=>{counter.textContent=`${message.value.length} / ${message.maxLength||1000}`;message.style.height="auto";message.style.height=`${Math.max(140,message.scrollHeight)}px`;};message.addEventListener("input",update);update();}

    const reason=page.querySelector("[data-contact-reason]");
    const context=page.querySelector("[data-contact-context]");
    if(!reason||!context)return;
    const content={
      "General question":["General inquiry","Tell us what you need.","A short explanation of your question and the outcome you want is enough to begin.",["What you are trying to do","Where you need clarification","How we can respond"]],
      "Beta access":["Beta access","Tell us how you want to test Zirel.","Explain your workflow and what kind of fictional world you would use during the closed beta.",["Your creator role","The project you want to test","What feedback you can provide"]],
      "Bug report":["Product issue","Help us reproduce the problem.","Describe what happened, what you expected, and the last action you took before the issue appeared.",["Page or workspace name","Steps that trigger the issue","Device and browser if relevant"]],
      "Collaboration":["Collaboration","Show us where our work connects.","Share the idea, the people involved, and what a useful collaboration would produce.",["Who you represent","Proposed scope","Expected outcome"]],
      "Business / partnership":["Partnership","Give us the practical context.","Outline the organization, opportunity, timing, and the next conversation you would like to have.",["Organization and role","Partnership idea","Timing or constraints"]],
      "Other":["Other message","Give the message a clear starting point.","Use the subject and message fields to explain where this request belongs.",["Relevant background","Your main question","Preferred next step"]]
    };
    const route=context.querySelector("[data-contact-route]"),title=context.querySelector("[data-contact-title]"),copy=context.querySelector("[data-contact-copy]"),tips=context.querySelector("[data-contact-tips] ul");
    const progress=page.querySelector("[data-contact-progress]"),fill=page.querySelector("[data-contact-progress-fill]");
    const updateContext=()=>{const item=content[reason.value]||content["General question"];route.textContent=item[0];title.textContent=item[1];copy.textContent=item[2];tips.replaceChildren(...item[3].map(text=>{const li=document.createElement("li");li.textContent=text;return li;}));};
    const updateProgress=()=>{const email=page.querySelector("#email")?.value.trim(),subject=page.querySelector("#subject")?.value.trim(),body=message?.value.trim();const value=Math.min(100,(email?35:0)+(body?45:0)+(subject?20:0));progress.textContent=`${value}%`;fill.style.width=`${value}%`;};
    reason.addEventListener("change",updateContext);
    page.querySelectorAll("#email,#subject,#message").forEach(field=>field.addEventListener("input",updateProgress));
    updateContext();updateProgress();
  });
})();
