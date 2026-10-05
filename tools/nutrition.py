"""Draft facts panels for the four test products.

Values are ESTIMATES calculated from the target formula in "Pre Post Game.pptx"
(CJane Run) and from an assumed, typical category formula (Everyday) – not lab
results. FORMULAS holds the ingredient build behind each panel; change a gram
amount there, then rebuild the site (python tools/build.py).

    python tools/nutrition.py                # print the calculated totals
    python tools/nutrition.py --export DIR   # also save each panel as a PNG in DIR
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Per gram of ingredient: kcal, fat, sat fat, carbs, fibre, sugars, added sugars,
# protein (g) and sodium, iron (mg). Typical supplier values – confirm with specs.
ING = {
    "cane sugar":          dict(kcal=4.0, fat=0, sat=0, carb=1.0, fiber=0, sugar=1.0, added=1.0, protein=0, sodium=0, iron=0),
    "coconut milk powder": dict(kcal=6.8, fat=.65, sat=.58, carb=.22, fiber=0, sugar=.07, added=0, protein=.06, sodium=.6, iron=0),
    "almond milk powder":  dict(kcal=6.0, fat=.50, sat=.04, carb=.20, fiber=.10, sugar=.05, added=0, protein=.21, sodium=0, iron=.03),
    "pea + rice protein":  dict(kcal=4.0, fat=.07, sat=.015, carb=.04, fiber=.02, sugar=0, added=0, protein=.80, sodium=10.8, iron=.21),
    "prebiotic fiber":     dict(kcal=1.6, fat=0, sat=0, carb=1.0, fiber=1.0, sugar=0, added=0, protein=0, sodium=0, iron=0),
    "matcha powder":       dict(kcal=3.0, fat=.05, sat=0, carb=.40, fiber=.38, sugar=0, added=0, protein=.30, sodium=0, iron=.17),
    "flavor + acid":       dict(kcal=2.0, fat=0, sat=0, carb=.60, fiber=0, sugar=0, added=0, protein=0, sodium=0, iron=0),
}

# Grams per serving. Actives and electrolyte salts add weight but no calories.
FORMULAS = {
    "cjr-before": {"cane sugar": 24, "coconut milk powder": 8, "flavor + acid": 2, "_actives": 8.2, "_salts": 4.5},
    "cjr-after": {"pea + rice protein": 23, "cane sugar": 25, "almond milk powder": 8, "prebiotic fiber": 5,
                  "matcha powder": 1, "flavor + acid": 1.5, "_actives": 3, "_salts": 3.8},
    "everyday-hydration": {"cane sugar": 10, "flavor + acid": 1.7, "_salts": 4.3},
    "everyday-recovery": {"pea + rice protein": 25, "cane sugar": 3, "matcha powder": 1, "flavor + acid": 1, "_salts": 1.5},
}

DV = dict(fat=78, sat=20, carb=275, fiber=28, added=50, sodium=2300)          # FDA Daily Values
MINERAL_DV = dict(potassium=4700, magnesium=420, iron=18, calcium=1300)


def totals(key):
    t = dict.fromkeys(next(iter(ING.values())), 0.0)
    for name, grams in FORMULAS[key].items():
        if not name.startswith("_"):
            for k, v in ING[name].items():
                t[k] += v * grams
    t["weight"] = sum(FORMULAS[key].values())
    return t


# FDA rounding rules (21 CFR 101.9) ------------------------------------------------
def r_kcal(x):  return 0 if x < 5 else (round(x / 5) * 5 if x <= 50 else round(x / 10) * 10)
def r_fat(x):   return 0 if x < .5 else (round(x * 2) / 2 if x < 5 else round(x))
def r_gram(x):  return 0 if x < .5 else round(x)
def pct(x, dv): return f"{round(100 * x / dv)}%"


def mineral_pct(x, dv):
    p = 100 * x / dv
    step = 2 if p <= 10 else 5 if p <= 50 else 10
    return f"{int(round(p / step) * step)}%"


def row(label, amount, dv, indent, bold):
    name = f"<b>{label}</b>" if bold else label
    return f'<div class="nf-r nf-i{indent}"><span>{name} {amount}</span><span class="nf-b">{dv}</span></div>'


def macro_rows(key, supplement):
    """Rows shared by both panel types: (label, amount, %DV, indent level, bold)."""
    t = totals(key)
    fat, sat = r_fat(t["fat"]), r_fat(t["sat"])
    carb, fiber, sugar, added, protein = (r_gram(t[k]) for k in ("carb", "fiber", "sugar", "added", "protein"))
    added = min(added, sugar)
    rows = [("Total Fat", f"{fat:g}g", pct(t["fat"] if fat else 0, DV["fat"]), 0, True),
            ("Saturated Fat", f"{sat:g}g", pct(t["sat"] if sat else 0, DV["sat"]), 1, False)]
    if not supplement:
        rows += [("<i>Trans</i> Fat", "0g", "", 1, False), ("Cholesterol", "0mg", "0%", 0, True)]
    carbs = [("Total Carbohydrate", f"{carb}g", pct(t["carb"], DV["carb"]), 0, True),
             ("Dietary Fiber", f"{fiber}g", pct(t["fiber"] if fiber else 0, DV["fiber"]), 1, False),
             ("Total Sugars", f"{sugar}g", "†" if supplement else "", 1, False),
             (f"Includes {added}g Added Sugars", "", pct(t["added"], DV["added"]), 2, False),
             ("Protein", f"{protein}g", "", 0, True)]
    if supplement:      # Supplement Facts leaves out nutrients present at zero
        rows = [r for r in rows if r[1] != "0g"]
        carbs = [r for r in carbs if r[1] != "0g"]
    return t, rows, carbs


def nutrition_facts(key, serving, sodium, minerals):
    t, fats, carbs = macro_rows(key, False)
    rows = fats + [("Sodium", f"{sodium}mg", pct(sodium, DV["sodium"]), 0, True)] + carbs
    mins = "".join(
        f'<div class="nf-r"><span>{name} {amt}</span><span>{mineral_pct(val, MINERAL_DV[k]) if k else "0%"}</span></div>'
        for name, amt, val, k in minerals)
    return f"""<div class="nf">
  <div class="nf-title">Nutrition Facts</div>
  <div class="nf-serv">1 serving per container</div>
  <div class="nf-serv nf-b nf-sz"><span>Serving size</span><span>{serving} ({round(t['weight'])}g)</span></div>
  <div class="nf-bar nf-thick"></div>
  <div class="nf-small nf-b">Amount per serving</div>
  <div class="nf-cal"><span>Calories</span><span>{r_kcal(t['kcal'])}</span></div>
  <div class="nf-bar nf-mid"></div>
  <div class="nf-r nf-right nf-b nf-small">% Daily Value*</div>
  {"".join(row(*r) for r in rows)}
  <div class="nf-bar nf-thick"></div>
  {mins}
  <div class="nf-bar nf-mid"></div>
  <div class="nf-foot">* The % Daily Value (DV) tells you how much a nutrient in a serving of food contributes to a daily diet. 2,000 calories a day is used for general nutrition advice.</div>
