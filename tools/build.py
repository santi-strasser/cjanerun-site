"""Builds the landing pages into public/.

Each page shares the same header, beliefs, join form, FAQ and footer; only the
hero copy, product section and "which first?" question change per concept.
Edit copy here, then run:
    python tools/build.py

Pages:
  /          home – both formats, asks which one they'd choose
  /sticks/   Meta test variant A – stick packs + protein balls
  /bottles/  Meta test variant B – creamy ready-to-drink bottles
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://cjanerun.store"
CONTACT = "hello@cjanerun.store"
TAGLINE = "Fuel what’s next."

ROLES = [
    "Athlete (18+)",
    "Athlete (13–17)",
    "Parent of an athlete",
    "Coach or trainer",
    "Other",
]

# ---------------------------------------------------------------- shared bits

BADGE = """<svg class="{cls}" viewBox="0 0 200 200" role="img" aria-label="CJane Run">
  <defs>
    <path id="arc-top-{uid}" d="M34 100A66 66 0 0 1 166 100"/>
    <path id="arc-bot-{uid}" d="M16 100A84 84 0 0 0 184 100"/>
  </defs>
  <circle cx="100" cy="100" r="96" fill="#1B2030" stroke="#E3A2AB" stroke-opacity=".35" stroke-width="2"/>
  <use href="/assets/images/runner.svg#runner" style="color:#E3A2AB"/>
  <g font-family="Montserrat, Arial, sans-serif" font-weight="600" font-size="25" letter-spacing="7" fill="#fff">
    <text><textPath href="#arc-top-{uid}" startOffset="50%" text-anchor="middle">CJANE</textPath></text>
    <text><textPath href="#arc-bot-{uid}" startOffset="50%" text-anchor="middle">RUN</textPath></text>
  </g>
</svg>"""

MARK = """<svg class="brand-mark" viewBox="0 0 200 200" aria-hidden="true">
  <circle cx="100" cy="100" r="96" fill="#252B40"/>
  <use href="/assets/images/runner.svg#runner" style="color:#E3A2AB"/>
</svg>"""


def head(page):
    url = SITE + page["path"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page['title']}</title>
<meta name="description" content="{page['description']}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['description']}">
<meta property="og:image" content="{SITE}/assets/images/og-share.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page['title']}">
<meta name="twitter:description" content="{page['description']}">
<meta name="twitter:image" content="{SITE}/assets/images/og-share.png">
<meta name="theme-color" content="#1B2030">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Montserrat:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<script src="/assets/config.js"></script>
<script src="/assets/pixel.js"></script>
<script src="/assets/form.js" defer></script>
</head>
"""


def topbar(page):
    # Test variants link the logo to the top of the same page, so ad traffic
    # isn't sent to the other concept and muddy the comparison.
    home = "/" if page["landing"] == "home" else "#top"
    return f"""<header class="topbar" id="top">
  <div class="wrap">
    <a class="brand" href="{home}">{MARK}<span class="brand-name">CJANE RUN</span></a>
    <a class="btn btn-small" href="#join">Join the waitlist</a>
  </div>
</header>
"""


def role_select():
    opts = "".join(f"<option>{r}</option>" for r in ROLES)
    return f"""<select class="select" name="role" required aria-label="I am a…">
        <option value="" disabled selected>I am a…</option>{opts}
      </select>"""


HONEYPOT = '<label class="hp-field" aria-hidden="true"><input type="checkbox" name="website" tabindex="-1"> Leave empty</label>'

FINEPRINT = (
    '<p class="fineprint">You must be 13 or older to join. By joining, you agree to get emails '
    'from CJane Run. Unsubscribe anytime. <a href="/privacy/">Privacy policy</a>.</p>'
)


