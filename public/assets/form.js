(function () {
  var cfg = window.CJR_CONFIG || {};
  var API = 'https://a.klaviyo.com/client/';
  var HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    Accept: 'application/vnd.api+json',
    revision: '2026-07-15'
  };
  var LANDING = document.body.getAttribute('data-landing') || 'cjr';
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  var leadTracked = false;

  // Keep the ad's UTM tags for the whole visit, even if the URL changes.
  var utms = {};
  var params = new URLSearchParams(window.location.search);
  UTM_KEYS.forEach(function (k) {
    var v = params.get(k);
    try {
      if (v) sessionStorage.setItem(k, v);
      else v = sessionStorage.getItem(k);
    } catch (e) { /* storage blocked – URL value only */ }
    if (v) utms[k] = v;
  });

  function post(path, body) {
    return fetch(API + path + '?company_id=' + encodeURIComponent(cfg.klaviyoPublicKey), {
      method: 'POST',
      headers: HEADERS,
      body: JSON.stringify(body)
    });
  }

  function subscribe(email) {
    return post('subscriptions', {
      data: {
        type: 'subscription',
        attributes: {
          custom_source: 'cjanerun.store – ' + LANDING,
          profile: {
            data: {
              type: 'profile',
              attributes: {
                email: email,
                subscriptions: { email: { marketing: { consent: 'SUBSCRIBED' } } }
              }
            }
          }
        },
        relationships: { list: { data: { type: 'list', id: cfg.klaviyoListId } } }
      }
    });
  }

  // The page and ad tags go on the profile separately, so a problem here never blocks the signup.
  function saveSource(email) {
    var props = { signup_page: LANDING };
    Object.keys(utms).forEach(function (k) { props[k] = utms[k]; });
    return post('profiles', {
      data: { type: 'profile', attributes: { email: email, properties: props } }
    }).catch(function () {});
  }

  function setStatus(el, kind, text) {
    el.className = 'form-status' + (kind ? ' ' + kind : '');
    el.textContent = text;
  }

  document.querySelectorAll('form.waitlist-form').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var honeypot = form.querySelector('.hp-field input');
      if (honeypot && honeypot.checked) return;

      if (!cfg.klaviyoPublicKey || !cfg.klaviyoListId) {
        setStatus(status, 'err', 'Signups aren’t connected yet – please check back soon.');
        console.warn('CJR: set klaviyoPublicKey and klaviyoListId in /assets/config.js');
        return;
      }

      var email = form.querySelector('input[type="email"]').value.trim();
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Joining…';
      setStatus(status, '', '');

      subscribe(email)
        .then(function (res) {
          if (!res.ok) throw new Error('Klaviyo ' + res.status);
          saveSource(email);
          // One Lead per visit, even if someone uses both forms on the page.
          if (!leadTracked) {
            if (window.fbq) window.fbq('track', 'Lead', { content_name: LANDING });
            if (window.gtag) window.gtag('event', 'generate_lead', { signup_page: LANDING });
          }
          leadTracked = true;

          form.reset();
          setStatus(status, 'ok', 'You’re on the list – we’ll be in touch.');
        })
        .catch(function () {
          setStatus(status, 'err', 'Something went wrong. Please try again.');
        })
        .finally(function () {
          btn.disabled = false;
          btn.textContent = label;
        });
    });
  });
})();
