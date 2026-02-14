# -*- coding: utf-8 -*-
"""
보이니치 문서 분석 시스템
- 보이니치 문자에 번호 부여
- n/b 코드 변환
- 다국어 단어와 매칭
- 고급 비트 계산 및 코사인 유사도
"""

from advanced_nb_calculator import (
    BIT_MAX_NB, BIT_MIN_NB,
    word_nb_unicode_format,
    calculate_similarity,
    cosine_similarity,
    calculate_array_order_and_duplicate,
    word_sim,
    levenshtein,
    identify_language
)

class NBCodeConverter:
    """n/b (숫자/비트) 코드 변환기"""
    
    def __init__(self):
        # 문자-번호 매핑 테이블
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
    
    def char_to_nb_code(self, char):
        """문자를 n/b 코드로 변환"""
        number = self.assign_number(char)
        # 8비트 이진수로 변환
        binary = format(number, '08b')
        # n/b 형식: 숫자_비트값
        return f"{number}/{binary}"
    
    def text_to_nb_codes(self, text):
        """텍스트를 n/b 코드 배열로 변환"""
        codes = []
        for char in text:
            if char.strip():  # 공백 제외
                code = self.char_to_nb_code(char)
                codes.append({
                    'char': char,
                    'number': self.char_to_number[char],
                    'nb_code': code
                })
        return codes
    
    def get_pattern_signature(self, text):
        """텍스트의 패턴 시그니처 생성 (매칭용)"""
        codes = self.text_to_nb_codes(text)
        # 숫자 패턴
        number_pattern = [c['number'] for c in codes]
        # 비트 합계
        bit_sum = sum(bin(c['number']).count('1') for c in codes)
        return {
            'length': len(codes),
            'pattern': number_pattern,
            'bit_sum': bit_sum,
            'nb_codes': codes
        }


class VoynichAnalyzer:
    """보이니치 문서 분석기"""
    
    def __init__(self):
        self.converter = NBCodeConverter()
        self.voynich_text = ""
        self.voynich_codes = []
        
    def load_voynich_text(self, text):
        """보이니치 텍스트 로드 및 번호 부여"""
        self.voynich_text = text
        print(f"\n=== 보이니치 문서 분석 ===")
        print(f"총 문자 수: {len(text)}\n")
        
        # 각 문자에 번호 부여 및 n/b 코드 변환
        self.voynich_codes = self.converter.text_to_nb_codes(text)
        
        # 결과 출력
        print("문자별 번호 및 n/b 코드:")
        for i, item in enumerate(self.voynich_codes, 1):  # 모든 문자 출력
            print(f"{i:3d}. '{item['char']}' → 번호: {item['number']:3d} → n/b: {item['nb_code']}")
        
        # 통계 정보 계산
        print(f"\n{'='*60}")
        print("📊 n/b 코드 통계 분석")
        print(f"{'='*60}")
        self._print_statistics()
        
        return self.voynich_codes
    
    def _print_statistics(self):
        """n/b 코드 통계 정보 출력"""
        if not self.voynich_codes:
            return
        
        # 번호 추출
        numbers = [item['number'] for item in self.voynich_codes]
        
        # 기본 통계
        max_num = max(numbers)
        min_num = min(numbers)
        avg_num = sum(numbers) / len(numbers)
        
        # 비트 수 계산
        bit_counts = [bin(num).count('1') for num in numbers]
        max_bits = max(bit_counts)
        min_bits = min(bit_counts)
        avg_bits = sum(bit_counts) / len(bit_counts)
        total_bits = sum(bit_counts)
        
        # 정규화 값 (0~1 범위)
        normalized = [(num - min_num) / (max_num - min_num) if max_num != min_num else 0 
                      for num in numbers]
        
        print(f"\n🔢 번호 통계:")
        print(f"   최소값(MIN): {min_num}")
        print(f"   최대값(MAX): {max_num}")
        print(f"   평균값(AVG): {avg_num:.2f}")
        print(f"   범위(RANGE): {max_num - min_num}")
        
        print(f"\n💾 비트 통계:")
        print(f"   최소 비트 수: {min_bits}")
        print(f"   최대 비트 수: {max_bits}")
        print(f"   평균 비트 수: {avg_bits:.2f}")
        print(f"   총 비트 합계: {total_bits}")
        
        print(f"\n📈 정규화 값 (MIN-MAX Normalization):")
        print(f"   공식: (값 - MIN) / (MAX - MIN)")
        for i, (item, norm) in enumerate(zip(self.voynich_codes[:10], normalized[:10]), 1):
            print(f"   {i:2d}. '{item['char']}' (번호:{item['number']:2d}) → 정규화: {norm:.4f}")
        if len(normalized) > 10:
            print(f"   ... (총 {len(normalized)}개)")
        
        print(f"\n🎯 전체 텍스트 시그니처:")
        print(f"   문자 수: {len(self.voynich_codes)}")
        print(f"   고유 문자: {len(self.converter.char_to_number)}개")
        print(f"   숫자 패턴: {numbers[:15]}..." if len(numbers) > 15 else f"   숫자 패턴: {numbers}")
        print(f"   비트 시그니처: {total_bits}")
        print(f"   복잡도 지수: {total_bits / len(numbers):.2f}")
        
        # 빈도수 분석
        from collections import Counter
        freq = Counter(numbers)
        print(f"\n📊 빈도수 분석 (상위 5개):")
        for num, count in freq.most_common(5):
            char = self.converter.number_to_char[num]
            percentage = (count / len(numbers)) * 100
            print(f"   '{char}' (번호:{num}) → {count}회 ({percentage:.1f}%)")
    
    def get_unique_chars(self):
        """고유 문자 목록 반환"""
        return self.converter.char_to_number
    

