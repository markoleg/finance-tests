# -*- coding: utf-8 -*-
"""Збирає готовий статичний сайт у папку «docs» з банків питань (*.json).

docs/ — це корінь сайту для GitHub Pages (Settings → Pages → Deploy from branch → /docs).
Вихідники (цей скрипт, generators/, *.json) лишаються в корені й у репозиторії.

Лендінг -> docs/index.html, тести -> docs/variant-N.html, спільні стилі/рушій -> docs/assets/.
"""
import json, os

OUT_DIR = "docs"
os.makedirs(OUT_DIR, exist_ok=True)

PAGE = r"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:type" content="website">
<meta property="og:locale" content="uk_UA">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="assets/quiz.css">
<style>:root{--brand:__BRAND__;--brand-d:__BRANDD__;--hover:__HOVER__}</style>
</head>
<body>
<header>
  <h1>__H1__</h1>
  <p>__SUB__</p>
  <a class="back" href="index.html">&larr; Усі тести</a>
</header>

<div class="bar">
  <div class="info">Опрацьовано: <b id="answered">0</b> / <span id="total1"></span></div>
  <div class="info">Максимум: <b id="total2"></b> балів</div>
</div>

<div class="wrap" id="quiz"></div>

<footer>__FOOT__<div class="disclaimer">Неофіційний ресурс для самопідготовки. Не пов’язаний з МОН України чи УЦОЯО. Завдання авторські й не є офіційними завданнями ЄФВВ.</div></footer>

<div class="abar" id="abar">
  <div class="abar-inner">
    <div class="result" id="result">
      <span class="score" id="scoreLine"></span>
      <span class="pct" id="pctLine"></span>
      <span class="grade" id="gradeBadge"></span>
    </div>
    <div class="abar-btns">
      <button class="btn primary" id="check">Перевірити результат</button>
      <button class="btn ghost" id="reset">Пройти заново</button>
    </div>
  </div>
</div>