def hero(page):
    return f"""<section class="hero">
  <div class="wrap">
    <div>
      {BADGE.format(cls="hero-badge", uid="hero")}
      <p class="eyebrow">Coming soon</p>
      <h1>Fuel what’s <span class="accent">next.</span></h1>
      <p class="lede">{page['hero_lede']}</p>
      <form class="waitlist-form" data-hero>
        <div class="field-row">
          <input class="input" type="email" name="email" placeholder="Your email" autocomplete="email" required aria-label="Email address">
          {role_select()}
        </div>
        {HONEYPOT}
        <button class="btn" type="submit">Join the waitlist</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        {FINEPRINT}
      </form>
    </div>
    <div class="hero-art {page['art_class']}" aria-hidden="true">
      <div class="glow"></div>
      {page['hero_art']}
    </div>
  </div>
</section>
"""


ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="#1B2030" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M10 2h4"/></svg>'
ICON_HEART = '<svg viewBox="0 0 24 24" fill="none" stroke="#1B2030" stroke-width="2.2" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>'
ICON_STAR = '<svg viewBox="0 0 24 24" fill="none" stroke="#1B2030" stroke-width="2.2" stroke-linejoin="round"><path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg>'

BELIEFS = f"""<section class="section beliefs">
  <div class="wrap">
    <p class="eyebrow">Why we exist</p>
    <h2>Not another gym-bro supplement.</h2>
    <p class="lede">Most sports nutrition was built for someone else. We’re building ours around the athletes who train for what they can do.</p>
    <div class="beliefs-grid">
      <article class="belief">
        <div class="dot" style="background:#FBE4EA">{ICON_CLOCK}</div>
        <h3>Built around your training</h3>
        <p>Before practice, after it and in between – made to fit real schedules with school, travel games and two-a-days.</p>
      </article>
      <article class="belief">
        <div class="dot" style="background:#ECE8F7">{ICON_HEART}</div>
        <h3>Taste comes first</h3>
        <p>If it doesn’t taste great, you won’t use it. We start with flavors you already love and ingredients you recognize.</p>
      </article>
      <article class="belief">
        <div class="dot" style="background:#E3EFE9">{ICON_STAR}</div>
        <h3>Confidence, not diet culture</h3>
        <p>We’re about energy, recovery and what your body can do. Never weight loss or body transformation.</p>
      </article>
    </div>
  </div>
</section>
"""


def product_card(p):
    rows = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["facts"])
    return f"""<article class="product m-{p['moment'].lower()}">
        <div class="product-art"><img src="/assets/images/{p['img']}" alt="{p['alt']}"></div>
        <div class="product-body">
          <p class="moment">{p['moment']}</p>
          <h3>{p['name']}</h3>
          <p class="how">{p['how']}</p>
          <dl>{rows}</dl>
        </div>
      </article>"""


def products(page):
    cards = "\n      ".join(product_card(p) for p in page["products"])
    grid = "product-grid two" if len(page["products"]) == 2 else "product-grid"
    return f"""<section class="section products">
  <div class="wrap">
    <p class="eyebrow">What we’re building</p>
    <h2>{page['products_title']}</h2>
    <p class="lede">{page['products_lede']}</p>
    <div class="{grid}">
      {cards}
    </div>
    <p class="concept-note">Product concepts shown are in development. Ingredients, flavors and packaging may change.</p>
  </div>
</section>
"""


def chips(q):
    items = "".join(
        f'<label class="chip"><input type="radio" name="{q["name"]}" value="{v}"><span>{v}</span></label>'
        for v in q["options"]
    )
    return f"""<fieldset>
          <legend>{q['legend']}</legend>
          <div class="chips">{items}</div>
        </fieldset>"""


