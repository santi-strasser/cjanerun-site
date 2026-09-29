(function () {
  var cfg = window.CJR_CONFIG || {};
  var API = 'https://a.klaviyo.com/client/';
  var HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    Accept: 'application/vnd.api+json',
    revision: '2026-07-15'
  };
  var LANDING = document.body.getAttribute('data-landing') || 'home';
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

  // Answers go on the profile separately so a problem here never blocks the signup.
  function saveAnswers(email, answers) {
    return post('profiles', {
      data: { type: 'profile', attributes: { email: email, properties: answers } }
    }).catch(function () {});
  }

  function answersFrom(form) {
    var data = new FormData(form);
    var out = { signup_page: LANDING };
    ['role', 'first_pick', 'format_pref', 'sport'].forEach(function (k) {
      var v = (data.get(k) || '').toString().trim();
      if (v) out[k] = v;
    });
    Object.keys(utms).forEach(function (k) { out[k] = utms[k]; });
    return out;
  }

  function setStatus(el, kind, html) {
    el.className = 'form-status' + (kind ? ' ' + kind : '');
    el.innerHTML = html;
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
      var answers = answersFrom(form);
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Joining…';
      setStatus(status, '', '');

      subscribe(email)
        .then(function (res) {
          if (!res.ok) throw new Error('Klaviyo ' + res.status);
          saveAnswers(email, answers);
          // One Lead per visit – the join form often follows a hero signup.
          if (!leadTracked) {
            if (window.fbq) window.fbq('track', 'Lead', { content_name: LANDING });
            if (window.gtag) window.gtag('event', 'generate_lead', { signup_page: LANDING });
          }
          leadTracked = true;

          form.reset();
          if (form.hasAttribute('data-hero')) {
            // Invite hero signups to answer the extra questions in the join form.
            var joinEmail = document.querySelector('#join input[type="email"]');
            if (joinEmail) joinEmail.value = email;
            setStatus(status, 'ok', 'You’re on the list! <a href="#join">Help us build it – 2 quick questions ↓</a>');
          } else {
            setStatus(status, 'ok', 'You’re on the list – thank you for helping us build CJane Run.');
          }
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
