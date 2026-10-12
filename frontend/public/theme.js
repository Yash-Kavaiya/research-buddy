// Apply a saved theme before first paint.
try {
  var t = JSON.parse(localStorage.getItem('rb.preferences') || '{}').theme;
  if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
} catch (e) {}