<script>const QUESTIONS = __DATA__;</script>
<script src="assets/quiz.js"></script>
</body>
</html>"""

def build(cfg):
    qs = json.load(open(cfg["json"], encoding="utf-8"))
    data = json.dumps(qs, ensure_ascii=False)
    html = (PAGE
            .replace("__TITLE__", cfg["title"])
            .replace("__DESC__", cfg["sub"])
            .replace("__H1__", cfg["h1"])
            .replace("__SUB__", cfg["sub"])
            .replace("__FOOT__", cfg["foot"])
            .replace("__BRANDD__", cfg["brand_d"])
            .replace("__BRAND__", cfg["brand"])
            .replace("__HOVER__", cfg["hover"])
            .replace("__DATA__", data))
    path = os.path.join(OUT_DIR, cfg["file"])
    open(path, "w", encoding="utf-8").write(html)
    print("OK:", path, "-", len(qs), "питань")
    return len(qs)

# Офіційний тест ЄФВВ-2024 НЕ публікується (авторські права на офіційні завдання ДУ «НМЦ»).
# Для локального використання можна додати назад у TESTS:
#   {"json": "questions.json", "file": "official-2024.html",
#    "title": "ЄФВВ-2024 — Облік та фінанси (офіційний)",
#    "h1": "Єдине фахове вступне випробування — 2024",
#    "sub": "Облік та фінанси · офіційні завдання · 1 бал за кожну правильну відповідь",
#    "foot": "© ДУ «Науково-методичний центр вищої та фахової передвищої освіти», 2024.",
#    "brand": "#2563eb", "brand_d": "#1d4ed8", "hover": "#f8faff"},

TESTS = [
    {"json": "questions2025.json",
     "file": "variant-1.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 1, легкий)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 1 (легкий)",
     "sub": "Облік та фінанси · легкий рівень · пробний тест за програмою (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Пробний тест укладено за офіційною програмою ЄФВВ. Легкий рівень. Для самопідготовки.",
     "brand": "#0f766e", "brand_d": "#0d5d57", "hover": "#f1fbf9"},
    {"json": "questions2025_v2.json",
     "file": "variant-2.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 2, легкий)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 2 (легкий)",
     "sub": "Облік та фінанси · легкий рівень · пробний тест за програмою (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Пробний тест укладено за офіційною програмою ЄФВВ. Легкий рівень. Для самопідготовки.",
     "brand": "#7c3aed", "brand_d": "#6d28d9", "hover": "#f7f4ff"},
    {"json": "questions2025_v3.json",
     "file": "variant-3.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 3, середній)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 3 (середній)",
     "sub": "Облік та фінанси · середній рівень · поглиблений пробний тест з розширеними поясненнями · програма (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Поглиблений пробний тест за офіційною програмою ЄФВВ. Середній рівень: більше розрахункових завдань і розширені пояснення. Для самопідготовки.",
     "brand": "#c2410c", "brand_d": "#9a3412", "hover": "#fff7ed"},
    {"json": "questions2025_v4.json",
     "file": "variant-4.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 4, середній)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 4 (середній)",
     "sub": "Облік та фінанси · середній рівень · поглиблений пробний тест з розширеними поясненнями · унікальні завдання · програма (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Поглиблений пробний тест за офіційною програмою ЄФВВ. Середній рівень: унікальні завдання, багато розрахунків і розширені пояснення. Для самопідготовки.",
     "brand": "#be123c", "brand_d": "#9f1239", "hover": "#fff1f2"},
    {"json": "questions2025_v5.json",
     "file": "variant-5.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 5, складний)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 5 (складний)",
     "sub": "Облік та фінанси · складний рівень · 20 розрахункових + 120 теоретичних завдань підвищеної складності · унікальні завдання · програма (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Складний пробний тест за офіційною програмою ЄФВВ: теоретичні завдання підвищеної складності та 20 розрахункових. Унікальні завдання з розширеними поясненнями. Для самопідготовки.",
     "brand": "#4338ca", "brand_d": "#3730a3", "hover": "#eef2ff"},
    {"json": "questions2025_v6.json",
     "file": "variant-6.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 6, екзаменаційний рівень)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 6 (екзаменаційний рівень)",
     "sub": "Облік та фінанси · екзаменаційний рівень за зразком офіційного тесту 2024 · переважно прикладні завдання (обчислення для вибору відповіді) · унікальні завдання · програма (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Пробний тест екзаменаційного рівня, укладений за зразком офіційного тесту 2024 року: переважно прикладні завдання з обчисленнями та близькими дистракторами. Унікальні завдання з поясненнями. Для самопідготовки.",
     "brand": "#334155", "brand_d": "#1e293b", "hover": "#f1f5f9"},
    {"json": "questions2025_v7.json",
     "file": "variant-7.html",
     "title": "ЄФВВ-2026 — Облік та фінанси (варіант 7, екзаменаційний рівень)",
     "h1": "Єдине фахове вступне випробування — 2026 · Варіант 7 (екзаменаційний рівень)",
     "sub": "Облік та фінанси · екзаменаційний рівень за зразком офіційного тесту 2024 · переважно прикладні завдання (обчислення для вибору відповіді) · унікальні завдання · програма (наказ МОН від 15.10.2025 № 1362)",
     "foot": "Пробний тест екзаменаційного рівня, укладений за зразком офіційного тесту 2024 року: переважно прикладні завдання з обчисленнями та близькими дистракторами. Унікальні завдання з поясненнями. Для самопідготовки.",
     "brand": "#0e7490", "brand_d": "#155e75", "hover": "#ecfeff"},
]

cards = []
for t in TESTS:
    n = build(t)
    cards.append((t, n))

# ----- лендінг index.html -----
card_html = ""
for t, n in cards:
    card_html += (
        '<a class="card" style="--c:{brand};--cd:{brand_d}" href="{file}">'
        '<div class="cn">{h1}</div>'
        '<div class="cd">{sub}</div>'
        '<div class="cb">{n} завдань · максимум {n} балів</div>'
        '<div class="go">Почати тест →</div>'
        '</a>\n'
    ).format(brand=t["brand"], brand_d=t["brand_d"], file=t["file"],
             h1=t["h1"], sub=t["sub"], n=n)

FORMULY_CARD = ('<a class="card" style="--c:#16a34a;--cd:#15803d" href="formulas.html">'
  '<div class="cn">📘 Формули · Облік та фінанси</div>'
  '<div class="cd">Формульний лист за розділами програми · з пошуком і поясненнями</div>'
  '<div class="cb">Позначення · шаблони задач · чек-лист</div>'
  '<div class="go">Переглянути формули →</div></a>\n')

LANDING = """<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Тести ЄФВВ · Облік та фінанси</title>
<meta name="description" content="Безкоштовні пробні тести ЄФВВ з обліку та фінансів: варіанти різної складності з миттєвою перевіркою та формульний лист. Для самопідготовки до вступу в магістратуру.">
<meta property="og:type" content="website">
<meta property="og:locale" content="uk_UA">
<meta property="og:title" content="Тести ЄФВВ · Облік та фінанси">
<meta property="og:description" content="Безкоштовні пробні тести ЄФВВ з обліку та фінансів + формульний лист. Варіанти різної складності з миттєвою перевіркою.">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/favicon.svg">
<style>
  body{margin:0;font-family:'Segoe UI',system-ui,Arial,sans-serif;background:#f4f6fb;color:#1c2433;line-height:1.5}
  header{background:linear-gradient(135deg,#1e293b,#334155);color:#fff;padding:36px 20px;text-align:center}
  header h1{margin:0 0 6px;font-size:1.7rem}
  header p{margin:0;opacity:.9}
  .wrap{max-width:760px;margin:0 auto;padding:24px 20px 40px}
  .card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #e3e8f0;
        border-left:6px solid var(--c);border-radius:14px;padding:20px 22px;margin:16px 0;
        box-shadow:0 1px 3px rgba(20,30,60,.05);transition:.15s}
  .card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(20,30,60,.10)}
  .card .cn{font-size:1.15rem;font-weight:700;color:var(--cd)}
  .card .cd{color:#6b7280;font-size:.92rem;margin-top:4px}
  .card .cb{color:#1c2433;font-size:.9rem;margin-top:10px;font-weight:600}
  .card .go{margin-top:12px;display:inline-block;color:#fff;background:var(--c);
            padding:8px 18px;border-radius:9px;font-weight:700;font-size:.9rem}
  footer{text-align:center;color:#6b7280;font-size:.8rem;padding:20px}
  .disclaimer{max-width:660px;margin:10px auto 0;font-size:.72rem;line-height:1.45;color:#6b7280;opacity:.85}
</style>
</head>
<body>
<header>
  <h1>Тести · Облік та фінанси</h1>
  <p>Єдине фахове вступне випробування · оберіть тест для проходження</p>
</header>
<div class="wrap">
""" + FORMULY_CARD + card_html + """</div>
<footer>1 бал за кожну правильну відповідь · результат і правильні відповіді показуються після перевірки · для самопідготовки<div class="disclaimer">Неофіційний ресурс для самопідготовки. Не пов’язаний з МОН України чи УЦОЯО. Завдання авторські й не є офіційними завданнями ЄФВВ.</div></footer>
</body>
</html>"""

open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(LANDING)
print("OK:", os.path.join(OUT_DIR, "index.html"))