def join(page):
    return f"""<section class="section join" id="join">
  <div class="wrap">
    <div>
      <p class="eyebrow">Join the waitlist</p>
      <h2>Help us build CJane Run.</h2>
      <p class="lede">We’re developing our products with athletes, not just for them. Join now and help shape what we make.</p>
      <ul class="perks">
        <li>First access when we launch</li>
        <li>A say in our flavors and products</li>
        <li>Behind-the-scenes updates as we build</li>
      </ul>
    </div>
    <div class="join-card">
      <form class="waitlist-form">
        <div class="field-row">
          <input class="input" type="email" name="email" placeholder="Your email" autocomplete="email" required aria-label="Email address">
          {role_select()}
        </div>
        {chips(page['question'])}
        <fieldset>
          <legend>What’s your sport? <span style="font-weight:400;color:#5B6072">(optional)</span></legend>
          <input class="input" type="text" name="sport" placeholder="e.g. soccer, volleyball, dance" maxlength="60" autocomplete="off">
        </fieldset>
        {HONEYPOT}
        <button class="btn" type="submit">Join the waitlist</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        {FINEPRINT}
      </form>
    </div>
  </div>
</section>
"""


def faq(page):
    items = [
        ("Can I buy it now?",
         "Not yet. CJane Run is in development – we’re building our products with athletes before we launch. Join the waitlist and you’ll hear first."),
        ("Who is it for?",
         "Athletes 13 and up who train seriously – high school, club and college – and the parents and coaches who support them."),
        (page["caffeine_q"],
         "We’re testing options, including a caffeine-free version. Tell us what you’d prefer when you join – it will shape what we make."),
        ("Is it right for teen athletes?",
         "We’re developing every product with age-appropriate expert guidance, and we’ll share full ingredient lists before launch. Food, water and rest come first – we’re here to make fueling easier, not replace it."),
    ]
    body = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f"""<section class="section faq">
  <div class="wrap">
    <p class="eyebrow">Questions</p>
    <h2>Good to know</h2>
    <div class="faq-list">{body}</div>
  </div>
</section>
"""


def footer():
    return f"""<footer class="footer">
  <div class="wrap">
    <span>© 2026 CJane Run · {TAGLINE}</span>
    <nav><a href="/privacy/">Privacy</a><a href="mailto:{CONTACT}">{CONTACT}</a></nav>
    <p class="disclaimer">CJane Run products are in development and not yet for sale.</p>
  </div>
</footer>
"""


# ---------------------------------------------------------------- page content

STICKS_PRODUCTS = [
    {
        "moment": "BEFORE", "name": "Performance stick", "img": "stick-before.svg",
        "alt": "Pink CJane Run 'Before' stick pack",
        "how": "Tear, pour into water and shake about 30 minutes before practice or a game.",
        "facts": [
            ("Built for", "Hydration, steady energy and focus"),
            ("Flavors we’re exploring", "Strawberry, mixed berry"),
        ],
    },
    {
        "moment": "AFTER", "name": "Recovery stick", "img": "stick-after.svg",
        "alt": "Lavender CJane Run 'After' stick pack",
        "how": "Mix with water, or blend into a smoothie after training.",
        "facts": [
            ("Built for", "Protein to rebuild, carbs to refuel, electrolytes to rehydrate"),
            ("Flavors we’re exploring", "Matcha, banana, almond"),
        ],
    },
    {
        "moment": "SNACK", "name": "Protein balls", "img": "pouch-snack.svg",
        "alt": "Green CJane Run protein balls pouch",
        "how": "A real-food snack for your bag, the bus or between sessions.",
        "facts": [
            ("Built for", "Protein and fiber in a bite-sized snack"),
            ("Flavors", "You tell us"),
        ],
    },
]

BOTTLES_PRODUCTS = [
    {
        "moment": "BEFORE", "name": "Strawberry Cream", "img": "bottle-before.svg",
        "alt": "CJane Run Strawberry Cream bottle",
        "how": "Creamy, sweet and ready to drink – grab it on your way to practice.",
        "facts": [
            ("Built for", "Energy, focus and electrolytes for hydration"),
            ("Tastes like", "A strawberry café drink, in a bottle"),
        ],
    },
    {
        "moment": "AFTER", "name": "Matcha Cream", "img": "bottle-after.svg",
        "alt": "CJane Run Matcha Cream bottle",
        "how": "A smooth, plant-based recovery drink for after training.",
        "facts": [
            ("Built for", "20g plant protein, carbs to refuel, electrolytes to rehydrate"),
            ("Flavors we’re exploring", "Matcha, banana, almond"),
        ],
    },
]

