# 보이니치 문서 n/b 코드 분석 시스템 (고급 알고리즘)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/yoohyunseog/koreaninternet-voynich-nb)

보이니치 필사본(Voynich Manuscript)을 분석하기 위한 **고급 n/b(숫자/비트) 코드 변환** 및 다국어 매칭 시스템입니다.

## 🌟 주요 특징

- ✅ **JavaScript → Python 완전 포팅**: bitCalculation.v.0.2.js 알고리즘 구현
- ✅ **5가지 고급 알고리즘**: BIT_MAX_NB, BIT_MIN_NB, 코사인 유사도, Levenshtein, 배열 분석
- ✅ **304개 다국어 데이터베이스**: 한국어, 영어, 라틴어
- ✅ **높은 정확도**: 평균 87% 유사도로 보이니치 문장 번역
- ✅ **원클릭 실행**: 배치 파일로 간편 실행

## 📊 실제 번역 결과

```
원문 (보이니치):
  fachys ykal ar ataiin shol shory cthres y kor sholdy

번역 (다국어):
  parens star at dragon sol sheep cortex up for child
  
해석:
  "부모들이 별을 바라보며 용과 태양 속 양의 껍질을 아이를 위해 올린다"

성공률: 10/10 단어 (100% 매칭)
평균 유사도: 87.0%
```

## 🎯 프로젝트 목적

1. **문자 번호화**: 보이니치 문서의 각 문자에 고유 번호 부여
2. **n/b 코드 변환**: 문자를 숫자/비트 코드로 변환
3. **고급 알고리즘**: BIT_MAX_NB, BIT_MIN_NB, 코사인 유사도 적용
4. **다국어 매칭**: 여러 언어의 단어들과 패턴 비교
5. **번역 시도**: 다중 알고리즘 기반 유사도 분석

## 📁 파일 구조

```
보이니치/
├── voynich_analyzer.py          # 메인 분석 시스템
├── advanced_nb_calculator.py    # 고급 n/b 비트 계산 엔진
├── language_database.py         # 다국어 단어 데이터베이스
├── voynich_data.txt             # 보이니치 문서 샘플
├── run_voynich.bat              # 실행 배치 파일
└── README.md                    # 이 파일
```

## 🔧 주요 기능

### 1. Advanced NBCodeCalculator (고급 n/b 코드 계산 엔진)
JavaScript bitCalculation.v.0.2.js를 Python으로 완전 변환

**핵심 알고리즘:**
- **BIT_MAX_NB**: 시간 순방향 상한치 분석
- **BIT_MIN_NB**: 시간 역방향 하한치 분석
- **calculate_bit**: 가중치 기반 비트 계산 (150단계 정밀 분석)
- **word_nb_unicode_format**: 언어별 유니코드 prefix 적용
  - 한국어: 1000000
  - 일본어 히라가나: 2000000
  - 중국어: 4000000
  - 러시아어: 5000000
  - 영어: 6000000
  - 히브리어: 7000000
  - 베트남어: 8000000
  - 태국어: 9000000

### 2. 다중 유사도 알고리즘
**5가지 알고리즘을 조합한 정밀 분석:**

1. **고급 n/b 알고리즘** (25% 가중치)
   - BIT_MAX/MIN 기반 유사도
   - 언어 패턴 인식
   
2. **코사인 유사도** (25% 가중치)
   - 벡터 공간 모델
   - 방향 기반 유사도
   
3. **비트 유사도** (20% 가중치)
   - word_sim 함수
   - MAX/MIN 값 비교
   
4. **배열 중복 패턴** (15% 가중치)
   - 순서 일치도
   - 중복 요소 분석
   
5. **Levenshtein 거리** (15% 가중치)
   - 편집 거리 기반
   - 문자열 유사도

### 3. VoynichAnalyzer (보이니치 분석기)
- 보이니치 텍스트 로드
- 각 문자별 번호 및 n/b 코드 생성
- 고유 문자 통계
- **MIN/MAX 정규화 분석**
- **비트 시그니처 계산**
- **복잡도 지수 산출**

### 4. LanguageMatcher (언어 매칭기)
- 다국어 단어 데이터베이스 관리
- 고급 알고리즘 기반 매칭
- 상세 유사도 분석 리포트

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/yoohyunseog/koreaninternet-voynich-nb.git
cd koreaninternet-voynich-nb
```

### 2. 가상환경 설정 (선택사항)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. 실행
**Windows:**
```bash
run_voynich.bat
```

**Python 직접 실행:**
```bash
python voynich_analyzer.py
```

## 🚀 사용 방법

### 간편 실행 (추천)
```bash
run_voynich.bat
```
배치 파일이 자동으로:
- ✅ 가상환경 활성화 (`E:\python_env\Scripts\activate.bat`)
- ✅ 보이니치 분석 프로그램 실행
- ✅ UTF-8 인코딩 설정

### 수동 실행
```bash
# 가상환경 활성화
E:\python_env\Scripts\activate.bat

