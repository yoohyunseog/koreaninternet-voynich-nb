# -*- coding: utf-8 -*-
"""
보이니치 문서 빠른 분석기
간단한 매칭으로 빠르게 분석
"""

import re
from advanced_nb_calculator import (
    BIT_MAX_NB, BIT_MIN_NB,
    word_nb_unicode_format,
    cosine_similarity,
    levenshtein
)
from language_database import LANGUAGE_DATABASE

def split_voynich_text(text):
    """보이니치 텍스트를 단어로 분리"""
    words = re.findall(r'[^,!?\.\;\:\s]+|[,!?\.\;\:]', text)
    words = [w.strip() for w in words if w.strip() and len(w.strip()) >= 2]
    return words

def simple_match_word(voynich_word):
    """
    간단한 매칭 (빠른 버전)
    - 길이 유사성
    - 레벤슈타인 거리
    """
    best_match = None
    best_score = 0
    
    for language, words in LANGUAGE_DATABASE.items():
        for word in words:
            # 길이 차이가 너무 크면 스킵
            len_diff = abs(len(voynich_word) - len(word))
            if len_diff > len(voynich_word) * 0.5:
                continue
            
            # 레벤슈타인 거리 계산
            distance = levenshtein(voynich_word.lower(), word.lower())
            max_len = max(len(voynich_word), len(word))
            similarity = (1 - distance / max_len) * 100
            
            if similarity > best_score:
                best_score = similarity
                best_match = {
                    'word': word,
                    'language': language,
                    'similarity': similarity
                }
    
    return best_match

def quick_analyze(filepath, output_file='voynich_quick_translation.txt', max_words=100):
    """빠른 분석"""
    print("=" * 80)
    print("보이니치 문서 빠른 분석")
    print("=" * 80)
    print()
    
    # 파일 읽기
    print(f"파일 읽기: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # 단어 분리
    words = split_voynich_text(full_text)
    total_words = len(words)
    
    if max_words:
        words = words[:max_words]
    
    print(f"총 {total_words}개 단어 중 {len(words)}개 분석")
    print()
    
    # 분석
    results = []
    translated = []
    
    print("번역 중...")
    for idx, vword in enumerate(words, 1):
        if idx % 10 == 0:
            print(f"  {idx}/{len(words)}...")
        
        # 구두점
        if vword in [',', '.', '!', '?', ';', ':']:
            results.append(f"{idx}. {vword} -> {vword}")
            translated.append(vword)
            continue
        
        # 매칭
        match = simple_match_word(vword)
        
        if match:
            word = match['word']
            lang = match['language']
            sim = match['similarity']
            results.append(f"{idx}. {vword} -> {word} ({lang}, {sim:.1f}%)")
            translated.append(word)
        else:
            results.append(f"{idx}. {vword} -> [?]")
            translated.append(f"[{vword}]")
    
    print("\n완료!")
    print()
    
    # 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("보이니치 문서 빠른 번역\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("번역 텍스트:\n")
        f.write("-" * 80 + "\n")
        f.write(" ".join(translated) + "\n\n")
        
        f.write("상세 결과:\n")
        f.write("-" * 80 + "\n")
        for result in results:
            f.write(result + "\n")
    
    print(f"결과 저장: {output_file}")
    
    # 미리보기
    print("\n" + "=" * 80)
    print("번역 미리보기 (처음 50단어):")
    print("=" * 80)
    print(" ".join(translated[:50]))
    print()
    
    return results, translated

if __name__ == "__main__":
    print("보이니치 빠른 분석기\n")
    
    # 옵션
    print("1. 초단기 테스트 (50단어)")
    print("2. 빠른 테스트 (200단어)")
    print("3. 중간 분석 (500단어)")
    print("4. 대량 분석 (1000단어)")
    print()
    
    choice = input("선택 (1-4): ").strip()
    
    options = {
        '1': (50, 'voynich_quick_50.txt'),
        '2': (200, 'voynich_quick_200.txt'),
        '3': (500, 'voynich_quick_500.txt'),
        '4': (1000, 'voynich_quick_1000.txt'),
    }
    
    if choice in options:
        max_w, output = options[choice]
        quick_analyze('voynich.nowhitespace.txt', output, max_w)
    else:
        print("기본값 (50단어) 실행")
        quick_analyze('voynich.nowhitespace.txt', 'voynich_quick_50.txt', 50)
