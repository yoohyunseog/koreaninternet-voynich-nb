# -*- coding: utf-8 -*-
"""
Generate complete index.html from voynich_to_english_sentence.txt
"""

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_voynich_data() -> dict:
    """Load data from voynich_to_english_sentence.txt"""
    data = {
        "english_sentence": "",
        "korean_translation": "",
        "pairs": [],
    }
    
    sent_file = ROOT_DIR / "outputs" / "voynich_to_english_sentence.txt"
    if not sent_file.exists():
        return data
    
    with sent_file.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        in_sentence = False
        in_translation = False
        in_details = False
        
        for line in lines:
            if line.startswith("Sentence:"):
                in_sentence = True
                in_translation = False
                in_details = False
            elif line.startswith("GPT Translation"):
                in_sentence = False
                in_translation = True
                in_details = False
            elif line.startswith("Details:"):
                in_sentence = False
                in_translation = False
                in_details = True
            elif in_sentence and line.strip():
                data["english_sentence"] += line.strip() + " "
            elif in_translation and line.strip():
                data["korean_translation"] += line.strip() + " "
            elif in_details and line.strip():
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    data["pairs"].append((parts[0], parts[1]))
    
    return data


def build_word_links(words: list[str]) -> str:
    """Build HTML links for words"""
    links = []
    for word in words:
        clean = word.strip()
        if not clean:
            continue
        links.append(
            f'                <a href="https://search.naver.com/search.naver?query=보이니치+해석+{clean}">{clean}</a>,\n'
        )
    
    if links:
        # Remove comma from last link
        links[-1] = links[-1].replace(",", ".")
    
    return "".join(links)