</div>"""


def supplement_facts(key, serving, sodium, potassium, magnesium, others, note=""):
    t, fats, carbs = macro_rows(key, True)
    macros = [(a, b[:-1] + " g" if b.endswith("g") else b, c + "*" if c.endswith("%") else c, d, e) for a, b, c, d, e in fats + carbs]
    rows = [("Calories", str(r_kcal(t["kcal"])), "", 0, True)] + macros
    if round(t["iron"]) >= 1:
        rows.append(("Iron", f"{round(t['iron'])} mg", mineral_pct(t["iron"], MINERAL_DV["iron"]), 0, True))
    rows += [("Magnesium", f"{magnesium} mg", mineral_pct(magnesium, MINERAL_DV["magnesium"]), 0, True),
             ("Sodium", f"{sodium} mg", pct(sodium, DV["sodium"]), 0, True),
             ("Potassium", f"{potassium} mg", mineral_pct(potassium, MINERAL_DV["potassium"]), 0, True)]
    return f"""<div class="nf nf-supp">
  <div class="nf-title">Supplement Facts</div>
  <div class="nf-serv">Serving Size: {serving} ({round(t['weight'])} g)</div>
  <div class="nf-serv">Servings Per Container: 1</div>
  <div class="nf-bar nf-thick"></div>
  <div class="nf-r nf-b nf-small nf-head"><span>Amount Per Serving</span><span>% Daily Value</span></div>
  <div class="nf-bar nf-mid"></div>
  {"".join(row(*r) for r in rows)}
  <div class="nf-bar nf-thick"></div>
  {"".join(row(name, amt, "†", 0, True) for name, amt in others)}
  <div class="nf-bar nf-thick"></div>
  <div class="nf-foot">* Percent Daily Values are based on a 2,000 calorie diet.<br>† Daily Value not established.{note}</div>
