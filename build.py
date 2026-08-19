#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Word Family Rush / Familias de Palabras (bilingual).

Reads the compact word-family databases:
  - families.txt  -> English (B2–C1)
  - familias.txt  -> Spanish (B1–B2)
validates them, and injects BOTH as JSON into `index.template.html` to
produce the single, self-contained, double-clickable `index.html`.

In the game a single language switch flips the whole app (menu + database)
between English and Spanish.

Database format (one family per line, same for both languages):

    word;pos;gloss[;alt,alt] | word;pos;gloss[;alt,alt] | ...

  - The FIRST word on a line is the "seed" (the base word shown to the player).
  - pos codes:  n=noun  v=verb  adj=adjective  adv=adverb
      combine with "/" for a word that is two parts of speech, e.g.  n/v
      (part-of-speech names are written in the database's OWN language:
       n->noun/sustantivo, v->verb/verbo, adj->adjective/adjetivo, adv->adverb/adverbio)
  - gloss: a very short meaning in the target language (shown as a hint only
      when two words in the family share a part of speech, and in the review).
  - alt (optional 4th field): comma-separated accepted alternate spellings.
  - Lines starting with # and blank lines are ignored.

Just run:  python build.py
"""

import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "index.template.html"
OUT = HERE / "index.html"

# Per-language configuration. The part-of-speech names are localised so the
# whole game (data included) reads in the chosen language.
LANGS = {
    "en": {
        "name": "English",
        "src": "families.txt",
        "level": "B2–C1",
        "pos": {"n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb"},
    },
    "es": {
        "name": "Español",
        "src": "familias.txt",
        "level": "B1–B2",
        "pos": {"n": "sustantivo", "v": "verbo", "adj": "adjetivo", "adv": "adverbio"},
    },
}


def expand_pos(code: str, pos_map: dict) -> str:
    parts = [p.strip() for p in code.split("/") if p.strip()]
    out = []
    for p in parts:
        if p not in pos_map:
            raise ValueError(f"unknown part-of-speech code: {p!r}")
        out.append(pos_map[p])
    return " / ".join(out)


def parse(src: Path, pos_map: dict):
    if not src.exists():
        sys.exit(f"ERROR: {src.name} not found.")
    families = []
    warnings = []
    seen_seed = {}
    total_words = 0
    with src.open(encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            word_specs = [w.strip() for w in line.split("|") if w.strip()]
            words = []
            for ws in word_specs:
                fields = [f.strip() for f in ws.split(";")]
                if len(fields) < 2:
                    sys.exit(f"{src.name} line {lineno}: '{ws}' needs at least word;pos")
                w = fields[0]
                try:
                    pos = expand_pos(fields[1], pos_map)
                except ValueError as e:
                    sys.exit(f"{src.name} line {lineno}: {e}  (in '{ws}')")
                gloss = fields[2] if len(fields) >= 3 else ""
                entry = {"w": w, "pos": pos, "en": gloss}
                if len(fields) >= 4 and fields[3]:
                    entry["alt"] = [a.strip() for a in fields[3].split(",") if a.strip()]
                words.append(entry)
            # validation
            if not (3 <= len(words) <= 10):
                warnings.append(f"line {lineno}: family '{words[0]['w']}' has {len(words)} words (want 3–10)")
            seed = words[0]["w"].lower()
            if seed in seen_seed:
                warnings.append(f"line {lineno}: duplicate seed '{seed}' (also line {seen_seed[seed]})")
            else:
                seen_seed[seed] = lineno
            total_words += len(words)
            families.append({"words": words})
    return families, warnings, total_words


def main():
    all_data = {}
    report = {}
    for lang, cfg in LANGS.items():
        families, warnings, total_words = parse(HERE / cfg["src"], cfg["pos"])
        all_data[lang] = {
            "lang": lang,
            "name": cfg["name"],
            "level": cfg["level"],
            "count": len(families),
            "families": families,
        }
        report[lang] = (families, warnings, total_words)

    payload = json.dumps(all_data, ensure_ascii=False, separators=(",", ":"))

    template = TEMPLATE.read_text(encoding="utf-8")
    if "__FAMILY_DATA__" not in template:
        sys.exit("ERROR: placeholder __FAMILY_DATA__ missing from template.")
    html = template.replace("__FAMILY_DATA__", payload)
    OUT.write_text(html, encoding="utf-8")

    print(f"Built {OUT.name}")
    for lang, cfg in LANGS.items():
        families, warnings, total_words = report[lang]
        print(f"  [{lang}] {cfg['name']} ({cfg['level']}) — {cfg['src']}")
        print(f"       families : {len(families)}")
        print(f"       words    : {total_words}  (avg {total_words/max(len(families),1):.1f} per family)")
        if warnings:
            print(f"       warnings : {len(warnings)}")
            for w in warnings[:40]:
                print("         -", w)
            if len(warnings) > 40:
                print(f"         … and {len(warnings)-40} more")
        else:
            print("       warnings : none")


if __name__ == "__main__":
    main()