class LanguageMatcher:
    """다국어 단어 매칭기 (최적화 버전)"""
    
    def __init__(self, voynich_analyzer):
        self.analyzer = voynich_analyzer
        self.converter = voynich_analyzer.converter
        self.language_database = {}
        self.word_cache = {}  # 캐싱 추가
        
    def add_language_words(self, language, words):
        """언어별 단어 추가 (사전 계산 포함)"""
        self.language_database[language] = []
        
        print(f"\n{language}: 단어 분석 중...", end=" ")
        for word in words:
            # 사전에 유니코드와 비트 값 계산
            word_unicode = word_nb_unicode_format(word)
            word_max = BIT_MAX_NB(word_unicode)
            word_min = BIT_MIN_NB(word_unicode)
            
            self.language_database[language].append({
                'word': word,
                'unicode': word_unicode,
                'max': word_max,
                'min': word_min
            })
        
        print(f"{len(words)}개 완료")
    
    def find_matches(self, voynich_word, threshold=0.7):
        """보이니치 단어와 매칭되는 단어들 찾기 (최적화 + 빠른 필터링)"""
        # 캐시 확인
        if voynich_word in self.word_cache:
            cached = self.word_cache[voynich_word]
            return [m for m in cached if m['similarity'] >= threshold]
        
        # 보이니치 단어의 유니코드 배열 및 비트 값 계산
        voynich_unicode = word_nb_unicode_format(voynich_word)
        voynich_max = BIT_MAX_NB(voynich_unicode)
        voynich_min = BIT_MIN_NB(voynich_unicode)
        voynich_len = len(voynich_word)
        
        vec1 = [float(x) for x in voynich_unicode]
        
        matches = []
        
        for language, words in self.language_database.items():
            for word_data in words:
                word = word_data['word']
                
                # 빠른 필터링: 길이 차이가 너무 크면 스킵
                len_diff = abs(len(word) - voynich_len)
                if len_diff > max(len(word), voynich_len) * 0.5:
                    continue
                
                # 사전 계산된 값 사용
                word_unicode = word_data['unicode']
                word_max = word_data['max']
                word_min = word_data['min']
                
                # 1. 비트 값 유사도 (빠른 계산)
                bit_similarity = word_sim(voynich_max, voynich_min, word_max, word_min)
                
                # 빠른 필터: 비트 유사도가 너무 낮으면 스킵
                if bit_similarity < 30:
                    continue
                
                # 2. 코사인 유사도
                vec2 = [float(x) for x in word_unicode]
                cosine_sim = cosine_similarity(vec1, vec2) * 100
                
                # 3. Levenshtein 거리 (간단한 계산)
                max_len = max(len(voynich_word), len(word))
                lev_distance = levenshtein(voynich_word, word)
                lev_similarity = ((max_len - lev_distance) / max_len) * 100 if max_len > 0 else 0
                
                # 간소화된 종합 유사도 (3가지만 사용)
                final_similarity = (
                    bit_similarity * 0.40 +
                    cosine_sim * 0.40 +
                    lev_similarity * 0.20
                ) / 100
                
                if final_similarity >= threshold:
                    matches.append({
                        'language': language,
                        'word': word,
                        'similarity': final_similarity,
                        'details': {
                            'bit_sim': bit_similarity / 100,
                            'cosine': cosine_sim / 100,
                            'levenshtein': lev_similarity / 100,
                            'voynich_max': voynich_max,
                            'voynich_min': voynich_min,
                            'word_max': word_max,
                            'word_min': word_min,
                        }
                    })
        
        # 유사도 순으로 정렬
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        # 캐시 저장
        self.word_cache[voynich_word] = matches
        
        return matches



