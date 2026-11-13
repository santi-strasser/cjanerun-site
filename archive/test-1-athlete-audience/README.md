# Test 1 – landing pages (athlete audience)

Documentation copy of the landing pages used for the first Meta test. These
files are **not served** by the site (they sit outside `public/`).

| | |
|---|---|
| Run | Nov 5–11, 2026 (campaign `CJR_EVD_WL_TEST_LEADS_20261104`) |
| Audience | US, age 18+, women 18–26 and sport interests (suggestions under Advantage+) |
| Messaging | Athlete-first: "Fuel what's next." (CJane Run) and "Hydration and recovery, made easy." (Everyday) |
| Form | Email only, "You must be 13 or older to join" |
| `signup_page` values | `cjr` and `everyday` |
| Code state | Git tag `test1-landing-pages` (commit `4181b9a`) |

Files:
- `cjanerun-store_index.html` – the CJane Run page (`/`)
- `everyday_index.html` – the Everyday page (`/everyday/`)
- `privacy_index.html` – the privacy policy as it read then
- `build_test1.py` – the generator with the test 1 copy

The HTML references `/assets/...`, so to see a page as it looked, check out the
tag (`git checkout test1-landing-pages`) and open `public/index.html`.

## Results (Klaviyo = count of record)

| | CJane Run | Everyday |
|---|---|---|
| Spend | $64.65 | $65.31 |
| Reach | 1,068 | 892 |
| Link clicks / CTR | 54 / 3.06% | 83 / 5.65% |
| Emails | 5 | 2 |
| Emails / reach | 0.47% | 0.22% |

Everyday's CTR came from one Reel (17% CTR, no emails); without it the CTRs
were about equal. Meta concentrated delivery unevenly across ads.

## Test 2 (parent audience)

From Nov 13, 2026 the live pages at `/` and `/everyday/` are parent-facing and
daughter-first, with an adults-only form (`signup_page` = `cjr-parents` and
`everyday-parents`). See the main `README.md`.
