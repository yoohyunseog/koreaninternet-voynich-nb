# -*- coding: utf-8 -*-
"""\
Build an English sentence by matching Voynich n/b metrics to English n/b metrics.

Example:
    python src/english_sentence_from_nb_json.py \
        --voynich outputs/voynich_nb_words.json \
        --english outputs/english_nb_words.json \
        --output outputs/voynich_to_english_sentence.txt \
        --limit 50
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_json(path: str) -> Dict:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = ROOT_DIR / file_path
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def score_pair(v_item: Dict[str, object], e_item: Dict[str, object]) -> float:
    # Smaller is better: sum of abs diffs for nb_max/nb_min.
    return abs(v_item["nb_max"] - e_item["nb_max"]) + abs(v_item["nb_min"] - e_item["nb_min"])


def match_words(v_words: List[Dict[str, object]], e_words: List[Dict[str, object]], limit: int) -> List[Tuple[str, str, float]]:
    results: List[Tuple[str, str, float]] = []
    used_words = deque(maxlen=5)  # Track last 5 used words to avoid repetition

    for v_item in v_words[:limit]:
        best_score = None
        best_word = None
        best_idx = None
        
        for idx, e_item in enumerate(e_words):
            # Skip nightingale
            if e_item["word"].lower() == "nightingale":
                continue
                
            score = score_pair(v_item, e_item)
            
            # Penalize recently used words (within last 5 matches)
            if e_item["word"] in used_words:
                score += 0.5  # Add penalty to encourage diversity
            
            if best_score is None or score < best_score:
                best_score = score
                best_word = e_item["word"]
                best_idx = idx
        
        results.append((v_item["word"], str(best_word), float(best_score)))
        
        # Track used words (automatic maxlen=5 enforcement)
        used_words.append(best_word)
    
    return results


def translate_word_gpt(word: str, model: str, api_key: str) -> str:
    """Translate a single word to Korean"""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Translate this English word to Korean. Reply with only the Korean word."},
            {"role": "user", "content": word},
        ],
        "temperature": 0.2,
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            if "choices" in parsed and parsed["choices"]:
                return parsed["choices"][0]["message"]["content"].strip()
            return word
    except Exception:
        return word


def translate_sentence_gpt(sentence: str, model: str) -> str:
    """Translate a sentence by translating individual words and combining them"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[skipped: missing OPENAI_API_KEY]"

    words = sentence.split()
    # Translate only unique words to save API calls
    unique_words = list(dict.fromkeys(words))
    
    word_translations = {}
    for word in unique_words:
        korean = translate_word_gpt(word, model, api_key)
        word_translations[word] = korean

    # Build final translation using the translated words
    translated_words = [word_translations.get(w, w) for w in words]
    return " ".join(translated_words)


def main() -> int:
    parser = argparse.ArgumentParser(description="Match Voynich n/b to English n/b and build a sentence")
    parser.add_argument("--voynich", default="outputs/voynich_nb_words.json", help="Voynich n/b JSON path")
    parser.add_argument("--english", default="outputs/english_nb_words.json", help="English n/b JSON path")
    parser.add_argument("--output", default="outputs/voynich_to_english_sentence.txt", help="Output text path")
    parser.add_argument("--limit", type=int, default=100, help="Number of Voynich words to map")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model for translation")
    args = parser.parse_args()

    v_data = load_json(args.voynich)
    e_data = load_json(args.english)

    v_words = v_data.get("words", [])
    e_words = e_data.get("words", [])

    if not v_words or not e_words:
        raise SystemExit("No words found in one or both JSON files.")

    matches = match_words(v_words, e_words, args.limit)
    sentence = " ".join(match[1] for match in matches)
    translation = translate_sentence_gpt(sentence, args.model)

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT_DIR / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("# Voynich to English (n/b match)\n")
        handle.write(f"Count: {len(matches)}\n")
        handle.write("\n")
        handle.write("Sentence:\n")
        handle.write(sentence + "\n\n")
        handle.write("GPT Translation (Korean):\n")
        handle.write(translation + "\n\n")
        handle.write("Details:\n")
        for v_word, e_word, score in matches:
            handle.write(f"{v_word}\t{e_word}\t{score:.6f}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
