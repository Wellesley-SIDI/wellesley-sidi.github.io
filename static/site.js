const menu = document.querySelector('.menu-button');
const nav = document.querySelector('.nav');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? 'Close −' : 'Menu +';
  nav.classList.toggle('open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.click();
    menu.focus();
  }
});

const filters = [...document.querySelectorAll('.filter')];
const year = document.querySelector('#event-year');
const cards = [...document.querySelectorAll('.event-card')];
let category = 'All';
function filterEvents() {
  let count = 0;
  for (const card of cards) {
    const show = (category === 'All' || card.dataset.category === category)
      && (!year.value || card.dataset.year === year.value);
    card.hidden = !show;
    if (show) count++;
  }
  document.querySelector('#event-count').textContent = `${count} past event${count === 1 ? '' : 's'}`;
  document.querySelector('#event-empty').hidden = count > 0;
}
filters.forEach(button => button.addEventListener('click', () => {
  category = button.dataset.category;
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  filterEvents();
}));
year?.addEventListener('change', filterEvents);

const collaborationForm = document.querySelector('#collaboration-form');
collaborationForm?.addEventListener('submit', async event => {
  event.preventDefault();
  if (collaborationForm.getAttribute('aria-busy') === 'true' || !collaborationForm.reportValidity()) return;
  const fields = new FormData(collaborationForm);
  if (fields.get('_honey')) return;
  const button = collaborationForm.querySelector('button[type="submit"]');
  const status = document.querySelector('#collaboration-status');
  const fallback = document.querySelector('#collaboration-fallback');
  const buttonContent = button.innerHTML;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);
  button.disabled = true;
  button.textContent = 'Sending…';
  collaborationForm.setAttribute('aria-busy', 'true');
  status.hidden = true;
  fallback.hidden = true;
  try {
    const response = await fetch(collaborationForm.dataset.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(Object.fromEntries(fields)),
      signal: controller.signal
    });
    const result = await response.json();
    if (!response.ok || ![true, 'true'].includes(result.success)) throw new Error('Submission was not accepted');
    if (/activat|confirm.*email/i.test(result.message || '')) throw new Error('Form activation is pending');
    status.dataset.state = 'success';
    status.textContent = 'Thank you! Your message has been submitted to SIDI.';
    collaborationForm.reset();
  } catch (error) {
    status.dataset.state = 'error';
    status.textContent = error.name === 'AbortError'
      ? 'We couldn’t confirm delivery. Your message is still here; please email us directly if needed.'
      : 'We couldn’t send your message. Your text is still here so you can try again or email us directly.';
    fallback.hidden = false;
  } finally {
    clearTimeout(timeout);
    status.hidden = false;
    button.disabled = false;
    button.innerHTML = buttonContent;
    collaborationForm.removeAttribute('aria-busy');
  }
});

// Small, short-lived decorations; never intercept pointer or keyboard input.
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
const layer = document.createElement('div');
layer.className = 'sparkle-layer';
layer.setAttribute('aria-hidden', 'true');
document.body.append(layer);
const colors = ['#2e3488', '#b4ca70', '#858bc3'];
function sparkle(x, y, count = 1) {
  if (reducedMotion.matches || document.hidden) return;
  for (let i = 0; i < count && layer.childElementCount < 28; i++) {
    const star = document.createElement('span');
    star.className = 'interaction-sparkle';
    const angle = Math.random() * Math.PI * 2;
    const distance = count > 1 ? 18 + Math.random() * 26 : 15;
    star.style.cssText = `left:${x}px;top:${y}px;--size:${7 + Math.random() * 10}px;--dx:${Math.cos(angle) * distance}px;--dy:${Math.sin(angle) * distance - 12}px;--sparkle-color:${colors[i % colors.length]}`;
    layer.append(star);
    star.addEventListener('animationend', () => star.remove(), { once: true });
    setTimeout(() => star.remove(), 800);
  }
}
let lastTrail = 0;
document.addEventListener('pointermove', event => {
  if (!finePointer.matches || event.pointerType === 'touch' || reducedMotion.matches) return;
  if (!event.target.closest('a, button, .portrait-frame, .event-image, .title-sparkles')) return;
  if (performance.now() - lastTrail < 110) return;
  lastTrail = performance.now();
  sparkle(event.clientX, event.clientY);
}, { passive: true });
document.addEventListener('pointerdown', event => {
  if (event.button !== 0 || !event.target.closest('a, button, .portrait-frame, .event-image')) return;
  sparkle(event.clientX, event.clientY, 5);
}, { passive: true });
document.addEventListener('focusin', event => {
  if (!event.target.matches('a:focus-visible, button:focus-visible, select:focus-visible')) return;
  const box = event.target.getBoundingClientRect();
  sparkle(Math.min(box.right - 8, innerWidth - 12), box.top + box.height / 2, 3);
});
reducedMotion.addEventListener('change', () => layer.replaceChildren());
