(function () {
  "use strict";
  var root = document.querySelector("[data-feature-explorer]");
  if (!root) return;
  var features = [
    {label:"Private projects",desc:"Create protected worlds in your account and keep every universe separate.",kind:"projects"},
    {label:"Core entities",desc:"Create, edit, search, filter, and bulk-manage characters, factions, and events.",kind:"entities"},
    {label:"Relation builder",desc:"Connect records with typed relations and preview source → relation → target before saving.",kind:"relations"},
    {label:"Logic warnings",desc:"Review explainable timeline and relationship warnings generated from current project data.",kind:"warnings"},
    {label:"Graph workspace",desc:"Explore real entities and relations through the interactive constellation map and inspector.",kind:"graph"},
    {label:"JSON portability",desc:"Export and import supported project data as JSON for backup and portability.",kind:"json"}
  ];
  var list=root.querySelector("[data-feature-list]"), inspector=root.querySelector("[data-feature-inspector]"), current=0;
  features.forEach(function(feature,index){var button=document.createElement("button");button.type="button";button.className="zle-item";button.dataset.index=index;button.setAttribute("role","tab");button.innerHTML='<span>'+String(index+1).padStart(2,"0")+'</span><i>'+["◆","◫","↗","!","⌘","{ }"][index]+'</i><b>'+feature.label+'</b><em></em>';list.appendChild(button);});
  var items=Array.from(list.querySelectorAll(".zle-item"));
  function demo(kind){
    if(kind==="projects")return '<div class="zle-projects"><article><i>AV</i><span><b>Ashen Vale</b><small>Private project · 32 records</small></span><em>Open</em></article><article><i>NS</i><span><b>Northstar</b><small>Private project · 18 records</small></span><em>Open</em></article></div>';
    if(kind==="entities")return '<div class="zle-table"><span>Name</span><span>Type</span><span>Status</span><b>Seren Vale</b><i>Character</i><em>Active</em><b>The Ember Court</b><i>Faction</i><em>Active</em><b>Founding Accord</b><i>Event</i><em>Recorded</em></div>';
    if(kind==="relations")return '<div class="zle-relation"><span class="character">Seren Vale<small>Character</small></span><i>→</i><b>member_of</b><i>→</i><span class="faction">Ember Court<small>Faction</small></span></div><p class="zle-demo-note">Typed connection preview</p>';
    if(kind==="warnings")return '<div class="zle-warnings"><article><i></i><span><b>Possible timeline conflict</b><small>A character appears in an event after their recorded death.</small></span></article><article><i></i><span><b>One-sided hostility</b><small>A hostile relation may need a reciprocal connection.</small></span></article></div>';
    if(kind==="graph")return '<div class="zle-graph"><svg viewBox="0 0 620 270" aria-hidden="true"><g class="links"><path d="M115 142L295 65L500 135M115 142L315 220L500 135M295 65L315 220"/></g><g><circle cx="115" cy="142" r="34"/><circle cx="295" cy="65" r="28"/><circle cx="315" cy="220" r="30"/><circle cx="500" cy="135" r="36"/></g><text x="115" y="147">Character</text><text x="295" y="70">Faction</text><text x="315" y="225">Event</text><text x="500" y="140">Inspector</text></svg></div>';
    return '<div class="zle-json"><pre>{\n  "project": "Ashen Vale",\n  "characters": [ ... ],\n  "factions": [ ... ],\n  "events": [ ... ],\n  "relations": [ ... ]\n}</pre><span>Valid project JSON</span></div>';
  }
  function select(index){current=index;items.forEach(function(item,i){var active=i===index;item.classList.toggle("is-active",active);item.setAttribute("aria-selected",active?"true":"false");});var f=features[index];inspector.classList.add("is-changing");setTimeout(function(){inspector.innerHTML='<div class="zle-panel"><span class="zle-panel-id">Feature '+String(index+1).padStart(2,"0")+' / Live</span><h3>'+f.label+'</h3><p>'+f.desc+'</p><div class="zle-demo"><header><i></i><i></i><i></i><span>zirel / '+f.kind+'</span></header><main>'+demo(f.kind)+'</main></div><div class="zle-panel-foot"><span><i></i> Available in the current MVP</span><b>'+String(index+1).padStart(2,"0")+' / 06</b></div></div>';inspector.classList.remove("is-changing");},120);}
  items.forEach(function(item,index){item.addEventListener("click",function(){select(index);});item.addEventListener("keydown",function(e){if(e.key==="ArrowDown"||e.key==="ArrowRight"){e.preventDefault();select((current+1)%features.length);items[current].focus();}else if(e.key==="ArrowUp"||e.key==="ArrowLeft"){e.preventDefault();select((current-1+features.length)%features.length);items[current].focus();}});});
  select(0);
})();
