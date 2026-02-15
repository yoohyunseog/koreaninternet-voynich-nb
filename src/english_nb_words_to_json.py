# -*- coding: utf-8 -*-
"""\
Generate n/b metrics for English words and save to JSON.

Example:
    python src/english_nb_words_to_json.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from advanced_nb_calculator import BIT_MAX_NB, BIT_MIN_NB, word_nb_unicode_format
from language_database import LANGUAGE_DATABASE

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT_DIR / "outputs"


def calculate_nb(word: str) -> Dict[str, object]:
    nb_codes = word_nb_unicode_format(word)
    return {
        "word": word,
        "length": len(word),
        "nb_max": BIT_MAX_NB(nb_codes),
        "nb_min": BIT_MIN_NB(nb_codes),
        "nb_codes": nb_codes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="English n/b JSON generator")
    parser.add_argument(
        "--output",
        default=str(OUTPUTS_DIR / "english_nb_words.json"),
        help="Output JSON path",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit number of words")
    parser.add_argument("--no-codes", action="store_true", help="Omit nb_codes from output")
    args = parser.parse_args()

    words: List[str] = LANGUAGE_DATABASE.get("영어", [])
    if args.limit is not None:
        words = words[: args.limit]

    results = []
    for word in words:
        item = calculate_nb(word)
        if args.no_codes:
            item.pop("nb_codes", None)
        results.append(item)

    payload = {
        "language": "영어",
        "count": len(results),
        "words": results,
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT_DIR / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