FORMATS = """<section class="section products">
  <div class="wrap">
    <p class="eyebrow">What we’re building</p>
    <h2>Two ways to fuel. Which would you reach for?</h2>
    <p class="lede">We’re deciding what to make first, and your vote counts. Here are the two ideas we’re exploring.</p>
    <div class="format-grid">
      <article class="format">
        <div class="format-art">
          <img src="/assets/images/stick-before.svg" alt="Before stick pack">
          <img src="/assets/images/stick-after.svg" alt="After stick pack">
          <img class="short" src="/assets/images/pouch-snack.svg" alt="Protein balls pouch">
        </div>
        <h3>Mix-and-go sticks + a snack</h3>
        <p>A Before stick and an After stick you pour into water, plus protein balls for between sessions. Light, cheap to carry and easy to toss in a bag.</p>
      </article>
      <article class="format">
        <div class="format-art">
          <img src="/assets/images/bottle-before.svg" alt="Strawberry Cream bottle">
          <img src="/assets/images/bottle-after.svg" alt="Matcha Cream bottle">
        </div>
        <h3>Creamy ready-to-drink bottles</h3>
        <p>Strawberry Cream before practice and Matcha Cream after – like your favorite café drinks, made for athletes. Nothing to mix.</p>
      </article>
    </div>
    <p class="concept-note">Product concepts shown are in development. Ingredients, flavors and packaging may change.</p>
  </div>
</section>
"""


def img(name, cls):
    return f'<img class="{cls}" src="/assets/images/{name}" alt="">'


PAGES = [
    {
        "file": "index.html", "path": "/", "landing": "home",
        "title": "CJane Run – Fuel what’s next.",
        "description": "Great-tasting sports nutrition built around how you actually train. CJane Run is coming soon – join the waitlist.",
        "hero_lede": "Great-tasting sports nutrition built around how you actually train – before practice, after it and everything in between.",
        "art_class": "art-home",
        "hero_art": img("stick-before.svg", "s1") + img("stick-after.svg", "s2") + img("bottle-before.svg", "b1") + img("bottle-after.svg", "b2"),
        "middle": FORMATS,
        "question": {
            "name": "format_pref", "legend": "Which would you reach for?",
            "options": ["Mix-and-go sticks + snack", "Ready-to-drink bottles", "Both", "Not sure yet"],
        },
        "caffeine_q": "Will the before-practice product have caffeine?",
    },
    {
        "file": "sticks/index.html", "path": "/sticks/", "landing": "sticks",
        "title": "CJane Run – Fuel what’s next.",
        "description": "Mix-and-go sports nutrition sticks and a protein snack, built around how you actually train. Join the CJane Run waitlist.",
        "hero_lede": "Great-tasting nutrition built around how you actually train. Tear, pour, shake – before practice, after it and in between.",
        "art_class": "art-sticks",
        "hero_art": img("stick-before.svg", "s1") + img("stick-after.svg", "s2") + img("pouch-snack.svg", "pouch"),
        "products": STICKS_PRODUCTS,
        "products_title": "Three moments. One routine.",
        "products_lede": "Light sticks you mix with water, plus a snack you’ll actually crave. Everything fits in your gym bag.",
        "question": {
            "name": "first_pick", "legend": "Which would you try first?",
            "options": ["Before stick", "After stick", "Protein balls"],
        },
        "caffeine_q": "Will the Performance stick have caffeine?",
    },
    {
        "file": "bottles/index.html", "path": "/bottles/", "landing": "bottles",
        "title": "CJane Run – Fuel what’s next.",
        "description": "Creamy, ready-to-drink fuel for before practice and after it – like your favorite café drinks, made for athletes. Join the CJane Run waitlist.",
        "hero_lede": "Your favorite café drinks, reimagined for athletes. Creamy, ready-to-drink fuel for before practice and after it.",
        "art_class": "art-bottles",
        "hero_art": img("bottle-before.svg", "b1") + img("bottle-after.svg", "b2"),
        "products": BOTTLES_PRODUCTS,
        "products_title": "Two drinks. Before and after.",
        "products_lede": "Nothing to mix, nothing to measure. Grab one from the fridge on the way to practice, and one for the ride home.",
        "question": {
            "name": "first_pick", "legend": "Which would you try first?",
            "options": ["Strawberry Cream (before)", "Matcha Cream (after)"],
        },
        "caffeine_q": "Will Strawberry Cream have caffeine?",
    },
]


