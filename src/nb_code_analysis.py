# -*- coding: utf-8 -*-
"""
보이니치 n/b 코드 변환 및 패턴 분석 (영어 매칭 없음)
순수 n/b 코드 기반 분석
"""

import re
from collections import Counter, defaultdict
from pathlib import Path

from advanced_nb_calculator import (
    word_nb_unicode_format,
    BIT_MAX_NB, BIT_MIN_NB,
    calculate_array_order_and_duplicate
)

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

class NBCodeAnalyzer:
    """n/b 코드 분석기"""
    
    def __init__(self):
        self.char_to_number = {}
        self.number_to_char = {}
        self.next_number = 1
        
    def assign_number(self, char):
        """문자에 번호 할당"""
        if char not in self.char_to_number:
            self.char_to_number[char] = self.next_number
            self.number_to_char[self.next_number] = char
            self.next_number += 1
        return self.char_to_number[char]
    
    def text_to_nb_codes(self, text):
        """텍스트를 n/b 코드로 변환"""
        codes = []
        for char in text:
            if char.strip():
                number = self.assign_number(char)
                binary = format(number, '08b')
                codes.append({
                    'char': char,
                    'number': number,
                    'binary': binary,
                    'bit_count': bin(number).count('1')
                })
        return codes
    
    def word_to_nb(self, word):
        """단어를 n/b 코드로 변환"""
        codes = []
        for char in word:
            number = self.assign_number(char)
            codes.append(number)
        return codes

def split_voynich_text(text):
    """보이니치 텍스트를 단어로 분리"""
    words = re.findall(r'[^,!?\.\;\:\s]+', text)
    words = [w.strip() for w in words if w.strip() and len(w.strip()) >= 2]
    return words

