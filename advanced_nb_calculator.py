# -*- coding: utf-8 -*-
"""
고급 n/b 비트 계산 시스템
JavaScript bitCalculation.v.0.2.js를 Python으로 변환
"""

import math
from typing import List, Dict, Tuple, Any
from collections import Counter

# 전역 변수
SUPER_BIT = 0.0


def initialize_arrays(count: int) -> Dict[str, List[float]]:
    """주어진 배열들을 초기화하는 함수"""
    arrays = ['BIT_START_A50', 'BIT_START_A100', 'BIT_START_B50', 'BIT_START_B100', 'BIT_START_NBA100']
    initialized_arrays = {}
    for array in arrays:
        initialized_arrays[array] = [0.0] * count
    return initialized_arrays


def calculate_bit(nb: List[float], bit: float = 5.5, reverse: bool = False) -> float:
    """N/B 값을 계산하는 함수 (가중치 상한치 및 하한치 기준)"""
    if len(nb) < 2:
        return bit / 100

    BIT_NB = bit
    max_val = max(nb)
    min_val = min(nb)
    COUNT = 150
    range_val = max_val - min_val

    # 음수와 양수 범위를 구별하여 증감 계산
    negative_range = abs(min_val) if min_val < 0 else 0
    positive_range = max_val if max_val > 0 else 0

    negative_increment = negative_range / (COUNT * len(nb) - 1) if (COUNT * len(nb) - 1) > 0 else 0
    positive_increment = positive_range / (COUNT * len(nb) - 1) if (COUNT * len(nb) - 1) > 0 else 0

    arrays = initialize_arrays(COUNT * len(nb))
    count = 0
    total_sum = 0

    for value in nb:
        for i in range(COUNT):
            BIT_END = 1

            # 부호에 따른 A50, B50 계산
            if value < 0:
                A50 = min_val + negative_increment * (count + 1)
            else:
                A50 = min_val + positive_increment * (count + 1)

            A100 = (count + 1) * BIT_NB / (COUNT * len(nb))

            if value < 0:
                B50 = A50 - negative_increment * 2
                B100 = A50 + negative_increment
            else:
                B50 = A50 - positive_increment * 2
                B100 = A50 + positive_increment

            NBA100 = A100 / (len(nb) - BIT_END) if (len(nb) - BIT_END) > 0 else 0

            arrays['BIT_START_A50'][count] = A50
            arrays['BIT_START_A100'][count] = A100
            arrays['BIT_START_B50'][count] = B50
            arrays['BIT_START_B100'][count] = B100
            arrays['BIT_START_NBA100'][count] = NBA100
            count += 1
        total_sum += value

    # Reverse 옵션 처리 (시간 역방향 분석)
    if reverse:
        arrays['BIT_START_NBA100'].reverse()

    # NB50 계산 (시간 순방향 기준 가중치 분석)
    NB50 = 0
    for value in nb:
        for a in range(len(arrays['BIT_START_NBA100'])):
            if arrays['BIT_START_B50'][a] <= value <= arrays['BIT_START_B100'][a]:
                idx = min(a, len(arrays['BIT_START_NBA100']) - 1)
                NB50 += arrays['BIT_START_NBA100'][idx]
                break

    # 시간 순방향의 상한치(MAX)와 하한치(MIN) 보정
    if len(nb) == 2:
        return bit - NB50  # NB 분석 인수가 양쪽뿐이면 시간 순방향 안정성이 높음

    return NB50


def update_super_bit(new_value: float):
    """SUPER_BIT 글로벌 변수 업데이트 함수"""
    global SUPER_BIT
    SUPER_BIT = new_value


def BIT_MAX_NB(nb: List[float], bit: float = 5.5) -> float:
    """시간 순방향 상한치 분석"""
    result = calculate_bit(nb, bit, False)  # 시간 정방향 분석

    # 결과 값이 유효 범위를 벗어나면 SUPER_BIT 반환
    if not math.isfinite(result) or math.isnan(result) or result > 100 or result < -100:
        return SUPER_BIT
    else:
        update_super_bit(result)
        return result


def BIT_MIN_NB(nb: List[float], bit: float = 5.5) -> float:
    """시간 순방향 하한치 분석"""
    result = calculate_bit(nb, bit, True)  # 시간 역방향 분석

    # 결과 값이 유효 범위를 벗어나면 SUPER_BIT 반환
    if not math.isfinite(result) or math.isnan(result) or result > 100 or result < -100:
        return SUPER_BIT
    else:
        update_super_bit(result)
        return result