def build_voynich_links(pairs: list[tuple]) -> str:
    """Build HTML links for Voynich text"""
    links = []
    for voynich_word, english_word in pairs[:1000]:
        escaped_voynich = (
            voynich_word.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        links.append(
            f'                <a href="https://search.naver.com/search.naver?query=보이니치+해석+{english_word}" title="{escaped_voynich} → {english_word}">{escaped_voynich}</a>,\n'
        )
    
    if links:
        # Remove comma from last link
        links[-1] = links[-1].replace(",", ".")
    
    return "".join(links)


def generate_html(data: dict) -> str:
    """Generate complete index.html"""
    
    english_words = data["english_sentence"].split()
    korean_words = data["korean_translation"].split()
    
    english_links = build_word_links(english_words)
    korean_links = build_word_links(korean_words)
    voynich_links = build_voynich_links(data["pairs"])
    english_sentence = " ".join(english_words)
    korean_translation = " ".join(korean_words)
    
    # Load GPT story if exists
    gpt_story = ""
    gpt_file = ROOT_DIR / "outputs" / "voynich_gpt_story.txt"
    if gpt_file.exists():
        with gpt_file.open("r", encoding="utf-8") as f:
            gpt_story = f.read().strip()
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="보이니치 원고의 신비로운 해석">
    <title>보이니치 원고의 신비로운 해석</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #b85c38;
            --primary-dark: #a04d2f;
            --bg-light: #f6f1e8;
            --text-dark: #333;
            --text-muted: #666;
        }}
        
        * {{
            font-family: 'Nanum Myeongjo', 'Noto Serif KR', 'Georgia', serif;
        }}
        
        body {{
            background-color: var(--bg-light);
            color: var(--text-dark);
            line-height: 1.8;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 4rem 0 3rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }}
        
        header h1 {{
            font-size: 2.8rem;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 0.8rem;
        }}
        
        header .subtitle {{
            font-size: 1.25rem;
            font-weight: 300;
            opacity: 0.98;
            letter-spacing: 0.5px;
        }}
        
        header .date {{
            font-size: 0.95rem;
            opacity: 0.90;
            margin-top: 0.8rem;
            font-style: italic;
        }}
        
        main {{
            padding: 3rem 0;
        }}
        
        .section-card {{
            background: white;
            border: none;
            border-left: 6px solid var(--primary-color);
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 2.5rem;
        }}
        
        .section-card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            transform: translateY(-4px);
        }}
        
        .section-card h2 {{
            color: var(--primary-color);
            font-size: 1.9rem;
            font-weight: 700;
            margin-bottom: 1.8rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(184, 92, 56, 0.15);
            position: relative;
        }}
        
        .section-card h2::before {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 80px;
            height: 2px;
            background: var(--primary-color);
        }}
        
        .section-card p {{
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 1rem;
        }}
        
        .word-links {{
            line-height: 2.2;
            font-size: 1rem;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 10px;
            border: 1px solid rgba(184, 92, 56, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
        }}

        .voynich-links {{
            line-height: 2.4;
            font-size: 0.9rem;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 10px;
            border: 1px solid rgba(184, 92, 56, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
        }}

        .voynich-links a {{
            border-bottom: 1px dotted var(--primary-color);
        }}

        .voynich-links a:hover {{
            background-color: rgba(184, 92, 56, 0.1);
            border-bottom: 2px solid var(--primary-color);
        }}

        .english-story {{
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid rgba(184, 92, 56, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            line-height: 2;
        }}

        .story-box {{
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid rgba(184, 92, 56, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            line-height: 2;
            color: var(--text-muted);
        }}

        /* 스크롤바 스타일 */
        .word-links::-webkit-scrollbar,
        .voynich-links::-webkit-scrollbar,
        .english-story::-webkit-scrollbar,
        .story-box::-webkit-scrollbar {{
            width: 8px;
        }}

        .word-links::-webkit-scrollbar-track,
        .voynich-links::-webkit-scrollbar-track,
        .english-story::-webkit-scrollbar-track,
        .story-box::-webkit-scrollbar-track {{
            background: rgba(184, 92, 56, 0.05);
            border-radius: 10px;
        }}

        .word-links::-webkit-scrollbar-thumb,
        .voynich-links::-webkit-scrollbar-thumb,
        .english-story::-webkit-scrollbar-thumb,
        .story-box::-webkit-scrollbar-thumb {{
            background: var(--primary-color);
            border-radius: 10px;
        }}

        .word-links::-webkit-scrollbar-thumb:hover,
        .voynich-links::-webkit-scrollbar-thumb:hover,
        .english-story::-webkit-scrollbar-thumb:hover,
        .story-box::-webkit-scrollbar-thumb:hover {{
            background: var(--primary-dark);
        }}
        
        footer {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 3rem 0 2rem;
            margin-top: 4rem;
        }}
        
        .btn-outline-primary {{
            color: var(--primary-color);
            border-color: var(--primary-color);
        }}
        
        .btn-outline-primary:hover {{
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }}
        
        a {{
            color: inherit;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        a:hover {{
            color: var(--primary-color);
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>보이니치 원고의 신비로운 해석</h1>
            <p class="subtitle">N/B 알고리즘 기반 고대 필사본 분석</p>
            <p class="date">생성일: 2026년 2월 15일</p>
        </div>
    </header>
    
    <main class="container">
        <div class="section-card card border-0 p-4" id="algorithm">
            <h2>알고리즘 설명</h2>
            <p>보이니치 원고의 신비로운 문자들을 해석하기 위한 5단계 프로세스입니다:</p>
            <ol>
                <li><strong>문자 번호화</strong> - 보이니치 원고의 각 문자에 고유한 숫자 부여</li>
                <li><strong>N/B 코드 변환</strong> - 문자의 번호를 이진수와 십진수로 변환</li>
                <li><strong>고급 알고리즘 적용</strong> - BIT_MAX_NB, BIT_MIN_NB 등의 복잡한 수학 알고리즘 사용</li>
                <li><strong>다국어 매칭</strong> - 영어, 한국어, 라틴어 등 다양한 언어의 단어와 비교</li>
                <li><strong>번역 해석</strong> - 다중 유사도 알고리즘으로 최적의 단어 선정</li>
            </ol>
        </div>


        <div class="section-card card border-0 p-4" id="voynich-original">
            <h2>보이니치 원고 원문 문자 (매칭 결과)</h2>
            <p class="mb-3">원본 보이니치 원고의 문자들을 N/B 알고리즘으로 해석한 영어 단어와 함께 표시합니다. 마우스를 올리면 매칭된 영어 단어를 확인할 수 있습니다.</p>
            <div class="word-links voynich-links">
{voynich_links}            </div>
        </div>

        <div class="section-card card border-0 p-4">
            <h2>영문 원문 (N/B 매칭 결과)</h2>
            <p class="word-links">
{english_links}            </p>
        </div>
        
        <div class="section-card card border-0 p-4">
            <h2>GPT 완성 문장</h2>
            <p>N/B 알고리즘으로 매칭된 {len(english_words)}개 영어 단어들을 연결하여 만든 연속적인 문장입니다:</p>
            <div class="english-story">{english_sentence}</div>
        </div>
        
        <div class="section-card card border-0 p-4">
            <h2>한국어 번역</h2>
            <p class="word-links">
{korean_links}            </p>
        </div>
        
        <div class="section-card card border-0 p-4">
            <h2>GPT 이야기 풀이</h2>
            <div class="story-box">{gpt_story if gpt_story else "GPT 해석이 준비 중입니다..."}</div>
        </div>
        
        <div class="section-card card border-0 p-4">
            <h2>영상 해설</h2>
            <p class="mb-3">N/B 알고리즘을 활용한 보이니치 원고 해석 과정을 영상으로 확인하세요.</p>
            <div class="ratio ratio-16x9">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/SHVFxGJlkgk?si=uir4USDGUCkNq7iM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
        </div>
        
        <div class="section-card card border-0 p-4">
            <h2>참고 자료 및 링크</h2>
            <ul class="list-unstyled">
                <li class="mb-3">
                    <a href="https://www.voynich.nu/intro.html" target="_blank" class="btn btn-outline-primary btn-sm">
                        🔗 Voynich Manuscript Official Website
                    </a>
                    <span class="ms-2">- 보이니치 원고 공식 정보</span>
                </li>
                <li class="mb-3">
                    <a href="https://www.youtube.com/watch?v=SHVFxGJlkgk" target="_blank" class="btn btn-outline-danger btn-sm">
                        🎥 YouTube: 보이니치 원고 해석 영상
                    </a>
                    <span class="ms-2">- N/B 알고리즘 설명 영상</span>
                </li>
                <li>
                    <a href="https://github.com/yoohyunseog/koreaninternet-voynich-nb" target="_blank" class="btn btn-outline-primary btn-sm">
                        💻 GitHub Repository
                    </a>
                    <span class="ms-2">- 프로젝트 소스 코드</span>
                </li>
            </ul>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p class="mb-1">© 2026 Voynich Manuscript Analysis Project</p>
            <p class="mb-0">Generated: 2026.02.15 | {len(data['pairs'])} Voynich Characters | {len(english_words)} English Words</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    
    return html


def main() -> int:
    print("=" * 50)
    print("Index.html 완전 재생성")
    print("=" * 50)
    
    print("\n데이터 로딩 중...")
    data = load_voynich_data()
    
    if not data["english_sentence"]:
        print("ERROR: 영어 문장을 찾을 수 없습니다.")
        return 1
    
    print(f"✓ {len(data['pairs'])}개 Voynich-English 쌍 로드")
    print(f"✓ {len(data['english_sentence'].split())}개 영어 단어 로드")
    print(f"✓ {len(data['korean_translation'].split())}개 한국어 단어 로드")
    
    print("\nHTML 생성 중...")
    html = generate_html(data)
    
    index_path = ROOT_DIR / "index.html"
    with index_path.open("w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✓ index.html 생성 완료: {index_path}")
    print(f"✓ 파일 크기: {len(html) / 1024:.1f} KB")
    
    print("\n✓ 완료! 모든 섹션이 최신 데이터로 업데이트되었습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