def analyze_nb_patterns(words, analyzer, max_words=1000):
    """n/b 코드 패턴 분석"""
    
    print("=" * 80)
    print("보이니치 n/b 코드 패턴 분석")
    print("=" * 80)
    print()
    
    # 단어별 n/b 코드 변환
    word_nb_codes = []
    for word in words[:max_words]:
        nb_codes = analyzer.word_to_nb(word)
        word_nb_codes.append({
            'word': word,
            'nb_codes': nb_codes,
            'length': len(nb_codes),
            'sum': sum(nb_codes),
            'avg': sum(nb_codes) / len(nb_codes) if nb_codes else 0
        })
    
    print(f"분석 대상: {len(word_nb_codes)}개 단어")
    print(f"고유 문자: {len(analyzer.char_to_number)}개")
    print()
    
    # 1. 단어 길이 분포
    print("=" * 80)
    print("1. 단어 길이 분포")
    print("=" * 80)
    
    length_dist = Counter(w['length'] for w in word_nb_codes)
    print("\n길이별 단어 수:")
    for length in sorted(length_dist.keys())[:20]:
        count = length_dist[length]
        bar = '█' * (count // 5)
        print(f"{length:3d}자: {count:4d}개 {bar}")
    
    # 2. 숫자 코드 빈도 분석
    print("\n" + "=" * 80)
    print("2. 숫자 코드 빈도 (상위 30개)")
    print("=" * 80)
    
    all_numbers = []
    for w in word_nb_codes:
        all_numbers.extend(w['nb_codes'])
    
    number_freq = Counter(all_numbers)
    print(f"\n총 숫자 코드: {len(all_numbers)}개")
    print(f"고유 숫자 코드: {len(number_freq)}개")
    print()
    print(f"{'순위':<6} {'문자':<8} {'숫자':<8} {'2진수':<12} {'비트수':<8} {'빈도'}")
    print("-" * 80)
    
    for rank, (num, count) in enumerate(number_freq.most_common(30), 1):
        char = analyzer.number_to_char[num]
        binary = format(num, '08b')
        bit_count = bin(num).count('1')
        percentage = (count / len(all_numbers)) * 100
        print(f"{rank:<6} '{char}'<6 {num:<8} {binary:<12} {bit_count:<8} {count:5d} ({percentage:5.2f}%)")
    
    # 3. 연속 패턴 분석
    print("\n" + "=" * 80)
    print("3. 연속 숫자 패턴 (2-gram)")
    print("=" * 80)
    
    bigrams = []
    for w in word_nb_codes:
        codes = w['nb_codes']
        for i in range(len(codes) - 1):
            bigrams.append((codes[i], codes[i+1]))
    
    bigram_freq = Counter(bigrams)
    print(f"\n총 2-gram: {len(bigrams)}개")
    print(f"고유 2-gram: {len(bigram_freq)}개")
    print()
    print(f"{'순위':<6} {'패턴 (문자)':<20} {'패턴 (숫자)':<20} {'빈도'}")
    print("-" * 80)
    
    for rank, (pattern, count) in enumerate(bigram_freq.most_common(30), 1):
        char1 = analyzer.number_to_char[pattern[0]]
        char2 = analyzer.number_to_char[pattern[1]]
        char_pattern = f"'{char1}{char2}'"
        num_pattern = f"{pattern[0]}-{pattern[1]}"
        percentage = (count / len(bigrams)) * 100
        print(f"{rank:<6} {char_pattern:<20} {num_pattern:<20} {count:4d} ({percentage:5.2f}%)")
    
    # 4. 반복 단어 분석
    print("\n" + "=" * 80)
    print("4. 반복 단어 패턴 (n/b 코드 동일)")
    print("=" * 80)
    
    word_freq = Counter(w['word'] for w in word_nb_codes)
    print("\n가장 자주 나타나는 단어 (상위 20개):")
    print("-" * 80)
    print(f"{'순위':<6} {'단어':<30} {'빈도':<6} {'n/b 코드'}")
    print("-" * 80)
    
    for rank, (word, count) in enumerate(word_freq.most_common(20), 1):
        # 해당 단어의 n/b 코드 찾기
        for w in word_nb_codes:
            if w['word'] == word:
                nb_str = '-'.join(map(str, w['nb_codes'][:10]))
                if len(w['nb_codes']) > 10:
                    nb_str += '...'
                break
        print(f"{rank:<6} {word:<30} {count:<6} {nb_str}")
    
    # 5. 숫자 합계와 평균 분포
    print("\n" + "=" * 80)
    print("5. 단어별 숫자 합계 분석")
    print("=" * 80)
    
    sums = [w['sum'] for w in word_nb_codes]
    avgs = [w['avg'] for w in word_nb_codes]
    
    print(f"\n숫자 합계 범위: {min(sums)} ~ {max(sums)}")
    print(f"평균 값 범위: {min(avgs):.2f} ~ {max(avgs):.2f}")
    print(f"전체 평균: {sum(avgs) / len(avgs):.2f}")
    
    # 6. BIT_MAX_NB와 BIT_MIN_NB 분석 (처음 50개 단어)
    print("\n" + "=" * 80)
    print("6. 고급 비트 분석 (처음 50개 단어)")
    print("=" * 80)
    
    print("\n단어별 BIT_MAX_NB / BIT_MIN_NB:")
    print("-" * 80)
    print(f"{'번호':<6} {'단어':<30} {'BIT_MAX':<12} {'BIT_MIN':<12}")
    print("-" * 80)
    
    for idx, w in enumerate(word_nb_codes[:50], 1):
        word = w['word']
        nb_codes = w['nb_codes']
        
        # unicode format으로 변환
        unicode_val = word_nb_unicode_format(word)
        
        # BIT 계산
        bit_max = BIT_MAX_NB(unicode_val)
        bit_min = BIT_MIN_NB(unicode_val)
        
        print(f"{idx:<6} {word:<30} {bit_max:<12.4f} {bit_min:<12.4f}")
    
    return word_nb_codes

# 메인 실행
if __name__ == "__main__":
    print("\n보이니치 n/b 코드 분석 시작\n")
    
    # 파일 읽기
    with (DATA_DIR / 'voynich.nowhitespace.txt').open('r', encoding='utf-8') as f:
        full_text = f.read()
    
    # 단어 분리
    words = split_voynich_text(full_text)
    print(f"총 단어 수: {len(words)}개\n")
    
    # 분석기 초기화
    analyzer = NBCodeAnalyzer()
    
    # 분석 실행
    results = analyze_nb_patterns(words, analyzer, max_words=1000)
    
    print("\n" + "=" * 80)
    print("분석 완료!")
    print("=" * 80)