def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("보이니치 문서 n/b 코드 분석 시스템 (고급 알고리즘 - 확장판)")
    print("=" * 80)
    
    # 1. 보이니치 분석기 생성
    analyzer = VoynichAnalyzer()
    
    # 2. 실제 보이니치 문장 (여러 단어로 구성)
    voynich_sentence = "fachys ykal ar ataiin shol shory cthres y kor sholdy"
    print(f"\n📜 분석할 보이니치 문장:")
    print(f"   '{voynich_sentence}'")
    print(f"   단어 수: {len(voynich_sentence.split())}개\n")
    
    analyzer.load_voynich_text(voynich_sentence)
    
    print(f"\n고유 문자 종류: {len(analyzer.get_unique_chars())}개")
    print("고유 문자 목록:", list(analyzer.get_unique_chars().keys()))
    
    # 3. 언어 매칭기 생성
    matcher = LanguageMatcher(analyzer)
    
    # 4. 대폭 확장된 다국어 단어 데이터베이스
    print("\n" + "=" * 80)
    print("📚 다국어 단어 데이터베이스 로딩")
    print("=" * 80)
    
    # 한국어 - 100개 이상
    matcher.add_language_words('한국어', [
        # 자연
        '하늘', '땅', '바다', '산', '강', '나무', '꽃', '풀', '돌', '물',
        '불', '바람', '구름', '비', '눈', '해', '달', '별', '빛', '그림자',
        # 동물
        '말', '소', '양', '개', '고양이', '새', '물고기', '용', '호랑이', '사자',
        # 식물
        '장미', '백합', '연꽃', '소나무', '대나무', '버드나무', '단풍', '은행',
        # 추상
        '사랑', '평화', '자유', '진리', '지혜', '용기', '희망', '믿음',
        '기쁨', '슬픔', '분노', '두려움', '행복', '고통', '즐거움', '아름다움',
        # 행동
        '걷다', '뛰다', '보다', '듣다', '말하다', '먹다', '자다', '일하다',
        # 시간
        '아침', '낮', '저녁', '밤', '봄', '여름', '가을', '겨울',
        # 방향/위치
        '위', '아래', '앞', '뒤', '왼쪽', '오른쪽', '안', '밖', '가운데',
        # 인간
        '사람', '남자', '여자', '아이', '부모', '친구', '왕', '여왕',
        # 신체
        '머리', '눈', '귀', '코', '입', '손', '발', '심장', '몸'
    ])
    
    # 영어 - 100개 이상
    matcher.add_language_words('영어', [
        # Nature
        'sky', 'earth', 'sea', 'mountain', 'river', 'tree', 'flower', 'grass', 'stone', 'water',
        'fire', 'wind', 'cloud', 'rain', 'snow', 'sun', 'moon', 'star', 'light', 'shadow',
        # Animals
        'horse', 'cow', 'sheep', 'dog', 'cat', 'bird', 'fish', 'dragon', 'tiger', 'lion',
        # Plants
        'rose', 'lily', 'lotus', 'pine', 'bamboo', 'willow', 'maple', 'ginkgo',
        # Abstract
        'love', 'peace', 'freedom', 'truth', 'wisdom', 'courage', 'hope', 'faith',
        'joy', 'sadness', 'anger', 'fear', 'happiness', 'pain', 'pleasure', 'beauty',
        # Actions
        'walk', 'run', 'see', 'hear', 'speak', 'eat', 'sleep', 'work',
        # Time
        'morning', 'day', 'evening', 'night', 'spring', 'summer', 'autumn', 'winter',
        # Direction
        'up', 'down', 'front', 'back', 'left', 'right', 'inside', 'outside', 'center',
        # Human
        'human', 'man', 'woman', 'child', 'parent', 'friend', 'king', 'queen',
        # Body
        'head', 'eye', 'ear', 'nose', 'mouth', 'hand', 'foot', 'heart', 'body',
        # Common words
        'the', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with'
    ])
    
    # 라틴어 - 100개 이상
    matcher.add_language_words('라틴어', [
        # Natura
        'caelum', 'terra', 'mare', 'mons', 'flumen', 'arbor', 'flos', 'herba', 'lapis', 'aqua',
        'ignis', 'ventus', 'nubes', 'pluvia', 'nix', 'sol', 'luna', 'stella', 'lux', 'umbra',
        # Animalia
        'equus', 'bos', 'ovis', 'canis', 'felis', 'avis', 'piscis', 'draco', 'tigris', 'leo',
        # Plantae
        'rosa', 'lilium', 'lotos', 'pinus', 'arundo', 'salix', 'acer',
        # Abstracta
        'amor', 'pax', 'libertas', 'veritas', 'sapientia', 'fortitudo', 'spes', 'fides',
        'gaudium', 'tristitia', 'ira', 'timor', 'felicitas', 'dolor', 'voluptas', 'pulchritudo',
        # Verba
        'ambulare', 'currere', 'videre', 'audire', 'dicere', 'edere', 'dormire', 'laborare',
        # Tempus
        'mane', 'dies', 'vesper', 'nox', 'ver', 'aestas', 'autumnus', 'hiems',
        # Directio
        'supra', 'infra', 'ante', 'post', 'sinister', 'dexter', 'intus', 'extra',
        # Homo
        'homo', 'vir', 'femina', 'puer', 'parens', 'amicus', 'rex', 'regina',
        # Corpus
        'caput', 'oculus', 'auris', 'nasus', 'os', 'manus', 'pes', 'cor', 'corpus',
        # Herbal/Medicine terms (보이니치와 관련)
        'herba', 'radix', 'folium', 'semen', 'cortex', 'medicina', 'potio', 'unguentum'
    ])
    
    # 5. 문장 단위 분석 및 번역 시도
    print("\n" + "=" * 80)
    print("🔍 보이니치 문장 단어별 분석 및 번역 시도")
    print("=" * 80)
    
    voynich_words = voynich_sentence.split()
    translated_sentence = []
    detailed_results = []
    
    for idx, vword in enumerate(voynich_words, 1):
        print(f"[{idx}/{len(voynich_words)}] '{vword}' 분석 중...", end=" ")
        
        matches = matcher.find_matches(vword, threshold=0.30)
        
        if matches:
            best_match = matches[0]
            translated_sentence.append(best_match['word'])
            detailed_results.append({
                'original': vword,
                'translated': best_match['word'],
                'language': best_match['language'],
                'similarity': best_match['similarity'],
                'top3': matches[:3]
            })
            print(f"✅ {best_match['word']} ({best_match['language']}, {best_match['similarity']:.1%})")
        else:
            translated_sentence.append(f"[{vword}]")
            detailed_results.append({
                'original': vword,
                'translated': f"[{vword}]",
                'language': 'unknown',
                'similarity': 0,
                'top3': []
            })
            print(f"❌ 매칭 실패")
    
    # 6. 번역된 문장 출력
    print("\n" + "=" * 80)
    print("📝 번역 결과")
    print("=" * 80)
    print(f"\n원문 (보이니치):")
    print(f"  {voynich_sentence}")
    print(f"\n번역문 (다국어 조합):")
    print(f"  {' '.join(translated_sentence)}")
    
    # 7. 상세 분석 결과
    print(f"\n" + "=" * 80)
    print("📊 단어별 상세 분석")
    print("=" * 80)
    for result in detailed_results:
        print(f"\n'{result['original']}' → '{result['translated']}'")
        if result['top3']:
            print(f"  상위 후보:")
            for i, match in enumerate(result['top3'], 1):
                print(f"    {i}. [{match['language']:^6}] {match['word']:12} ({match['similarity']:.1%}) "
                      f"[비트:{match['details']['bit_sim']:.0%} 코사인:{match['details']['cosine']:.0%}]")
    
    # 8. 언어별 통계
    from collections import Counter
    language_stats = Counter()
    for result in detailed_results:
        if result['language'] != 'unknown':
            language_stats[result['language']] += 1
    
    print(f"\n" + "=" * 80)
    print("📈 언어별 매칭 통계")
    print("=" * 80)
    for lang, count in language_stats.most_common():
        percentage = (count / len(voynich_words)) * 100
        print(f"  • {lang}: {count}개 단어 ({percentage:.1f}%)")
    
    # 9. 가능한 해석
    print(f"\n" + "=" * 80)
    print("💡 가능한 해석")
    print("=" * 80)
    print(f"\n이 보이니치 문장은 다음과 같이 해석될 수 있습니다:")
    print(f"  '{' '.join(translated_sentence)}'")
    print(f"\n주요 언어: {language_stats.most_common(1)[0][0] if language_stats else 'N/A'}")
    avg_similarity = sum(r['similarity'] for r in detailed_results) / len(detailed_results) if detailed_results else 0
    print(f"평균 유사도: {avg_similarity:.1%}")
    
    print("\n" + "=" * 80)
    print("분석 완료!")
    print("=" * 80)


if __name__ == "__main__":
    main()