def calculate_array_order_and_duplicate(nb1: List, nb2: List) -> Dict[str, float]:
    """두 배열을 비교하여 중복 인수와 순서를 측정하는 함수"""
    order_match = 0  # 순서가 일치하는 요소의 수
    max_order_match = 0  # 가장 긴 연속된 순서 일치 요소의 수
    duplicate_match = 0  # 중복값이 2번 이상인 경우의 일치하는 요소의 수

    length1 = len(nb1)
    length2 = len(nb2)

    # 중복 확인을 위한 카운터
    element_count1 = Counter(nb1)
    element_count2 = Counter(nb2)

    # 중복값이 2번 이상인 경우의 일치하는지 확인
    for key in element_count1:
        if key in element_count2 and element_count1[key] >= 1 and element_count2[key] >= 1:
            duplicate_match += min(element_count1[key], element_count2[key])

    # 두 배열의 순서 및 중복 비교
    for i in range(length1):
        for j in range(length2):
            if nb1[i] == nb2[j]:
                temp_match = 0
                x, y = i, j

                while x < length1 and y < length2 and nb1[x] == nb2[y]:
                    temp_match += 1
                    x += 1
                    y += 1

                if temp_match > max_order_match:
                    max_order_match = temp_match

    order_match = max_order_match

    # 순서 일치 비율 계산 (백분율)
    order_match_ratio = (order_match / min(length1, length2)) * 100 if min(length1, length2) > 0 else 0

    # 좌측과 우측의 중복 비율 계산
    duplicate_match_ratio_left = (duplicate_match / length1) * 100 if length1 > 0 else 0
    duplicate_match_ratio_right = (duplicate_match / length2) * 100 if length2 > 0 else 0

    # 중복 일치 비율 계산 (백분율): 좌측과 우측의 중복 비율의 평균
    duplicate_match_ratio = (duplicate_match_ratio_left + duplicate_match_ratio_right) / 2

    # 길이 비교 (두 배열의 길이 차이)
    if length2 < length1:
        length_difference = (length2 / length1) * 100 if length1 > 0 else 0
    else:
        length_difference = (length1 / length2) * 100 if length2 > 0 else 0

    # 최종 결과 반환
    return {
        'orderMatchRatio': order_match_ratio,
        'duplicateMatchRatio': duplicate_match_ratio,
        'duplicateMatchRatioLeft': duplicate_match_ratio_left,
        'duplicateMatchRatioRight': duplicate_match_ratio_right,
        'lengthDifference': length_difference
    }


def calculate_inclusion_from_base(sentence1: str, sentence2: str) -> Dict[str, Any]:
    """기준 문장(sentence1)의 단어들이 비교 문장(sentence2)에 얼마나 포함되어 있는지 계산"""
    if not sentence1 or not sentence2:
        return {'matched': 0, 'total': 0, 'ratio': 0.0, 'matchedWords': []}

    import re

    def clean(s):
        # 특수문자 제거, 공백 정리
        s = re.sub(r'[^\w가-힣\s]', '', s, flags=re.UNICODE)
        s = re.sub(r'\s+', ' ', s)
        return s.strip()

    base_words = clean(sentence1).split(' ')
    compare_words = clean(sentence2).split(' ')

    matched_words = []

    for word in base_words:
        if word in compare_words:
            matched_words.append(word)

    match_count = len(matched_words)
    ratio = (match_count / len(base_words)) * 100 if len(base_words) > 0 else 0

    return {
        'matched': match_count,
        'total': len(base_words),
        'ratio': round(ratio, 5),
        'matchedWords': matched_words
    }


