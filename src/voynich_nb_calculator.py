# -*- coding: utf-8 -*-
"""
Voynich n/b calculator (CLI)

Examples:
    python src/voynich_nb_calculator.py --text "qokedy qokeedy"
    python src/voynich_nb_calculator.py --file data/voynich.nowhitespace.txt --limit 50
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List

from advanced_nb_calculator import BIT_MAX_NB, BIT_MIN_NB, word_nb_unicode_format

ROOT_DIR = Path(__file__).resolve().parents[1]


def iter_words_from_text(text: str) -> List[str]:
    return [w for w in text.split() if w]


def read_text_from_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = ROOT_DIR / file_path

    with file_path.open("r", encoding="utf-8") as handle:
        return handle.read()


def calculate_word_metrics(word: str) -> dict:
    nb_codes = word_nb_unicode_format(word)
    nb_max = BIT_MAX_NB(nb_codes)
    nb_min = BIT_MIN_NB(nb_codes)
    return {
        "word": word,
        "length": len(word),
        "nb_max": nb_max,
        "nb_min": nb_min,
        "nb_codes": nb_codes,
    }


def print_metrics(metrics: Iterable[dict], show_codes: bool, limit: int | None) -> None:
    print("word\tlen\tNB_MAX\tNB_MIN")
    count = 0
    for item in metrics:
        if limit is not None and count >= limit:
            break
        line = f"{item['word']}\t{item['length']}\t{item['nb_max']:.6f}\t{item['nb_min']:.6f}"
        print(line)
        if show_codes:
            print("  codes:", item["nb_codes"])
        count += 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Voynich n/b calculator")
    parser.add_argument("--text", help="Input text (space-separated words)")
    parser.add_argument("--file", help="Path to a text file")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of words to print")
    parser.add_argument("--show-codes", action="store_true", help="Print n/b code arrays")

    args = parser.parse_args()

    if not args.text and not args.file:
        try:
            args.text = input("Enter text: ").strip()
        except EOFError:
            return 1

    if args.file:
        try:
            text = read_text_from_file(args.file)
        except OSError as exc:
            print(f"Failed to read file: {exc}", file=sys.stderr)
            return 1
    else:
        text = args.text or ""

    words = iter_words_from_text(text)
    if not words:
        print("No words found.", file=sys.stderr)
        return 1

    metrics = (calculate_word_metrics(word) for word in words)
    print_metrics(metrics, args.show_codes, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