def build(page):
    middle = page.get("middle") or products(page)
    html = (
        head(page)
        + f'<body data-landing="{page["landing"]}">\n'
        + topbar(page)
        + "<main>\n"
        + hero(page)
        + BELIEFS
        + middle
        + join(page)
        + faq(page)
        + "</main>\n"
        + footer()
        + "</body>\n</html>\n"
    )
    out = PUBLIC / page["file"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


PRIVACY = f"""<section class="legal">
  <div class="wrap">
    <h1>Privacy policy</h1>
    <p class="updated">Last updated: September 28, 2026</p>
    <p>CJane Run (“we,” “us”) is a brand in development. This policy explains what we collect on cjanerun.store and how we use it.</p>

    <h2>What we collect</h2>
    <ul>
      <li><strong>What you give us:</strong> your email address and any answers you choose to share when you join the waitlist (such as whether you’re an athlete, parent or coach, your sport and which products interest you).</li>
      <li><strong>Visit information:</strong> the page you signed up on and any campaign tags in the link you followed (for example, which ad you clicked).</li>
      <li><strong>Advertising measurement:</strong> we use the Meta Pixel to understand whether our ads on Facebook and Instagram lead to waitlist signups. The pixel uses cookies and similar technology to record page visits and signups.</li>
    </ul>

    <h2>How we use it</h2>
    <ul>
      <li>To send you updates about CJane Run, including launch news and invitations to share feedback.</li>
      <li>To learn which product ideas people are most interested in, so we can decide what to build.</li>
      <li>To measure and improve our advertising.</li>
    </ul>
    <p>We don’t sell your personal information.</p>

    <h2>Who helps us</h2>
    <p>We use Klaviyo to store our waitlist and send email, Meta for advertising measurement, and Cloudflare to host this site. They process data on our behalf under their own privacy terms.</p>

    <h2>Your choices</h2>
    <ul>
      <li>Every email includes an unsubscribe link.</li>
      <li>To see, correct or delete the information we hold about you, email <a href="mailto:{CONTACT}">{CONTACT}</a>.</li>
      <li>You can limit ad tracking in your Facebook/Instagram ad settings and your browser’s cookie settings.</li>
    </ul>

    <h2>Children</h2>
    <p>Our waitlist is for people 13 and older. We don’t knowingly collect information from children under 13. If you believe a child under 13 has signed up, email us and we’ll delete it.</p>

    <h2>Changes</h2>
    <p>If we update this policy, we’ll change the date at the top of this page.</p>

    <h2>Contact</h2>
    <p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
  </div>
</section>
"""


def build_privacy():
    page = {
        "path": "/privacy/", "landing": "privacy",
        "title": "Privacy policy – CJane Run",
        "description": "How CJane Run collects and uses information on cjanerun.store.",
    }
    html = (
        head(page)
        + '<body data-landing="privacy">\n'
        + topbar({"landing": "home"}).replace('href="#join"', 'href="/#join"')
        + "<main>\n" + PRIVACY + "</main>\n"
        + footer()
        + "</body>\n</html>\n"
    )
    out = PUBLIC / "privacy" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    for p in PAGES:
        build(p)
    build_privacy()