def levenshtein(a: str, b: str) -> int:
    """Levenshtein 거리 계산 함수"""
    matrix = [[0] * (len(a) + 1) for _ in range(len(b) + 1)]

    for i in range(len(b) + 1):
        matrix[i][0] = i

    for j in range(len(a) + 1):
        matrix[0][j] = j

    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            if b[i - 1] == a[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(
                    matrix[i - 1][j - 1] + 1,  # 대체
                    matrix[i][j - 1] + 1,      # 삽입
                    matrix[i - 1][j] + 1       # 삭제
                )

    return matrix[len(b)][len(a)]


def calculate_levenshtein_similarity(nb1: List[str], nb2: List[str]) -> float:
    """Levenshtein 기반 유사도 계산 함수"""
    total_similarity = 0

    for i in range(len(nb1)):
        best_match = float('inf')

        for j in range(len(nb2)):
            distance = levenshtein(str(nb1[i]), str(nb2[j]))
            best_match = min(best_match, distance)

        max_length = max(len(str(nb1[i])), len(str(nb2[min(int(best_match), len(nb2) - 1)])) if len(nb2) > 0 else 1)
        similarity = ((max_length - best_match) / max_length) * 100 if max_length > 0 else 0
        total_similarity += similarity

    return total_similarity / len(nb1) if len(nb1) > 0 else 0


def soundex(s: str) -> str:
    """SOUNDEX 함수 (문자열을 발음 코드로 변환)"""
    if not isinstance(s, str):
        s = str(s)

    s = s.lower()
    if len(s) == 0:
        return "0000"

    a = list(s)
    f = a.pop(0)

    def get_code(c):
        if c in 'bfpv':
            return '1'
        elif c in 'cgjkqsxz':
            return '2'
        elif c in 'dt':
            return '3'
        elif c in 'l':
            return '4'
        elif c in 'mn':
            return '5'
        elif c in 'r':
            return '6'
        else:
            return ''

    r = []
    prev = ''
    for c in a:
        code = get_code(c)
        if code and code != prev:
            r.append(code)
            prev = code

    result = f + ''.join(r) + '000'
    return result[:4].upper()


def calculate_soundex_match(nb1: List, nb2: List) -> float:
    """SOUNDEX 기반 유사도 계산 함수"""
    soundex_match = 0

    for i in range(len(nb1)):
        for j in range(len(nb2)):
            if soundex(str(nb1[i])) == soundex(str(nb2[j])):
                soundex_match += 1

    soundex_match_ratio = (soundex_match / min(len(nb1), len(nb2))) * 100 if min(len(nb1), len(nb2)) > 0 else 0
    return soundex_match_ratio


def word_sim(nb_max: float = 100, nb_min: float = 50, max_val: float = 100, min_val: float = 50) -> float:
    """단어 유사도 계산"""
    if nb_max <= max_val:
        sim_max = (nb_max / max_val) * 100 if max_val != 0 else 0
    else:
        sim_max = (max_val / nb_max) * 100 if nb_max != 0 else 0

    sim_max = abs(sim_max)
    if sim_max > 100:
        sim_max = 100 - abs(sim_max)
    if nb_max == max_val:
        sim_max = 99.99

    if nb_min <= min_val:
        sim_min = (nb_min / min_val) * 100 if min_val != 0 else 0
    else:
        sim_min = (min_val / nb_min) * 100 if nb_min != 0 else 0

    sim_min = abs(sim_min)
    if sim_min > 100:
        sim_min = 100 - abs(sim_min)
    if nb_min == min_val:
        sim_min = 99.99

    similarity = (sim_max + sim_min) / 2
    return abs(similarity)


def word_sim2(nb_max: float = 100, max_val: float = 100) -> float:
    """단어 유사도 계산 2"""
    if nb_max <= max_val:
        sim_max = (nb_max / max_val) * 100 if max_val != 0 else 0
    else:
        sim_max = (max_val / nb_max) * 100 if nb_max != 0 else 0

    if nb_max == max_val:
        sim_max = 99.99

    return abs(sim_max)


def calculate_array_similarity(array1: List, array2: List) -> float:
    """배열 유사도 계산 (Jaccard + 순서 고려)"""
    # 기존 교집합/합집합 기반 유사도 계산
    intersection = [value for value in array1 if value in array2]
    union = list(set(array1 + array2))
    jaccard_similarity = (len(intersection) / len(union)) * 100 if len(union) > 0 else 0

    # 순서를 고려한 유사도 계산
    ordered_matches = [array1[i] for i in range(min(len(array1), len(array2))) if i < len(array2) and array1[i] == array2[i]]
    ordered_similarity = 0
    if len(array1) > 0 and len(array1) == len(array2):
        ordered_similarity = (len(ordered_matches) / len(array1)) * 100

    # 두 유사도를 결합하여 최종 유사도 계산
    return (jaccard_similarity * 0.5) + (ordered_similarity * 0.5)


def word_nb_unicode_format(domain: str) -> List[int]:
    """유니코드 기반 언어별 prefix 적용"""
    default_prefix = '한 국 어 영 어 중 국 어 . 일 본 어'

    if not domain or len(domain) == 0:
        domain = default_prefix
    else:
        domain = default_prefix + ':' + domain

    chars = list(domain)

    lang_ranges = [
        {'range': (0xAC00, 0xD7AF), 'prefix': 1000000},  # Korean
        {'range': (0x3040, 0x309F), 'prefix': 2000000},  # Japanese Hiragana
        {'range': (0x30A0, 0x30FF), 'prefix': 3000000},  # Japanese Katakana
        {'range': (0x4E00, 0x9FFF), 'prefix': 4000000},  # Chinese
        {'range': (0x0410, 0x044F), 'prefix': 5000000},  # Russian
        {'range': (0x0041, 0x007A), 'prefix': 6000000},  # English (basic Latin)
        {'range': (0x0590, 0x05FF), 'prefix': 7000000},  # Hebrew
        {'range': (0x00C0, 0x00FD), 'prefix': 8000000},  # Vietnamese
        {'range': (0x0E00, 0x0E7F), 'prefix': 9000000},  # Thai
    ]

    result = []
    for char in chars:
        unicode_value = ord(char)
        prefix = 0

        for lang in lang_ranges:
            if lang['range'][0] <= unicode_value <= lang['range'][1]:
                prefix = lang['prefix']
                break

        result.append(prefix + unicode_value)

    return result


def identify_language(text: str) -> str:
    """텍스트의 언어 식별"""
    if not text:
        return 'None'

    language_counts = {
        'Japanese': 0,
        'Korean': 0,
        'English': 0,
        'Russian': 0,
        'Chinese': 0,
        'Hebrew': 0,
        'Vietnamese': 0,
        'Thai': 0,
        'Portuguese': 0,
        'Others': 0,
    }

    portuguese_chars = {
        0x00C0, 0x00C1, 0x00C2, 0x00C3, 0x00C7, 0x00C8, 0x00C9, 0x00CA, 0x00CB, 0x00CC, 0x00CD, 0x00CE,
        0x00CF, 0x00D2, 0x00D3, 0x00D4, 0x00D5, 0x00D9, 0x00DA, 0x00DB, 0x00DC, 0x00DD, 0x00E0, 0x00E1,
        0x00E2, 0x00E3, 0x00E7, 0x00E8, 0x00E9, 0x00EA, 0x00EB, 0x00EC, 0x00ED, 0x00EE, 0x00EF, 0x00F2,
        0x00F3, 0x00F4, 0x00F5, 0x00F9, 0x00FA, 0x00FB, 0x00FC, 0x00FD,
    }

    for char in text:
        unicode_value = ord(char)

        if unicode_value in portuguese_chars:
            language_counts['Portuguese'] += 1
            language_counts['Portuguese'] *= 10
        elif 0xAC00 <= unicode_value <= 0xD7AF:
            language_counts['Korean'] += 1
            language_counts['Korean'] *= 100
        elif (0x3040 <= unicode_value <= 0x309F) or (0x30A0 <= unicode_value <= 0x30FF):
            language_counts['Japanese'] += 1
            language_counts['Japanese'] *= 10
        elif 0x4E00 <= unicode_value <= 0x9FFF:
            language_counts['Chinese'] += 1
        elif (0x0041 <= unicode_value <= 0x005A) or (0x0061 <= unicode_value <= 0x007A):
            language_counts['English'] += 1
        elif (0x00C0 <= unicode_value <= 0x00FF) or (0x0102 <= unicode_value <= 0x01B0):
            language_counts['Vietnamese'] += 1
            language_counts['Vietnamese'] *= 10
        elif 0x0410 <= unicode_value <= 0x044F:
            language_counts['Russian'] += 1
            language_counts['Russian'] *= 10
        elif 0x0590 <= unicode_value <= 0x05FF:
            language_counts['Hebrew'] += 1
            language_counts['Hebrew'] *= 10
        elif 0x0E00 <= unicode_value <= 0x0E7F:
            language_counts['Thai'] += 1
            language_counts['Thai'] *= 10
        else:
            language_counts['Others'] += 1

    total_characters = sum(language_counts.values())
    if total_characters == 0:
        return 'None'

    language_ratios = {k: v / total_characters for k, v in language_counts.items()}
    sorted_languages = sorted(language_ratios.items(), key=lambda x: x[1], reverse=True)

    identified_language = sorted_languages[0][0]
    max_ratio = sorted_languages[0][1]

    if identified_language == 'Others' or max_ratio == 0:
        if len(sorted_languages) > 1:
            second_language = sorted_languages[1][0]
            second_ratio = sorted_languages[1][1]
            return 'None' if second_ratio == 0 else second_language
        else:
            return 'None'

    return identified_language


def are_languages_same(str1: str, str2: str) -> bool:
    """두 문자열의 언어가 같은지 확인"""
    return identify_language(str1) == identify_language(str2)


def calculate_similarity(word1: str, word2: str) -> float:
    """전체 유사도 계산"""
    stage_level = 1

    arrs1 = word_nb_unicode_format(word1)
    nb_max = BIT_MAX_NB(arrs1)
    nb_min = BIT_MIN_NB(arrs1)

    arrs2 = word_nb_unicode_format(word2)
    max_val = BIT_MAX_NB(arrs2)
    min_val = BIT_MIN_NB(arrs2)

    similarity1 = word_sim(nb_max, nb_min, max_val, min_val)
    similarity2 = calculate_array_similarity(arrs1, arrs2)

    if are_languages_same(word1, word2):
        return max(similarity1, similarity2) * stage_level
    else:
        return min(similarity1, similarity2) / stage_level


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """코사인 유사도 계산"""
    if len(vec1) != len(vec2):
        # 길이가 다르면 짧은 쪽에 맞춰서 계산
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)
