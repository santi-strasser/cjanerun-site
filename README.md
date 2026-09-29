# cjanerun.store – waitlist test site

A static site for a Meta ad test of CJane Run's stick packs. Visitors join a
Klaviyo waitlist, and their answers (role, how often they'd use it, sport, ad
UTM tags) are saved on their Klaviyo profile along with `signup_page`.

## The test (2x2)

| Page | `signup_page` | Cell |
|---|---|---|
| `/pre/` | `cjr_pre` | Pre-workout – CJane Run Before stick |
| `/hydrate/` | `generic_pre` | Pre-workout – "Everyday Hydration Mix" (neutral, Liquid IV-style control) |
| `/post/` | `cjr_post` | Post-workout – CJane Run After stick |
| `/recover/` | `generic_post` | Post-workout – "Everyday Recovery Mix" (neutral, Vital Proteins-style control) |
| `/` | `home` | CJane Run home – organic traffic, not an ad cell |
| `/privacy/` | – | Privacy policy |

All four ad pages share the same layout, form, questions, flavors and
nutrition – only the brand and positioning change. They don't link to each
other (the logo scrolls to the top), so each ad's visitors stay in their cell.
"Everyday" is a made-up neutral brand; its pages disclose in the footer and
consent line that it's a concept being tested by CJane Run. Its ads should run
from a separate, neutral Facebook Page so the CJane Run name doesn't appear.

Old `/sticks/` and `/bottles/` links redirect to `/` (see `public/_redirects`).

## Before launch

1. **Klaviyo** – create a CJane Run account (separate from Good Again), create
   a list called "CJane Run Waitlist" and paste the **Public API key** and
   **List ID** into `public/assets/config.js`.
   - Set the list to **single opt-in** if you want signups to count right away
     (Lists & Segments > list > Settings > Opt-in process).
2. **Meta Pixel** – create a pixel in Events Manager and paste its ID into
   `public/assets/config.js`. The site fires `PageView` on load and one `Lead`
   per visit on signup, with `content_name` = the page's `signup_page` value.
   - Verify the domain in Business Settings > Brand safety > Domains (add the
     DNS TXT record in Cloudflare).
3. **Google Analytics 4** – paste the web stream's Measurement ID (`G-…`) into
   `public/assets/config.js`. Pages report by path (`/pre/`, `/hydrate/`,
   `/post/`, `/recover/`); signups send one `generate_lead` event per visit
   with `signup_page`. In GA, mark `generate_lead` as a key event and register
   `signup_page` as an event-scoped custom dimension.
4. **Contact email** – the site lists `hello@cjanerun.store`. Turn on
   Cloudflare Email Routing for the domain and forward it to your inbox.
5. **Privacy policy** – `tools/build.py` has a plain-language draft. Have it
   reviewed before spending on ads.

## Ad links

Tag every ad's URL so signups show which ad they came from:

```
https://cjanerun.store/pre/?utm_source=meta&utm_medium=paid&utm_campaign=cjr_stick_test&utm_content=AD_NAME
```

## Editing

Page copy lives in `tools/build.py`. After editing, rebuild:

```
python tools/build.py
```

Stick illustrations: `tools/make_art.py`. Favicons and share image:
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
