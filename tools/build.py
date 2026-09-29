"""Builds the landing pages into public/.

The Meta test is a 2x2: CJane Run vs a neutral control brand ("Everyday"),
for a pre-workout stick and a post-workout stick. All four test pages share
the same layout, form, questions, flavors and nutrition – only the brand and
positioning change. Edit copy here, then run:
    python tools/build.py

Pages:
  /           CJane Run home – both sticks (organic traffic, not an ad cell)
  /pre/       Ad cell: pre-workout, CJane Run Before stick
  /hydrate/   Ad cell: pre-workout, Everyday Hydration Mix (Liquid IV-style control)
  /post/      Ad cell: post-workout, CJane Run After stick
  /recover/   Ad cell: post-workout, Everyday Recovery Mix (Vital Proteins-style control)
  /privacy/   Privacy policy
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://cjanerun.store"
CONTACT = "hello@cjanerun.store"

ROLES = [
    "Athlete (18+)",
    "Athlete (13–17)",
    "Parent of an athlete",
    "Coach or trainer",
    "Other",
]

# Asked on every ad cell, so desire can be compared like-for-like.
USE_FREQ = {
    "name": "use_freq", "legend": "How often would you use it?",
    "options": ["Every practice or workout", "A few times a week", "Game or race days only", "Not sure yet"],
}

# ---------------------------------------------------------------- brand marks

CJR_BADGE = """<svg class="hero-badge" viewBox="0 0 200 200" role="img" aria-label="CJane Run">
  <defs>
    <path id="arc-top" d="M34 100A66 66 0 0 1 166 100"/>
    <path id="arc-bot" d="M16 100A84 84 0 0 0 184 100"/>
  </defs>
  <circle cx="100" cy="100" r="96" fill="#1B2030" stroke="#E3A2AB" stroke-opacity=".35" stroke-width="2"/>
  <use href="/assets/images/runner.svg#runner" style="color:#E3A2AB"/>
  <g font-family="Montserrat, Arial, sans-serif" font-weight="600" font-size="25" letter-spacing="7" fill="#fff">
    <text><textPath href="#arc-top" startOffset="50%" text-anchor="middle">CJANE</textPath></text>
    <text><textPath href="#arc-bot" startOffset="50%" text-anchor="middle">RUN</textPath></text>
  </g>
</svg>"""

CJR_MARK = """<svg class="brand-mark" viewBox="0 0 200 200" aria-hidden="true">
  <circle cx="100" cy="100" r="96" fill="#252B40"/>
  <use href="/assets/images/runner.svg#runner" style="color:#E3A2AB"/>
</svg>"""

EVERYDAY_MARK = """<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
  <circle cx="20" cy="20" r="19" fill="#2BA8B8"/>
  <path d="M11 22c3-4 6-4 9 0s6 4 9 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