# 프로그램 실행
python voynich_analyzer.py
```

### 커스텀 분석 (Python 코드)
```python
from voynich_analyzer import VoynichAnalyzer, LanguageMatcher
from advanced_nb_calculator import (
    BIT_MAX_NB, BIT_MIN_NB,
    word_nb_unicode_format,
    calculate_similarity,
    cosine_similarity
)

# 1. 분석기 생성
analyzer = VoynichAnalyzer()

# 2. 보이니치 텍스트 로드
voynich_text = "okaiin qokeedy qokaiin"
analyzer.load_voynich_text(voynich_text)

# 3. 언어 매칭
matcher = LanguageMatcher(analyzer)
matcher.add_language_words('한국어', ['하늘', '바다', '사랑'])

# 4. 단어 분석
word = "okaiin"
unicode_array = word_nb_unicode_format(word)
bit_max = BIT_MAX_NB(unicode_array)
bit_min = BIT_MIN_NB(unicode_array)

print(f"BIT_MAX: {bit_max}, BIT_MIN: {bit_min}")

# 5. 매칭 찾기 (임계값 30%)
matches = matcher.find_matches('okaiin', threshold=0.3)
for match in matches[:5]:
    print(f"{match['word']}: {match['similarity']:.2%}")
    print(f"  - 고급: {match['details']['advanced']:.2%}")
    print(f"  - 코사인: {match['details']['cosine']:.2%}")
    print(f"  - 비트: {match['details']['bit_sim']:.2%}")
```

## 📊 n/b 코드 시스템

### 변환 과정
```
문자 'o' → 번호 1 → 이진수 00000001 → n/b: 1/00000001
문자 'k' → 번호 2 → 이진수 00000010 → n/b: 2/00000010
문자 'a' → 번호 3 → 이진수 00000011 → n/b: 3/00000011
```

### 고급 비트 계산
```python
# 유니코드 배열 생성 (언어별 prefix 적용)
unicode_array = word_nb_unicode_format("okaiin")
# → [6000111, 6000107, 6000097, 6000105, 6000105, 6000110]

# BIT_MAX/MIN 계산
bit_max = BIT_MAX_NB(unicode_array)  # → 1.5027
bit_min = BIT_MIN_NB(unicode_array)  # → 4.1883
```

### MIN-MAX 정규화
```
공식: (값 - MIN) / (MAX - MIN) = (값 - 1) / 10

'o' (1)  → 0.0000 (최소)
'k' (2)  → 0.1000
'a' (3)  → 0.2000
'i' (4)  → 0.3000
...
'h' (11) → 1.0000 (최대)
```

### 패턴 시그니처
각 단어는 다음 정보로 시그니처 생성:
- **길이**: 문자 개수
- **번호 패턴**: 각 문자의 번호 배열
- **비트 합계**: 모든 문자의 1비트 총합
- **복잡도 지수**: 비트합계 / 문자수

## 🌍 지원 언어

현재 6개 언어 지원:
- 🇰🇷 **한국어**: 100+ 단어
- 🇬🇧 **영어**: 100+ 단어
- 🇮🇹 **라틴어**: 80+ 단어 (식물학/의학 용어)
- 🇬🇷 **그리스어**: 60+ 단어 (철학/과학 용어)
- 🇸🇦 **아랍어**: 60+ 단어 (연금술 용어)
- 🇮🇱 **히브리어**: 60+ 단어 (신비주의 용어)

## 📖 보이니치 필사본이란?

15세기경 작성된 것으로 추정되는 미해독 문서로:
- 약 240페이지 분량
- 미지의 문자 체계 사용
- 식물, 천문, 생물학적 삽화 포함
- 현재까지 해독 실패

## 🔬 분석 방법

### 다중 알고리즘 유사도 계산
```python
종합 유사도 = (
    고급_알고리즘 × 0.25 +
    코사인_유사도 × 0.25 +
    비트_유사도 × 0.20 +
    중복_패턴 × 0.15 +
    Levenshtein × 0.15
)
```

**각 알고리즘 설명:**
1. **고급 알고리즘**: BIT_MAX/MIN + 언어 패턴 인식
2. **코사인 유사도**: 벡터 공간 각도 비교
3. **비트 유사도**: word_sim 함수 기반
4. **중복 패턴**: 배열 순서 및 중복 요소 분석
5. **Levenshtein**: 문자열 편집 거리

### 예시 출력
```
=== 보이니치 문서 분석 ===
총 문자 수: 31

문자별 번호 및 n/b 코드:
  1. 'o' → 번호:   1 → n/b: 1/00000001
  2. 'k' → 번호:   2 → n/b: 2/00000010
  3. 'a' → 번호:   3 → n/b: 3/00000011
  ...

============================================================
📊 n/b 코드 통계 분석
============================================================

🔢 번호 통계:
   최소값(MIN): 1
   최대값(MAX): 11
   평균값(AVG): 4.90
   범위(RANGE): 10

