// Google Analytics 4 – loads only once a Measurement ID is set in config.js.
(function () {
  var id = window.CJR_CONFIG && window.CJR_CONFIG.ga4MeasurementId;
  if (!id) return;

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', id);
})();
