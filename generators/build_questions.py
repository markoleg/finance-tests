# -*- coding: utf-8 -*-
"""Єдиний генератор банків питань ЄФВВ (Облік та фінанси).

Запускає всі генератори варіантів у правильному порядку та відтворює
банки questions2025*.json у корені проєкту. Це єдина точка входу — більше
не треба пам'ятати, який скрипт за чим запускати.

Пайплайн (порядок важливий):
  Варіанти 1–2:  gen2025.py / gen2025_v2.py  ->  банк БЕЗ пояснень
                 enrich.py                    ->  додає пояснення (explain) in-place
  Варіанти 3–7:  gen2025_v3..v7.py            ->  банк з поясненнями одразу

questions.json (офіційний тест ЄФВВ-2024) — зовнішній банк, тут НЕ генерується.

Запуск:   python generators/build_questions.py
Далі:     python build.py        # збирає HTML-сторінки з готових JSON
"""
import subprocess, sys, os, json, re

# друкуємо в UTF-8 незалежно від кодування консолі Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # корінь проєкту — туди пишуться JSON

# (скрипт, опис). enrich.py МАЄ йти після gen2025 / gen2025_v2.
PIPELINE = [
    ("gen2025.py",    "questions2025.json     · варіант 1 (легкий) — без пояснень"),
    ("gen2025_v2.py", "questions2025_v2.json  · варіант 2 (легкий) — без пояснень"),
    ("enrich.py",     "+ додає пояснення до варіантів 1 і 2"),
    ("gen2025_v3.py", "questions2025_v3.json  · варіант 3 (середній)"),
    ("gen2025_v4.py", "questions2025_v4.json  · варіант 4 (середній)"),
    ("gen2025_v5.py", "questions2025_v5.json  · варіант 5 (складний)"),
    ("gen2025_v6.py", "questions2025_v6.json  · варіант 6 (екзаменаційний)"),
    ("gen2025_v7.py", "questions2025_v7.json  · варіант 7 (екзаменаційний)"),
]


# банки варіантів у порядку пріоритету (перше входження питання лишається)
VARIANT_BANKS = [
    "questions2025.json", "questions2025_v2.json", "questions2025_v3.json",
    "questions2025_v4.json", "questions2025_v5.json", "questions2025_v6.json",
    "questions2025_v7.json",
]


def _norm(s):
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[’‘“”\"]", "", s)
    return s


# додаткові унікальні питання, якими добиваємо банк назад до потрібної кількості
# (після видалення дублікатів). Ключ — банк, значення — файл з питаннями.
EXTRA = {
    "questions2025_v3.json": "extra_v3.json",
}


def dedupe():
    """Прибирає питання, що повторюються МІЖ варіантами (лишає перше входження
    за порядком VARIANT_BANKS), за потреби добиває банк унікальними питаннями
    з EXTRA, і перенумеровує кожен банк 1..N."""
    seen = set()
    total_removed = total_added = 0
    for fn in VARIANT_BANKS:
        path = os.path.join(ROOT, fn)
        qs = json.load(open(path, encoding="utf-8"))
        out = []
        for q in qs:
            k = _norm(q["q"])
            if k in seen:
                continue
            seen.add(k)
            out.append(q)
        removed = len(qs) - len(out)

        added = 0
        if fn in EXTRA:
            extra = json.load(open(os.path.join(HERE, EXTRA[fn]), encoding="utf-8"))
            for q in extra:
                k = _norm(q["q"])
                if k in seen:          # не додаємо, якщо таке питання вже десь є
                    continue
                seen.add(k)
                out.append(q)
                added += 1

        total_removed += removed
        total_added += added
        for i, q in enumerate(out, 1):
            q["n"] = i
        json.dump(out, open(path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        parts = []
        if removed:
            parts.append("-%d дубл." % removed)
        if added:
            parts.append("+%d дод." % added)
        flag = ("  (" + ", ".join(parts) + ")") if parts else ""
        print("  ", fn.ljust(24), "%3d питань%s" % (len(out), flag))
    print("   прибрано дублікатів:", total_removed, "| додано унікальних:", total_added)


def main():
    for script, desc in PIPELINE:
        path = os.path.join(HERE, script)
        print(">>", script.ljust(15), desc)
        r = subprocess.run([sys.executable, path], cwd=ROOT)
        if r.returncode != 0:
            print("ERROR:", script, "повернув код", r.returncode)
            sys.exit(r.returncode)
    print("\n-- дедуплікація між варіантами --")
    dedupe()
    print("\nOK: банки питань відтворено й очищено від дублікатів. Далі: python build.py")


if __name__ == "__main__":
    main()