</div>"""


PANELS = {
    "cjr-before": lambda: supplement_facts(
        "cjr-before", "1 stick", sodium=500, potassium=400, magnesium=300,
        others=[("Creatine Monohydrate", "3 g"), ("L-Citrulline", "3 g"), ("Taurine", "1 g"),
                ("Beta-Alanine", "500 mg"), ("Lion’s Mane Mushroom Extract", "500 mg"),
                ("L-Theanine", "100 mg"), ("Caffeine", "90 mg")]),
    "cjr-after": lambda: supplement_facts(
        "cjr-after", "1 stick", sodium=500, potassium=400, magnesium=300,
        others=[("Creatine Monohydrate", "3 g"), ("Matcha Green Tea Powder", "1 g")],
        note="<br>Matcha naturally contains about 30 mg of caffeine per serving."),
    "everyday-hydration": lambda: nutrition_facts(
        "everyday-hydration", "1 stick", sodium=500,
        minerals=[("Vitamin D", "0mcg", 0, None), ("Calcium", "0mg", 0, None), ("Iron", "0mg", 0, None),
                  ("Potassium", "400mg", 400, "potassium"), ("Magnesium", "60mg", 60, "magnesium")]),
    "everyday-recovery": lambda: nutrition_facts(
        "everyday-recovery", "1 stick", sodium=350,
        minerals=[("Vitamin D", "0mcg", 0, None), ("Calcium", "30mg", 30, "calcium"), ("Iron", "5mg", 5, "iron"),
                  ("Potassium", "200mg", 200, "potassium")]),
}

# "What's inside" – the headline ingredients, grouped by what they're there for.
INSIDE = {
    "cjr-before": [
        ("Energy", [("Cane sugar + coconut milk", "150 calories"), ("Caffeine", "90mg"), ("Taurine", "1g"),
                    ("Creatine", "3g"), ("Beta-alanine", "500mg"), ("L-citrulline", "3g")]),
        ("Focus", [("L-theanine", "100mg"), ("Lion’s mane", "500mg")]),
        ("Hydration", [("Sodium", "500mg"), ("Potassium", "400mg"), ("Magnesium", "300mg")]),
    ],
    "cjr-after": [
        ("Refuel", [("Cane sugar + almond milk", "34g carbs"), ("Fiber, incl. prebiotic", "7g")]),
        ("Rebuild", [("Complete plant protein", "20g"), ("Creatine", "3g"), ("Matcha", "1g")]),
        ("Rehydrate", [("Sodium", "500mg"), ("Potassium", "400mg"), ("Magnesium", "300mg")]),
    ],
    "everyday-hydration": [
        ("Hydration", [("Sodium", "500mg"), ("Potassium", "400mg"), ("Magnesium", "60mg")]),
        ("Energy", [("Cane sugar", "10g"), ("Calories", "45")]),
    ],
    "everyday-recovery": [
        ("Recovery", [("Complete plant protein", "20g"), ("Cane sugar", "3g"), ("Calories", "120")]),
        ("Hydration", [("Sodium", "350mg"), ("Potassium", "200mg")]),
    ],
}


def export(dest):
    """Save each panel as a PNG, styled with the same CSS the site uses."""
    from PIL import Image, ImageChops
    css = re.search(r"/\* nf:start \*/(.*?)/\* nf:end \*/", (ROOT / "public/assets/styles.css").read_text(encoding="utf-8"), re.S).group(1)
    dest.mkdir(parents=True, exist_ok=True)
    for key, build in PANELS.items():
        html = (f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:24px;background:#fff}}{css}</style></head>'
                f'<body>{build()}</body></html>')
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            page = Path(f.name)
        out = dest / f"facts-{key}.png"
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=3",
                        "--window-size=500,900", f"--screenshot={out}", page.as_uri()], capture_output=True)
        page.unlink()
        im = Image.open(out).convert("RGB")
        box = ImageChops.difference(im, Image.new("RGB", im.size, "#fff")).getbbox()
        im.crop((max(0, box[0] - 30), max(0, box[1] - 30), min(im.width, box[2] + 30), min(im.height, box[3] + 30))).save(out, optimize=True)
        print("wrote", out)


if __name__ == "__main__":
    for key in FORMULAS:
        t = totals(key)
        print(f"{key:20s} {t['weight']:5.1f} g  {t['kcal']:4.0f} kcal  fat {t['fat']:.1f}  sat {t['sat']:.1f}  carb {t['carb']:.1f}  "
              f"fiber {t['fiber']:.1f}  added sugar {t['added']:.1f}  protein {t['protein']:.1f}  iron {t['iron']:.1f} mg")
    if "--export" in sys.argv:
        export(Path(sys.argv[sys.argv.index("--export") + 1]).resolve())