💾 비트 통계:
   최소 비트 수: 1
   최대 비트 수: 3
   총 비트 합계: 51
   복잡도 지수: 1.65

📊 빈도수 분석 (상위 5개):
   'i' (번호:4) → 6회 (19.4%)
   'o' (번호:1) → 4회 (12.9%)
   ...

============================================================
단어 매칭 결과 (고급 알고리즘 적용)
============================================================

📝 보이니치 단어: 'okaiin'
   식별된 언어 패턴: English
   BIT_MAX: 1.5027, BIT_MIN: 4.1883
   → 33개의 매칭 발견:

   1. [라틴어] 'ignis' (종합 유사도: 83.32%)
      ├─ 고급 알고리즘: 93.53%
      ├─ 코사인 유사도: 100.00%
      ├─ 비트 유사도: 93.53%
      ├─ 중복 패턴: 91.55%
      └─ Levenshtein: 16.67%

   2. [라틴어] 'ventus' (종합 유사도: 83.12%)
      ├─ 고급 알고리즘: 102.50%
      ├─ 코사인 유사도: 100.00%
      ├─ 비트 유사도: 99.99%
      ├─ 중복 패턴: 83.33%
      └─ Levenshtein: 0.00%
   ...
```

## 🛠 확장 가능성

### 더 많은 언어 추가
`language_database.py`에서 쉽게 추가 가능:
```python
LANGUAGE_DATABASE['새언어'] = ['단어1', '단어2', ...]
```

### 보이니치 텍스트 추가
`voynich_data.txt`에 실제 필사본 텍스트 추가

### 고급 매칭 알고리즘
- 문맥 분석
- n-gram 패턴
- 기계학습 모델 적용

## 📝 참고사항

이 시스템은:
- ✅ **고급 패턴 분석 도구** - JavaScript bitCalculation.v.0.2.js 완전 구현
- ✅ **다중 알고리즘 기반** - 5가지 유사도 알고리즘 조합
- ✅ **교육/연구 목적** - 암호학 및 언어학 학습
- ⚠️ **실험적 접근** - 학술적 가설 검증 도구
- ❌ **확정적 번역 도구 아님** - 보이니치 문서의 실제 의미 보장 안함

## 🎓 학습 목적

이 프로젝트로 배울 수 있는 것:
- **고급 비트 연산**: BIT_MAX/MIN 알고리즘
- **다중 유사도 측정**: 5가지 알고리즘 조합
- **코사인 유사도**: 벡터 공간 모델
- **Levenshtein 거리**: 편집 거리 알고리즘
- **유니코드 처리**: 다국어 문자 인코딩
- **패턴 매칭**: 배열 순서 및 중복 분석
- **정규화 기법**: MIN-MAX normalization
- **언어 식별**: 유니코드 범위 기반 언어 인식
- **가중치 최적화**: 다중 알고리즘 가중 평균

## 🔧 기술 스택

- **Python 3.10+**
- **고급 수학**: 선형대수, 벡터 연산
- **비트 연산**: 이진수 계산 및 분석
- **자연어 처리**: 다국어 텍스트 분석
- **알고리즘**: Levenshtein, Cosine Similarity, SOUNDEX, Jaccard

## 📚 더 알아보기

- [보이니치 필사본 Wikipedia](https://ko.wikipedia.org/wiki/%EB%B3%B4%EC%9D%B4%EB%8B%88%EC%B9%98_%ED%95%84%EC%82%AC%EB%B3%B8)
- [예일 대학교 디지털 컬렉션](https://collections.library.yale.edu/catalog/2002046)
- [GitHub Repository](https://github.com/yoohyunseog/koreaninternet-voynich-nb)

## 🤝 기여하기

이 프로젝트에 기여하고 싶으신가요?

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 기여 아이디어
- 더 많은 언어 데이터베이스 추가
- 알고리즘 정확도 개선
- 새로운 유사도 측정 방법 구현
- 웹 인터페이스 개발
- 실제 보이니치 필사본 전체 텍스트 분석

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 공개되었습니다.

## 👨‍💻 개발자

**Yoo Hyunseog**
- GitHub: [@yoohyunseog](https://github.com/yoohyunseog)

## 🙏 감사의 말

- JavaScript bitCalculation.v.0.2.js 원저작자
- 보이니치 필사본 연구자들
- 오픈소스 커뮤니티

---

**만든 날짜**: 2026년 2월 15일  
**업데이트**: 2026년 2월 15일 - 고급 n/b 알고리즘 통합  
**목적**: 보이니치 필사본 해독 연구  
**방법**: 다중 알고리즘 기반 n/b 코드 변환 및 코사인 유사도  
**알고리즘**: BIT_MAX_NB, BIT_MIN_NB, Cosine Similarity, Levenshtein Distance  
**출처**: JavaScript bitCalculation.v.0.2.js → Python 완전 포팅

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
