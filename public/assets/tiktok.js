// TikTok Pixel – loads only once a Pixel ID is set in config.js.
// One pixel per TikTok ad account: /everyday/ pages use the Everyday pixel,
// every other page (except /privacy/) uses the CJane Run pixel.
(function () {
  var cfg = window.CJR_CONFIG || {};
  var path = window.location.pathname || '/';
  if (path.indexOf('/privacy') === 0) return;

  var id = path.indexOf('/everyday') === 0 ? cfg.tiktokPixelIdEveryday : cfg.tiktokPixelIdCjr;
  if (!id) return;

  !function (w, d, t) {
    w.TiktokAnalyticsObject = t;
    var ttq = w[t] = w[t] || [];
    ttq.methods = ['page', 'track', 'identify', 'instances', 'debug', 'on', 'off', 'once', 'ready', 'alias', 'group', 'enableCookie', 'disableCookie', 'holdConsent', 'revokeConsent', 'grantConsent'];
    ttq.setAndDefer = function (t, e) {
      t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); };
    };
    for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
    ttq.instance = function (t) {
      for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]);
      return e;
    };
    ttq.load = function (e, n) {
      var r = 'https://analytics.tiktok.com/i18n/pixel/events.js';
      ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = r;
      ttq._t = ttq._t || {}; ttq._t[e] = +new Date();
      ttq._o = ttq._o || {}; ttq._o[e] = n || {};
      var s = d.createElement('script');
      s.type = 'text/javascript'; s.async = true;
      s.src = r + '?sdkid=' + e + '&lib=' + t;
      var f = d.getElementsByTagName('script')[0];
      f.parentNode.insertBefore(s, f);
    };
    ttq.load(id);
    ttq.page();
  }(window, document, 'ttq');
})();
