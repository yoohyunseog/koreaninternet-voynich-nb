# -*- coding: utf-8 -*-
"""
보이니치 번역 순서 보기 - 처음 200개 단어
"""

import re
from pathlib import Path

from advanced_nb_calculator import levenshtein
from language_database import LANGUAGE_DATABASE

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

def split_voynich_text(text):
    """보이니치 텍스트를 단어로 분리"""
    words = re.findall(r'[^,!?\.\;\:\s]+', text)
    words = [w.strip() for w in words if w.strip() and len(w.strip()) >= 2]
    return words

def find_best_match(voynich_word, word_list):
    """최적의 영어 단어 찾기"""
    best_match = None
    best_score = 0
    
    for word in word_list:
        len_diff = abs(len(voynich_word) - len(word))
        if len_diff > len(voynich_word) * 0.6:
            continue
        
        distance = levenshtein(voynich_word.lower(), word.lower())
        max_len = max(len(voynich_word), len(word))
        similarity = (1 - distance / max_len) * 100
        
        if similarity > best_score:
            best_score = similarity
            best_match = (word, similarity)
    
    return best_match

print("보이니치 번역 순서 (처음 200개 단어)")
print("=" * 80)

# 파일 읽기
with (DATA_DIR / 'voynich.nowhitespace.txt').open('r', encoding='utf-8') as f:
    full_text = f.read()

words = split_voynich_text(full_text)[:200]
english_words = LANGUAGE_DATABASE['영어']

print(f"\n{'번호':<6} {'보이니치 단어':<40} {'번역':<20} {'유사도'}")
print("-" * 80)

for idx, vword in enumerate(words, 1):
    match = find_best_match(vword, english_words)
    
    if match:
        translated, score = match
        if score > 20:
            print(f"{idx:<6} {vword:<40} {translated:<20} {score:.1f}%")
        else:
            print(f"{idx:<6} {vword:<40} [매칭 실패]")
    else:
        print(f"{idx:<6} {vword:<40} [매칭 실패]")

print("\n" + "=" * 80)
print("처음 200개 단어 번역 완료")
