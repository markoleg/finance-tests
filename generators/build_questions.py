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
import subprocess, sys, os

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


def main():
    for script, desc in PIPELINE:
        path = os.path.join(HERE, script)
        print(">>", script.ljust(15), desc)
        r = subprocess.run([sys.executable, path], cwd=ROOT)
        if r.returncode != 0:
            print("ERROR:", script, "повернув код", r.returncode)
            sys.exit(r.returncode)
    print("\nOK: усі банки питань відтворено. Далі запусти: python build.py")


if __name__ == "__main__":
    main()
