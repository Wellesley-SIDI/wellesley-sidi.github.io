const menu=document.querySelector('.menu-button'),nav=document.querySelector('.nav');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'Close −':'Menu +';nav.classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){menu.click();menu.focus()}});
const filters=[...document.querySelectorAll('.filter')],year=document.querySelector('#event-year'),cards=[...document.querySelectorAll('.event-card')];let category='All';
function filterEvents(){let count=0;for(const card of cards){const show=(category==='All'||card.dataset.category===category)&&(!year.value||card.dataset.year===year.value);card.hidden=!show;if(show)count++}document.querySelector('#event-count').textContent=count+' past event'+(count===1?'':'s');document.querySelector('#event-empty').hidden=count>0}
filters.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.category;filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filterEvents()}));year?.addEventListener('change',filterEvents);