</svg>"""

# ---------------------------------------------------------------- icons

ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M10 2h4"/></svg>'
ICON_HEART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>'
ICON_STAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg>'
ICON_BAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2"/></svg>'
ICON_SMILE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 14a4 4 0 0 0 7 0M9 9.5h.01M15 9.5h.01"/></svg>'
ICON_PEOPLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5a3 3 0 0 1 0 6M18 14c2 .7 3 2.7 3 6"/></svg>'

# ---------------------------------------------------------------- brands

BRANDS = {
    "cjr": {
        "name": "CJane Run",
        "wordmark": "CJANE RUN",
        "mark": CJR_MARK,
        "badge": CJR_BADGE,
        "body_class": "",
        "fonts": "family=DM+Sans:wght@400;500;700&family=Montserrat:wght@600;700",
        "theme_color": "#1B2030",
        "favicon": "favicon-32.png",
        "touch_icon": "apple-touch-icon.png",
        "og_image": "og-share.png",
        "consent": "get emails from CJane Run",
        "disclaimer": "CJane Run products are in development and not yet for sale.",
        "footer_line": "© 2026 CJane Run · Fuel what’s next.",
        "beliefs": {
            "eyebrow": "Why we exist",
            "title": "Not another gym-bro supplement.",
            "lede": "Most sports nutrition was built for someone else. We’re building ours around the athletes who train for what they can do.",
            "items": [
                (ICON_CLOCK, "Built around your training", "Before practice and after it – made to fit real schedules with school, travel games and two-a-days."),
                (ICON_HEART, "Taste comes first", "If it doesn’t taste great, you won’t use it. We start with flavors you already love and ingredients you recognize."),
                (ICON_STAR, "Confidence, not diet culture", "We’re about energy, recovery and what your body can do. Never weight loss or body transformation."),
            ],
        },
        "join": {
            "title": "Help us build CJane Run.",
            "lede": "We’re developing our products with athletes, not just for them. Join now and help shape what we make.",
        },
        "who": "Athletes 13 and up who train seriously – high school, club and college – and the parents and coaches who support them.",
    },
    "everyday": {
        "name": "Everyday",
        "wordmark": "everyday",
        "mark": EVERYDAY_MARK,
        "badge": "",
        "body_class": "theme-everyday",
        "fonts": "family=Inter:wght@400;500;700",
        "theme_color": "#12414D",
        "favicon": "everyday-favicon-32.png",
        "touch_icon": "everyday-touch-icon.png",
        "og_image": "og-everyday.png",
        # Honest disclosure: the control brand is a CJane Run concept test.
        "consent": "get emails about this product from CJane Run, the team testing it",
        "disclaimer": "Everyday is a product concept being tested by CJane Run. Products are in development and not yet for sale.",
        "footer_line": "© 2026 Everyday",
        "beliefs": {
            "eyebrow": "Why Everyday",
            "title": "Simple, everyday essentials.",
            "lede": "Good-for-you basics that taste great and fit into any routine.",
            "items": [
                (ICON_BAG, "Easy to use", "Tear, pour, shake. One stick fits in any bag, pocket or desk drawer."),
                (ICON_SMILE, "Tastes great", "Flavors you’ll look forward to, with ingredients you recognize."),
                (ICON_PEOPLE, "Made for everyone", "For workdays, workouts, travel and everything in between."),
            ],
        },
        "join": {
            "title": "Be the first to try it.",
            "lede": "We’re getting ready to launch. Join now and help shape what we make.",
        },
        "who": "Anyone who wants an easier way to take care of themselves – at work, at the gym or on the go.",
    },
}

# ---------------------------------------------------------------- products

CJR_BEFORE = {
    "cls": "m-before", "moment": "BEFORE", "name": "Performance stick", "img": "stick-before.svg",
    "alt": "Pink CJane Run 'Before' stick pack",
    "how": "Tear, pour into water and shake about 30 minutes before practice or a game.",
    "facts": [
        ("Built for", "Hydration, steady energy and focus"),
        ("Flavors we’re exploring", "Strawberry, mixed berry"),
    ],
}
CJR_AFTER = {
    "cls": "m-after", "moment": "AFTER", "name": "Recovery stick", "img": "stick-after.svg",
    "alt": "Lavender CJane Run 'After' stick pack",
    "how": "Mix with water, or blend into a smoothie after training.",
    "facts": [
        ("Built for", "Protein to rebuild, carbs to refuel, electrolytes to rehydrate"),
        ("Flavors we’re exploring", "Matcha, banana, almond"),
    ],
}
EVERYDAY_HYDRATION = {
    "cls": "m-hydration", "moment": "HYDRATION", "name": "Everyday Hydration Mix", "img": "stick-everyday-hydration.svg",
    "alt": "Light blue Everyday Hydration Mix stick pack",
    "how": "Tear, pour into water and shake – anytime you need to rehydrate.",
    "facts": [
        ("Built for", "Electrolytes for fast, everyday hydration"),
        ("Flavors we’re exploring", "Strawberry, mixed berry"),
    ],
}
EVERYDAY_RECOVERY = {
    "cls": "m-recovery", "moment": "RECOVERY", "name": "Everyday Recovery Mix", "img": "stick-everyday-recovery.svg",
    "alt": "Sand-colored Everyday Recovery Mix stick pack",
    "how": "Mix with water, or blend into a smoothie or your morning coffee.",
    "facts": [
        ("Built for", "Protein to support recovery and everyday wellness"),
        ("Flavors we’re exploring", "Matcha, banana, almond"),
    ],
}

# ---------------------------------------------------------------- sections


def head(page, brand):
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
<meta property="og:image" content="{SITE}/assets/images/{brand['og_image']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page['title']}">
<meta name="twitter:description" content="{page['description']}">
<meta name="twitter:image" content="{SITE}/assets/images/{brand['og_image']}">
<meta name="theme-color" content="{brand['theme_color']}">
<meta name="facebook-domain-verification" content="c9epdgrilqn1eqrvwwe9vn37ud9xhx" />
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/{brand['favicon']}">
<link rel="apple-touch-icon" href="/assets/images/{brand['touch_icon']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{brand['fonts']}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<script src="/assets/config.js"></script>
<script src="/assets/pixel.js"></script>
<script src="/assets/analytics.js"></script>
<script src="/assets/form.js" defer></script>
</head>
"""


