# -*- coding: utf-8 -*-
"""
보이니치 문서 전체 분석기
voynich.nowhitespace.txt 파일을 읽어서 전체 텍스트를 분석합니다
"""

import re
from voynich_analyzer import LanguageMatcher, VoynichAnalyzer
from language_database import get_total_word_count, get_language_count, LANGUAGE_DATABASE

def split_voynich_text(text):
    """
    보이니치 텍스트를 단어로 분리
    , ! ? . ; : 등의 구두점으로 구분
    """
    # 구두점으로 분리하되, 구두점도 유지
    words = re.findall(r'[^,!?\.\;\:\s]+|[,!?\.\;\:]', text)
    
    # 빈 문자열과 너무 짧은 단어 제거 (2글자 이상)
    words = [w.strip() for w in words if w.strip() and len(w.strip()) >= 2]
    
    return words

def analyze_voynich_file(filepath, output_file='voynich_translation.txt', max_words=None):
    """
    보이니치 파일을 읽어서 전체 분석
    
    Args:
        filepath: 보이니치 텍스트 파일 경로
        output_file: 결과 저장 파일 경로
        max_words: 최대 분석 단어 수 (None이면 전체)
    """
    print("=" * 80)
    print("보이니치 문서 전체 분석 시작")
    print("=" * 80)
    print(f"데이터베이스: {get_language_count()}개 언어, {get_total_word_count()}개 단어")
    print()
    
    # 파일 읽기
    print(f"파일 읽는 중: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # 단어로 분리
    print("텍스트 분리 중...")
    words = split_voynich_text(full_text)
    
    total_words = len(words)
    if max_words:
        words = words[:max_words]
        print(f"총 {total_words}개 단어 중 {max_words}개 분석")
    else:
        print(f"총 {total_words}개 단어 분석")
    
    print()
    
    # 보이니치 분석기 초기화
    print("분석 시스템 초기화 중...")
    analyzer = VoynichAnalyzer()
    
    # 언어 매칭 시스템 초기화
    matcher = LanguageMatcher(analyzer)
    
    # 데이터베이스 로드
    print("데이터베이스 로드 중...")
    for language, words in LANGUAGE_DATABASE.items():
        matcher.add_language_words(language, words)
    
    # 결과 저장
    results = []
    translated_words = []
    
    # 진행률 표시를 위한 변수
    total = len(words)
    progress_step = max(1, total // 20)  # 5%씩 진행률 표시
    
    print("번역 시작...")
    print("-" * 80)
    
    for idx, voynich_word in enumerate(words, 1):
        # 진행률 표시
        if idx % progress_step == 0 or idx == total:
            percentage = (idx / total) * 100
            print(f"진행률: {idx}/{total} ({percentage:.1f}%)")
        
        # 구두점은 그대로 유지
        if voynich_word in [',', '.', '!', '?', ';', ':']:
            results.append(f"{idx}. {voynich_word} -> {voynich_word}")
            translated_words.append(voynich_word)
            continue
        
        # 단어 매칭
        matches = matcher.find_matches(voynich_word, top_n=1)
        
        if matches:
            best_match = matches[0]
            lang = best_match['language']
            word = best_match['word']
            similarity = best_match['similarity']
            
            result_line = f"{idx}. {voynich_word} -> {word} ({lang}, {similarity:.1f}%)"
            results.append(result_line)
            translated_words.append(word)
        else:
            result_line = f"{idx}. {voynich_word} -> [매칭 실패]"
            results.append(result_line)
            translated_words.append(f"[{voynich_word}]")
    
    print("-" * 80)
    print("번역 완료!")
    print()
    
    # 결과 저장
    print(f"결과 저장 중: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        # 헤더
        f.write("=" * 80 + "\n")
        f.write("보이니치 문서 번역 결과\n")
        f.write("=" * 80 + "\n")
        f.write(f"총 단어 수: {len(words)}\n")
        f.write(f"데이터베이스: {get_language_count()}개 언어, {get_total_word_count()}개 단어\n")
        f.write("\n")
        
        # 번역된 텍스트 (한 줄로)
        f.write("=" * 80 + "\n")
        f.write("번역된 텍스트:\n")
        f.write("=" * 80 + "\n")
        f.write(" ".join(translated_words) + "\n")
        f.write("\n")
        
        # 상세 매칭 결과
        f.write("=" * 80 + "\n")
        f.write("상세 매칭 결과:\n")
        f.write("=" * 80 + "\n")
        for result in results:
            f.write(result + "\n")
    
    print(f"✓ 결과가 '{output_file}'에 저장되었습니다")
    print()
    
    # 통계 출력
    print("=" * 80)
    print("분석 통계")
    print("=" * 80)
    
    # 언어별 통계
    lang_counts = {}
    for result in results:
        if '(' in result and ')' in result:
            # 언어 정보 추출
            try:
                lang_part = result.split('(')[1].split(',')[0]
                lang_counts[lang_part] = lang_counts.get(lang_part, 0) + 1
            except:
                pass
    
    if lang_counts:
        print("\n언어별 매칭:")
        for lang, count in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(words)) * 100
            print(f"  {lang}: {count}개 ({percentage:.1f}%)")
    
    # 평均 유사도 계산
    similarities = []
    for result in results:
        if '%' in result:
            try:
                sim_str = result.split('(')[-1].split('%')[0].split(',')[-1].strip()
                similarities.append(float(sim_str))
            except:
                pass
    
    if similarities:
        avg_sim = sum(similarities) / len(similarities)
        print(f"\n평균 유사도: {avg_sim:.1f}%")
    
    print()
    print("분석 완료!")
    print("=" * 80)

if __name__ == "__main__":
    # voynich.nowhitespace.txt 파일 분석
    # 먼저 처음 500단어만 테스트
    print("보이니치 문서 분석기")
    print()
    print("옵션을 선택하세요:")
    print("1. 테스트 (처음 500단어)")
    print("2. 중간 분석 (처음 2000단어)")
    print("3. 전체 분석 (모든 단어)")
    print()
    
    choice = input("선택 (1-3): ").strip()
    
    if choice == '1':
        analyze_voynich_file('voynich.nowhitespace.txt', 
                           output_file='voynich_translation_test.txt',
                           max_words=500)
    elif choice == '2':
        analyze_voynich_file('voynich.nowhitespace.txt',
                           output_file='voynich_translation_2000.txt',
                           max_words=2000)
    elif choice == '3':
        analyze_voynich_file('voynich.nowhitespace.txt',
                           output_file='voynich_translation_full.txt',
                           max_words=None)
    else:
        print("잘못된 선택입니다. 기본값(테스트 500단어)으로 실행합니다.")
        analyze_voynich_file('voynich.nowhitespace.txt',
                           output_file='voynich_translation_test.txt',
                           max_words=500)
