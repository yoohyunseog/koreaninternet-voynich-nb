# -*- coding: utf-8 -*-
"""\
Split Voynich text into words and calculate n/b metrics to JSON.

Example:
    python src/voynich_nb_words_to_json.py --input data/voynich.nowhitespace.txt
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import List, Dict

from advanced_nb_calculator import BIT_MAX_NB, BIT_MIN_NB, word_nb_unicode_format

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT_DIR / "outputs"


def load_text(path: str) -> str:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = ROOT_DIR / file_path

    with file_path.open("r", encoding="utf-8") as handle:
        return handle.read()


def split_words(text: str) -> List[str]:
    # Use Unicode word characters (letters/digits/underscore) as tokens.
    return re.findall(r"\w+", text, flags=re.UNICODE)


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
    parser = argparse.ArgumentParser(description="Voynich word split + n/b JSON generator")
    parser.add_argument("--input", required=True, help="Path to Voynich text file")
    parser.add_argument(
        "--output",
        default=str(OUTPUTS_DIR / "voynich_nb_words.json"),
        help="Output JSON path",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit number of words")
    parser.add_argument("--no-codes", action="store_true", help="Omit nb_codes from output")
    args = parser.parse_args()

    text = load_text(args.input)
    words = split_words(text)
    if args.limit is not None:
        words = words[: args.limit]

    results = []
    for word in words:
        item = calculate_nb(word)
        if args.no_codes:
            item.pop("nb_codes", None)
        results.append(item)

    payload = {
        "source": args.input,
        "count": len(results),
        "words": results,
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT_DIR / output_path

    output_dir = os.path.dirname(str(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
