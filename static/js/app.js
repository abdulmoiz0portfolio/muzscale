/* MuzScale - Client-side logic for dark theme image editor */

const state = {
  img: null,
  canvas: null,
  ctx: null,
  filters: {
    brightness: 100,
    contrast: 100,
    saturation: 100,
    blur: 0,
    grayscale: 0,
    sepia: 0,
  },
  transform: {
    rotate: 0,
    flipH: false,
    flipV: false,
    scale: 1,
  },
  uploading: false,
  mockMode: false,
};

function qs(sel) { return document.querySelector(sel); }
function qsa(sel) { return Array.from(document.querySelectorAll(sel)); }

function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast show ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { toast.remove(); }, 3000);
}

function buildFilterCSS() {
  const f = state.filters;
  return `brightness(${f.brightness}%) contrast(${f.contrast}%) saturate(${f.saturation}%) blur(${f.blur}px) grayscale(${f.grayscale}%) sepia(${f.sepia}%)`;
}

function applyCanvas() {
  if (!state.img || !state.ctx) return;
  const { canvas, ctx } = state;
  const img = state.img;

  // fit to canvas
  const maxW = Math.min(window.innerWidth - 480, img.width);
  const maxH = Math.min(window.innerHeight - 220, img.height);
  const ratio = Math.min(maxW / img.width, maxH / img.height, 1);
  canvas.width = Math.max(1, Math.floor(img.width * ratio * state.transform.scale));
  canvas.height = Math.max(1, Math.floor(img.height * ratio * state.transform.scale));

  ctx.save();
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // set filters
  ctx.filter = buildFilterCSS();

  // transforms
  ctx.translate(canvas.width / 2, canvas.height / 2);
  const rad = (state.transform.rotate * Math.PI) / 180;
  ctx.rotate(rad);
  ctx.scale(state.transform.flipH ? -1 : 1, state.transform.flipV ? -1 : 1);

  const drawW = canvas.width;
  const drawH = canvas.height;
  ctx.drawImage(img, -drawW / 2, -drawH / 2, drawW, drawH);

  ctx.restore();
}

function loadImageFromFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = reader.result;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function handleFiles(files) {
  if (!files || !files.length) return;
  const file = files[0];
  try {
    state.img = await loadImageFromFile(file);
    applyCanvas();
    showToast('Image loaded');
  } catch (e) {
    console.error(e);
    showToast('Failed to load image', 'error');
  }
}

function initUploadArea() {
  const drop = qs('#uploadArea');
  const fileInput = qs('#fileInput');
  drop.addEventListener('click', () => fileInput.click());
  drop.addEventListener('dragover', (e) => {
    e.preventDefault();
    drop.classList.add('dragover');
  });
  drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));
  drop.addEventListener('drop', (e) => {
    e.preventDefault();
    drop.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
  });
  fileInput.addEventListener('change', (e) => handleFiles(e.target.files));
}

function bindControls() {
  const map = [
    ['#brightness', 'brightness'],
    ['#contrast', 'contrast'],
    ['#saturation', 'saturation'],
    ['#blur', 'blur'],
    ['#grayscale', 'grayscale'],
    ['#sepia', 'sepia'],
    ['#rotate', 'rotate', 'transform'],
    ['#scale', 'scale', 'transform'],
  ];
  map.forEach(([sel, key, domain]) => {
    const el = qs(sel);
    const valLabel = el?.parentElement?.querySelector('.val');
    if (!el) return;
    el.addEventListener('input', () => {
      const num = Number(el.value);
      if (domain === 'transform') {
        state.transform[key] = num;
      } else {
        state.filters[key] = num;
      }
      if (valLabel) valLabel.textContent = num;
      applyCanvas();
    });
  });

  qs('#flipH')?.addEventListener('click', () => {
    state.transform.flipH = !state.transform.flipH;
    applyCanvas();
  });
  qs('#flipV')?.addEventListener('click', () => {
    state.transform.flipV = !state.transform.flipV;
    applyCanvas();
  });
}

async function upscaleImage() {
  if (!state.img) return showToast('Please upload an image first', 'warning');
  const btn = qs('#upscaleBtn');
  const loading = qs('#upscaleLoading');

  btn.disabled = true;
  loading.classList.add('active');

  try {
    if (state.mockMode) {
      // Simulate delay and return current canvas as result
      await new Promise((r) => setTimeout(r, 1200));
      const dataUrl = state.canvas.toDataURL('image/png');
      openResult(dataUrl);
      return;
    }

    // Build form data: include original file and parameters
    const blob = await new Promise((resolve) => state.canvas.toBlob(resolve, 'image/png'));
    const form = new FormData();
    form.append('image', blob, 'canvas.png');
    form.append('brightness', state.filters.brightness);
    form.append('contrast', state.filters.contrast);
    form.append('saturation', state.filters.saturation);
    form.append('blur', state.filters.blur);
    form.append('grayscale', state.filters.grayscale);
    form.append('sepia', state.filters.sepia);
    form.append('rotate', state.transform.rotate);
    form.append('flipH', state.transform.flipH);
    form.append('flipV', state.transform.flipV);
    form.append('scale', state.transform.scale);

    const res = await fetch('/api/upscale', {
      method: 'POST',
      body: form,
    });

    if (!res.ok) throw new Error('Server error');

    const ct = res.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      const json = await res.json();
      if (json.url) return openResult(json.url);
      if (json.dataUrl) return openResult(json.dataUrl);
    }

    const blobRes = await res.blob();
    const url = URL.createObjectURL(blobRes);
    openResult(url);
  } catch (e) {
    console.error(e);
    showToast('Upscale failed', 'error');
  } finally {
    btn.disabled = false;
    loading.classList.remove('active');
  }
}

function openResult(url) {
  const a = document.createElement('a');
  a.href = url;
  a.download = 'muzscale_result.png';
  a.click();
  showToast('Upscaled image downloaded');
}

function bindToolbar() {
  qs('#resetBtn')?.addEventListener('click', () => {
    state.filters = { brightness: 100, contrast: 100, saturation: 100, blur: 0, grayscale: 0, sepia: 0 };
    state.transform = { rotate: 0, flipH: false, flipV: false, scale: 1 };
    qsa('input[type="range"]').forEach((r) => {
      const id = r.id;
      if (id in state.filters) r.value = state.filters[id];
      if (id in state.transform) r.value = state.transform[id];
      r.dispatchEvent(new Event('input'));
    });
    applyCanvas();
  });

  qs('#downloadBtn')?.addEventListener('click', () => {
    if (!state.canvas) return;
    const url = state.canvas.toDataURL('image/png');
    openResult(url);
  });

  qs('#upscaleBtn')?.addEventListener('click', upscaleImage);
}

function detectMockMode() {
  // If backend not available, allow demoing UI
  fetch('/health').then(() => { state.mockMode = false; }).catch(() => { state.mockMode = true; });
}

function init() {
  state.canvas = qs('#canvas');
  state.ctx = state.canvas.getContext('2d');
  initUploadArea();
  bindControls();
  bindToolbar();
  detectMockMode();
}

document.addEventListener('DOMContentLoaded', init);