def topbar(brand, home_href, join_href="#join"):
    return f"""<header class="topbar" id="top">
  <div class="wrap">
    <a class="brand" href="{home_href}">{brand['mark']}<span class="brand-name">{brand['wordmark']}</span></a>
    <a class="btn btn-small" href="{join_href}">Join the waitlist</a>
  </div>
</header>
"""


def role_select():
    opts = "".join(f"<option>{r}</option>" for r in ROLES)
    return f"""<select class="select" name="role" required aria-label="I am a…">
        <option value="" disabled selected>I am a…</option>{opts}
      </select>"""


HONEYPOT = '<label class="hp-field" aria-hidden="true"><input type="checkbox" name="website" tabindex="-1"> Leave empty</label>'


def fineprint(brand):
    return (
        '<p class="fineprint">You must be 13 or older to join. By joining, you agree to '
        f'{brand["consent"]}. Unsubscribe anytime. <a href="/privacy/">Privacy policy</a>.</p>'
    )


def hero(page, brand):
    return f"""<section class="hero">
  <div class="wrap">
    <div>
      {brand['badge']}
      <p class="eyebrow">Coming soon</p>
      <h1>{page['h1']}</h1>
      <p class="lede">{page['hero_lede']}</p>
      <form class="waitlist-form" data-hero>
        <div class="field-row">
          <input class="input" type="email" name="email" placeholder="Your email" autocomplete="email" required aria-label="Email address">
          {role_select()}
        </div>
        {HONEYPOT}
        <button class="btn" type="submit">Join the waitlist</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        {fineprint(brand)}
      </form>
    </div>
    <div class="hero-art {page['art_class']}" aria-hidden="true">
      <div class="glow"></div>
      {page['hero_art']}
    </div>
  </div>
</section>
"""


def beliefs(brand):
    b = brand["beliefs"]
    tiles = "".join(
        f"""
      <article class="belief">
        <div class="dot dot-{i}">{icon}</div>
        <h3>{title}</h3>
        <p>{text}</p>
      </article>"""
        for i, (icon, title, text) in enumerate(b["items"], 1)
    )
    return f"""<section class="section beliefs">
  <div class="wrap">
    <p class="eyebrow">{b['eyebrow']}</p>
    <h2>{b['title']}</h2>
    <p class="lede">{b['lede']}</p>
    <div class="beliefs-grid">{tiles}
    </div>
  </div>
</section>
"""


def facts(p):
    return "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["facts"])


