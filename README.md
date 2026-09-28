# cjanerun.store – waitlist test site

A static site for testing CJane Run concepts with Meta ads. Visitors join a
Klaviyo waitlist, and their answers (role, which product first, sport, ad UTM
tags) are saved on their Klaviyo profile.

| Page | Purpose |
|---|---|
| `/` | Home – shows both formats and asks which one they'd reach for |
| `/sticks/` | Ad test A – Before/After stick packs + protein balls |
| `/bottles/` | Ad test B – Strawberry Cream + Matcha Cream bottles |
| `/privacy/` | Privacy policy |

The test pages don't link to each other (the logo scrolls to the top), so
visitors from a sticks ad never see the bottles page and vice versa.

## Before launch

1. **Klaviyo** – create a CJane Run account (separate from Good Again), create
   a list called "CJane Run Waitlist" and paste the **Public API key** and
   **List ID** into `public/assets/config.js`.
   - Set the list to **single opt-in** if you want signups to count right away
     (Lists & Segments > list > Settings > Opt-in process).
2. **Meta Pixel** – create a pixel in Events Manager and paste its ID into
   `public/assets/config.js`. The site fires `PageView` on load and one `Lead`
   per visit on signup, with `content_name` = `home`, `sticks` or `bottles`.
   - Verify the domain in Business Settings > Brand safety > Domains (add the
     DNS TXT record in Cloudflare).
3. **Contact email** – the site lists `hello@cjanerun.store`. Turn on
   Cloudflare Email Routing for the domain and forward it to your inbox.
4. **Privacy policy** – `tools/build.py` has a plain-language draft. Have it
   reviewed before spending on ads.

## Ad links

Tag every ad's URL so signups show which ad they came from:

```
https://cjanerun.store/sticks/?utm_source=meta&utm_medium=paid&utm_campaign=cjr_concept_test&utm_content=AD_NAME
```

## Editing

Page copy lives in `tools/build.py`. After editing, rebuild:

```
python tools/build.py
```

Product illustrations: `tools/make_art.py`. Favicons and share image:
`tools/make_images.py` (uses headless Edge).

## Deploying (Cloudflare Workers static assets)

Same setup as the Good Again site. Either connect a GitHub repo to a Worker in
the Cloudflare dashboard (Workers & Pages > Create > Import a repository), or
deploy from this folder:

```
npx wrangler login
npx wrangler deploy
```

Then add `cjanerun.store` as a Custom Domain on the Worker
(Settings > Domains & Routes).

## Local preview

```
python -m http.server 8791 --directory public
```
