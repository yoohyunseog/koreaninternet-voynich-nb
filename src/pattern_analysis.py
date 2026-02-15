# -*- coding: utf-8 -*-
"""
보이니치 패턴 분석 - 진짜 반복 구조 찾기
착시 번역이 아닌 실제 패턴 검증
"""

import re
from collections import Counter, defaultdict
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
    """최적 매칭 찾기"""
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

print("=" * 80)
print("보이니치 패턴 분석 - 반복 구조와 일관성 검증")
print("=" * 80)
print()

# 파일 읽기
with (DATA_DIR / 'voynich.nowhitespace.txt').open('r', encoding='utf-8') as f:
    full_text = f.read()

words = split_voynich_text(full_text)
english_words = LANGUAGE_DATABASE['영어']

print(f"총 보이니치 단어: {len(words)}개")
print(f"고유 보이니치 단어: {len(set(words))}개")
print(f"영어 후보 단어: {len(english_words)}개")
print()

# 1단계: 보이니치 단어 → 영어 후보 매핑
print("=" * 80)
print("1단계: 일관성 검증 - 같은 보이니치 단어가 항상 같은 번역으로 가는가?")
print("=" * 80)

voynich_to_english = defaultdict(list)  # {보이니치: [(영어, 유사도, 위치)...]}
english_to_voynich = defaultdict(list)  # {영어: [(보이니치, 유사도, 위치)...]}

for idx, vword in enumerate(words[:1000], 1):  # 처음 1000개 분석
    match = find_best_match(vword, english_words)
    if match:
        eng_word, score = match
        if score > 25:  # 최소 25% 유사도
            voynich_to_english[vword].append((eng_word, score, idx))
            english_to_voynich[eng_word].append((vword, score, idx))

# A. 같은 보이니치 단어가 여러 영어 단어로 매칭되는 경우 (충돌)
print("\n[A] 일관성 부족 - 하나의 보이니치 단어 → 여러 영어 번역:")
print("-" * 80)

inconsistent = []
for vword, matches in voynich_to_english.items():
    if len(matches) > 1:
        unique_english = set(m[0] for m in matches)
        if len(unique_english) > 1:
            inconsistent.append((vword, matches, len(unique_english)))

inconsistent.sort(key=lambda x: x[2], reverse=True)

for vword, matches, unique_count in inconsistent[:10]:
    print(f"\n보이니치: '{vword}' ({len(matches)}번 출현, {unique_count}개 다른 번역)")
    eng_counter = Counter(m[0] for m in matches)
    for eng, count in eng_counter.most_common(3):
        percentage = (count / len(matches)) * 100
        print(f"  → {eng}: {count}회 ({percentage:.1f}%)")

# B. 같은 영어 단어가 여러 보이니치 단어에서 매칭되는 경우
print("\n\n[B] 과적합 의심 - 하나의 영어 단어 → 여러 보이니치 단어:")
print("-" * 80)

overmatched = []
for eng, matches in english_to_voynich.items():
    if len(matches) > 1:
        unique_voynich = set(m[0] for m in matches)
        if len(unique_voynich) > 3:  # 3개 이상 다른 보이니치 단어
            overmatched.append((eng, matches, len(unique_voynich)))

overmatched.sort(key=lambda x: x[2], reverse=True)

for eng, matches, unique_count in overmatched[:10]:
    print(f"\n영어: '{eng}' ({len(matches)}번 매칭, {unique_count}개 다른 보이니치 단어)")
    voynich_counter = Counter(m[0] for m in matches)
    for vword, count in voynich_counter.most_common(3):
        print(f"  ← {vword}: {count}회")

# 2단계: 반복되는 보이니치 단어 패턴
print("\n\n" + "=" * 80)
print("2단계: 반복 패턴 - 빈도수 높은 보이니치 단어들")
print("=" * 80)

word_freq = Counter(words[:1000])
print("\n상위 20개 반복 단어:")
print("-" * 80)
print(f"{'순위':<6} {'보이니치 단어':<30} {'빈도':<8} {'주요 번역 후보'}")
print("-" * 80)

for rank, (vword, count) in enumerate(word_freq.most_common(20), 1):
    if vword in voynich_to_english:
        matches = voynich_to_english[vword]
        eng_counter = Counter(m[0] for m in matches)
        top_eng = eng_counter.most_common(1)[0][0] if eng_counter else "없음"
    else:
        top_eng = "매칭 실패"
    
    print(f"{rank:<6} {vword:<30} {count:<8} {top_eng}")

# 3단계: 보이니치 토큰 후보 추출 (부분 문자열 패턴)
print("\n\n" + "=" * 80)
print("3단계: 공통 토큰 패턴 - 반복되는 짧은 구조")
print("=" * 80)

def extract_ngrams(word, n=2):
    """n-gram 추출"""
    if len(word) < n:
        return []
    return [word[i:i+n] for i in range(len(word) - n + 1)]

# 2-gram, 3-gram 빈도 분석
bigrams = []
trigrams = []

for word in words[:1000]:
    bigrams.extend(extract_ngrams(word, 2))
    trigrams.extend(extract_ngrams(word, 3))

bigram_freq = Counter(bigrams)
trigram_freq = Counter(trigrams)

print("\n가장 빈번한 2-gram 토큰 (20개):")
print("-" * 40)
for token, count in bigram_freq.most_common(20):
    print(f"'{token}': {count}회")

print("\n가장 빈번한 3-gram 토큰 (20개):")
print("-" * 40)
for token, count in trigram_freq.most_common(20):
    print(f"'{token}': {count}회")

# 4단계: 신뢰도 높은 매칭만 추출
print("\n\n" + "=" * 80)
print("4단계: 고신뢰도 매칭 - 일관성과 빈도가 높은 번역")
print("=" * 80)

reliable_translations = []

for vword, matches in voynich_to_english.items():
    if len(matches) >= 3:  # 최소 3번 이상 출현
        eng_counter = Counter(m[0] for m in matches)
        top_eng, top_count = eng_counter.most_common(1)[0]
        
        consistency = top_count / len(matches)  # 일관성 비율
        
        if consistency >= 0.7:  # 70% 이상 같은 번역
            avg_score = sum(m[1] for m in matches if m[0] == top_eng) / top_count
            reliable_translations.append({
                'voynich': vword,
                'english': top_eng,
                'frequency': len(matches),
                'consistency': consistency,
                'avg_similarity': avg_score
            })

reliable_translations.sort(key=lambda x: (x['consistency'], x['frequency']), reverse=True)

print("\n신뢰도 높은 번역 (상위 30개):")
print("-" * 80)
print(f"{'보이니치':<25} {'영어':<15} {'빈도':<6} {'일관성':<8} {'평균 유사도'}")
print("-" * 80)

for trans in reliable_translations[:30]:
    print(f"{trans['voynich']:<25} {trans['english']:<15} "
          f"{trans['frequency']:<6} {trans['consistency']*100:>5.1f}%  "
          f"{trans['avg_similarity']:>6.1f}%")

print("\n\n" + "=" * 80)
print("분석 완료!")
print("=" * 80)
print(f"\n총 분석 단어: 1000개")
print(f"고유 보이니치 단어: {len(voynich_to_english)}개")
print(f"매칭된 영어 단어: {len(english_to_voynich)}개")
print(f"고신뢰도 번역: {len(reliable_translations)}개")
print(f"반복 토큰(2-gram): {len(bigram_freq)}개")
print(f"반복 토큰(3-gram): {len(trigram_freq)}개")