def product_card(p):
    return f"""<article class="product {p['cls']}">
        <div class="product-art"><img src="/assets/images/{p['img']}" alt="{p['alt']}"></div>
        <div class="product-body">
          <p class="moment">{p['moment']}</p>
          <h3>{p['name']}</h3>
          <p class="how">{p['how']}</p>
          <dl>{facts(p)}</dl>
        </div>
      </article>"""


def product_feature(p):
    """One product, shown large – used on the single-product ad pages."""
    return f"""<article class="product feature {p['cls']}">
        <div class="product-art"><img src="/assets/images/{p['img']}" alt="{p['alt']}"></div>
        <div class="product-body">
          <p class="moment">{p['moment']}</p>
          <h3>{p['name']}</h3>
          <p class="how">{p['how']}</p>
          <dl>{facts(p)}</dl>
        </div>
      </article>"""


def products(page):
    items = page["products"]
    if len(items) == 1:
        body = product_feature(items[0])
    else:
        body = f'<div class="product-grid two">{"".join(product_card(p) for p in items)}</div>'
    return f"""<section class="section products">
  <div class="wrap">
    <p class="eyebrow">What we’re building</p>
    <h2>{page['products_title']}</h2>
    <p class="lede">{page['products_lede']}</p>
    {body}
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


def join(page, brand):
    j = brand["join"]
    return f"""<section class="section join" id="join">
  <div class="wrap">
    <div>
      <p class="eyebrow">Join the waitlist</p>
      <h2>{j['title']}</h2>
      <p class="lede">{j['lede']}</p>
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
          <legend>What’s your sport? <span class="optional">(optional)</span></legend>
          <input class="input" type="text" name="sport" placeholder="e.g. soccer, volleyball, running" maxlength="60" autocomplete="off">
        </fieldset>
        {HONEYPOT}
        <button class="btn" type="submit">Join the waitlist</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        {fineprint(brand)}
      </form>
    </div>
  </div>
</section>
"""


def faq(page, brand):
    items = [
        ("Can I buy it now?",
         "Not yet – it’s in development. Join the waitlist and you’ll hear first when it’s ready."),
        ("Who is it for?", brand["who"]),
    ] + page["faq"]
    body = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f"""<section class="section faq">
  <div class="wrap">
    <p class="eyebrow">Questions</p>
    <h2>Good to know</h2>
    <div class="faq-list">{body}</div>
  </div>
</section>
"""


def footer(brand):
    return f"""<footer class="footer">
  <div class="wrap">
    <span>{brand['footer_line']}</span>
    <nav><a href="/privacy/">Privacy</a><a href="mailto:{CONTACT}">{CONTACT}</a></nav>
    <p class="disclaimer">{brand['disclaimer']}</p>
  </div>
