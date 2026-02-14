# -*- coding: utf-8 -*-
"""
보이니치 문서 전체 번역 - 영어 단어만 사용
"""

import re
from advanced_nb_calculator import levenshtein
from language_database import LANGUAGE_DATABASE

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
        # 길이 차이가 너무 크면 스킵
        len_diff = abs(len(voynich_word) - len(word))
        if len_diff > len(voynich_word) * 0.6:
            continue
        
        # 레벤슈타인 거리 계산
        distance = levenshtein(voynich_word.lower(), word.lower())
        max_len = max(len(voynich_word), len(word))
        similarity = (1 - distance / max_len) * 100
        
        if similarity > best_score:
            best_score = similarity
            best_match = word
    
    return best_match, best_score

# 메인 실행
print("=" * 80)
print("보이니치 문서 전체 번역 (영어 단어만)")
print("=" * 80)
print()

# 파일 읽기
print("파일 읽기: voynich.nowhitespace.txt")
with open('voynich.nowhitespace.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# 단어 분리
print("단어 분리 중...")
words = split_voynich_text(full_text)
print(f"총 {len(words)}개 단어 발견")
print()

# 영어 단어 목록
english_words = LANGUAGE_DATABASE['영어']
print(f"영어 단어 데이터베이스: {len(english_words)}개 단어")
print()

# 번역
print("번역 시작... (시간이 걸릴 수 있습니다)")
print()

translated = []
total = len(words)

for idx, vword in enumerate(words, 1):
    if idx % 100 == 0:
        percentage = (idx / total) * 100
        print(f"진행: {idx}/{total} ({percentage:.1f}%)")
    
    # 매칭
    match_word, score = find_best_match(vword, english_words)
    
    if match_word and score > 20:  # 최소 20% 유사도
        translated.append(match_word)
    else:
        translated.append(f"[{vword}]")

print()
print("번역 완료!")
print()

# 결과 저장
output_file = 'voynich_full_translation_english_only.txt'
print(f"결과 저장: {output_file}")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("보이니치 문서 전체 번역 (영어 단어만)\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"총 단어 수: {len(words)}\n")
    f.write(f"영어 단어 DB: {len(english_words)}개\n")
    f.write("\n")
    
    f.write("=" * 80 + "\n")
    f.write("번역 텍스트:\n")
    f.write("=" * 80 + "\n\n")
    
    # 한줄로 출력
    f.write(" ".join(translated))
    f.write("\n\n")
    
    # 문단별로 출력 (50단어씩)
    f.write("=" * 80 + "\n")
    f.write("문단별 번역 (50단어씩):\n")
    f.write("=" * 80 + "\n\n")
    
    for i in range(0, len(translated), 50):
        chunk = translated[i:i+50]
        f.write(f"[{i+1}~{i+len(chunk)}]\n")
        f.write(" ".join(chunk))
        f.write("\n\n")

print()
print("=" * 80)
print("미리보기 (처음 100단어):")
print("=" * 80)
print(" ".join(translated[:100]))
print()
print("완료!")