</footer>
"""


# ---------------------------------------------------------------- pages


def img(name, cls):
    return f'<img class="{cls}" src="/assets/images/{name}" alt="">'


def fan(name):
    """Three of the same stick, fanned – hero art for single-product pages."""
    return img(name, "s1") + img(name, "s2") + img(name, "s3")


CAFFEINE_ANSWER = "We’re testing options, including a caffeine-free version. Tell us what you’d prefer when you join – it will shape what we make."
TEEN_ANSWER = "We’re developing every product with age-appropriate expert guidance, and we’ll share full ingredient lists before launch. Food, water and rest come first – we’re here to make fueling easier, not replace it."
PROTEIN_ANSWER = "We’re developing it with a complete protein and will share the full ingredient list before launch. Tell us what you’d prefer when you join."

PAGES = [
    {
        "file": "index.html", "path": "/", "landing": "home", "brand": "cjr",
        "title": "CJane Run – Fuel what’s next.",
        "description": "Great-tasting sports nutrition built around how you actually train. CJane Run is coming soon – join the waitlist.",
        "h1": 'Fuel what’s <span class="accent">next.</span>',
        "hero_lede": "Great-tasting nutrition built around how you actually train. Tear, pour, shake – before practice and after it.",
        "art_class": "art-pair",
        "hero_art": img("stick-before.svg", "s1") + img("stick-after.svg", "s2"),
        "products": [CJR_BEFORE, CJR_AFTER],
        "products_title": "Two moments. One routine.",
        "products_lede": "Light sticks you mix with water – one before practice, one after. Both fit in your gym bag.",
        "question": {"name": "first_pick", "legend": "Which would you try first?", "options": ["Before stick", "After stick", "Both"]},
        "faq": [("Will the Before stick have caffeine?", CAFFEINE_ANSWER), ("Is it right for teen athletes?", TEEN_ANSWER)],
    },
    {
        "file": "pre/index.html", "path": "/pre/", "landing": "cjr_pre", "brand": "cjr",
        "title": "CJane Run Before stick – Fuel what’s next.",
        "description": "Great-tasting pre-practice fuel built around how you actually train. Join the CJane Run waitlist.",
        "h1": 'Fuel what’s <span class="accent">next.</span>',
        "hero_lede": "The Before stick: great-tasting pre-practice fuel built around how you actually train. Tear, pour, shake – 30 minutes before you play.",
        "art_class": "art-single",
        "hero_art": fan("stick-before.svg"),
        "products": [CJR_BEFORE],
        "products_title": "Meet the Before stick.",
        "products_lede": "Light enough for your gym bag, easy enough to mix on the way to practice.",
        "question": USE_FREQ,
        "faq": [("Will the Before stick have caffeine?", CAFFEINE_ANSWER), ("Is it right for teen athletes?", TEEN_ANSWER)],
    },
    {
        "file": "post/index.html", "path": "/post/", "landing": "cjr_post", "brand": "cjr",
        "title": "CJane Run After stick – Fuel what’s next.",
        "description": "Great-tasting recovery built around how you actually train. Join the CJane Run waitlist.",
        "h1": 'Fuel what’s <span class="accent">next.</span>',
        "hero_lede": "The After stick: great-tasting recovery built around how you actually train. Mix it after practice to refuel, rebuild and rehydrate.",
        "art_class": "art-single",
        "hero_art": fan("stick-after.svg"),
        "products": [CJR_AFTER],
        "products_title": "Meet the After stick.",
        "products_lede": "Everything you need after training, in one stick you can mix anywhere.",
        "question": USE_FREQ,
        "faq": [("What kind of protein is in it?", PROTEIN_ANSWER), ("Is it right for teen athletes?", TEEN_ANSWER)],
    },
    {
        "file": "hydrate/index.html", "path": "/hydrate/", "landing": "generic_pre", "brand": "everyday",
        "title": "Everyday Hydration Mix",
        "description": "An easy electrolyte drink mix for everyday hydration. Join the waitlist.",
        "h1": 'Hydration, made <span class="accent">easy.</span>',
        "hero_lede": "Everyday Hydration Mix is an electrolyte drink mix for busy days. Tear, pour, shake – anytime, anywhere.",
        "art_class": "art-single",
        "hero_art": fan("stick-everyday-hydration.svg"),
        "products": [EVERYDAY_HYDRATION],
        "products_title": "Meet Everyday Hydration Mix.",
        "products_lede": "Light enough for any bag, easy enough to mix anywhere.",
        "question": USE_FREQ,
        "faq": [("Will it have caffeine?", CAFFEINE_ANSWER), ("What’s in it?", "Electrolytes – sodium, potassium and magnesium – in a great-tasting mix. We’ll share the full ingredient list before launch.")],
    },
    {
        "file": "recover/index.html", "path": "/recover/", "landing": "generic_post", "brand": "everyday",
        "title": "Everyday Recovery Mix",
        "description": "An easy protein drink mix for recovery and everyday wellness. Join the waitlist.",
        "h1": 'Recovery, made <span class="accent">easy.</span>',
        "hero_lede": "Everyday Recovery Mix is a protein drink mix for recovery and everyday wellness. Mix it with water or blend it into a smoothie.",
        "art_class": "art-single",
        "hero_art": fan("stick-everyday-recovery.svg"),
        "products": [EVERYDAY_RECOVERY],
        "products_title": "Meet Everyday Recovery Mix.",
        "products_lede": "Protein you can mix anywhere, in one easy stick.",
        "question": USE_FREQ,
        "faq": [("What kind of protein is in it?", PROTEIN_ANSWER), ("What’s in it?", "Protein to support recovery, plus electrolytes, in a great-tasting mix. We’ll share the full ingredient list before launch.")],
    },
]


def build(page):
    brand = BRANDS[page["brand"]]
    # Ad pages link the logo to their own top, so ad traffic never crosses cells.
    home_href = "/" if page["landing"] == "home" else "#top"
    body_class = f' class="{brand["body_class"]}"' if brand["body_class"] else ""
    html = (
        head(page, brand)
        + f'<body{body_class} data-landing="{page["landing"]}">\n'
        + topbar(brand, home_href)
        + "<main>\n"
        + hero(page, brand)
        + beliefs(brand)
        + products(page)
        + join(page, brand)
        + faq(page, brand)
        + "</main>\n"
        + footer(brand)
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
    <p>CJane Run (“we,” “us”) is a brand in development. This policy explains what we collect on cjanerun.store – including pages for product concepts we test under other names, such as Everyday – and how we use it.</p>

    <h2>What we collect</h2>
    <ul>
      <li><strong>What you give us:</strong> your email address and any answers you choose to share when you join a waitlist (such as whether you’re an athlete, parent or coach, your sport and how often you’d use a product).</li>
      <li><strong>Visit information:</strong> the page you signed up on and any campaign tags in the link you followed (for example, which ad you clicked).</li>
      <li><strong>Advertising measurement:</strong> we use the Meta Pixel to understand whether our ads on Facebook and Instagram lead to waitlist signups. The pixel uses cookies and similar technology to record page visits and signups.</li>
      <li><strong>Site analytics:</strong> we use Google Analytics to understand how visitors use our pages – for example, which pages they view, how long they stay and whether they join a waitlist. It uses cookies and collects information such as your approximate location, device and browser.</li>
    </ul>

    <h2>How we use it</h2>
    <ul>
      <li>To send you updates about the product you signed up for, including launch news and invitations to share feedback.</li>
      <li>To learn which product ideas people are most interested in, so we can decide what to build.</li>
      <li>To measure and improve our advertising.</li>
    </ul>
    <p>We don’t sell your personal information.</p>

    <h2>Who helps us</h2>
    <p>We use Klaviyo to store our waitlists and send email, Meta for advertising measurement, Google Analytics for site analytics, and Cloudflare to host this site. They process data on our behalf under their own privacy terms.</p>

    <h2>Your choices</h2>
    <ul>
      <li>Every email includes an unsubscribe link.</li>
      <li>To see, correct or delete the information we hold about you, email <a href="mailto:{CONTACT}">{CONTACT}</a>.</li>
      <li>You can limit ad tracking in your Facebook/Instagram ad settings and your browser’s cookie settings, and opt out of Google Analytics with Google’s <a href="https://tools.google.com/dlpage/gaoptout">browser add-on</a>.</li>
    </ul>

    <h2>Children</h2>
    <p>Our waitlists are for people 13 and older. We don’t knowingly collect information from children under 13. If you believe a child under 13 has signed up, email us and we’ll delete it.</p>

    <h2>Changes</h2>
    <p>If we update this policy, we’ll change the date at the top of this page.</p>

    <h2>Contact</h2>
    <p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
  </div>
</section>
"""


def build_privacy():
    brand = BRANDS["cjr"]
    page = {
        "path": "/privacy/",
        "title": "Privacy policy – CJane Run",
        "description": "How CJane Run collects and uses information on cjanerun.store.",
    }
    html = (
        head(page, brand)
        + '<body data-landing="privacy">\n'
        + topbar(brand, "/", "/#join")
        + "<main>\n" + PRIVACY + "</main>\n"
        + footer(brand)
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
