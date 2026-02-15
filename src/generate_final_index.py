# -*- coding: utf-8 -*-
"""
Generate final index.html using GPT AI based on voynich_interpretation.html content.

This script:
1. Reads voynich_interpretation.html and voynich_to_english_sentence.txt
2. Uses GPT to generate a complete, beautiful HTML page with full narrative
3. Outputs complete index.html
"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Dict

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_files() -> Dict[str, str]:
    """Load content from interpretation files"""
    result = {
        "korean_translation": "",
        "english_sentence": "",
        "sentence_story": "",  # Full English sentence story
    }
    
    # Load content from voynich_to_english_sentence.txt
    sent_file = ROOT_DIR / "outputs" / "voynich_to_english_sentence.txt"
    if sent_file.exists():
        with sent_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            in_sentence = False
            in_translation = False
            for i, line in enumerate(lines):
                if line.startswith("Sentence:"):
                    in_sentence = True
                    in_translation = False
                elif line.startswith("GPT Translation"):
                    in_sentence = False
                    in_translation = True
                elif line.startswith("Details:"):
                    break
                elif in_sentence and line.strip():
                    result["sentence_story"] = line.strip()  # Full story from file
                    result["english_sentence"] += line.strip() + " "
                elif in_translation and line.strip():
                    result["korean_translation"] += line.strip() + " "
    
    result["korean_translation"] = result["korean_translation"].strip()
    result["english_sentence"] = result["english_sentence"].strip()
    
    return result


def generate_html_with_gpt(korean_translation: str, english_sentence: str, sentence_story: str = "") -> str:
    """Generate complete HTML using GPT AI"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return generate_fallback_html(korean_translation, english_sentence, sentence_story)
    
    korean_preview = korean_translation[:100]
    
    prompt = f"""당신은 아름다운 웹 페이지를 만드는 디자이너입니다.

다음 보이니치 원고 해석을 바탕으로 완전하고 아름다운 HTML5 페이지를 생성해주세요:

영어 원문: {english_sentence}
한국어 해석: {korean_translation}

요구사항:
1. <!DOCTYPE html> 부터 시작하는 완전한 HTML5 페이지 생성
2. 메타데이터, 스타일, 본문 모두 포함
3. 한국어 제목: "보이니치 원고의 신비로운 해석"
4. 부제: "N/B 알고리즘 엔진을 통한 AI 해석"
5. 날짜: 2026년 2월 15일 추가
6. 따뜻하고 신비로운 색상 사용 (배경: #f6f1e8, 강조: #b85c38)
7. Nanum Myeongjo 폰트 사용
8. 섹션:
   - 알고리즘 설명 (BIT_MAX_NB, BIT_MIN_NB, 매칭 알고리즘, 중복 방지, GPT 번역)
   - 영문 원문 (매칭된 100개 영어 단어)
   - GPT 완성 문장 (전체 이야기)
   - GPT 이야기 풀이 (한국어 해석)
   - 참고 자료 및 링크
9. 각 키워드에 대해 네이버 검색 링크 추가 (query=보이니치+해석+키워드)
10. 푸터에 저작권 정보 포함: © 2026 Voynich Manuscript Analysis
11. 반응형 디자인으로 모바일에서도 잘 보이도록

HTML 코드만 출력하세요. 설명이나 다른 텍스트는 제외."""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert HTML5 developer creating beautiful, semantic web pages. Generate complete, valid HTML5 code with proper structure, styling, and content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
    }
    
    try:
        print("Calling GPT to generate final HTML...", end=" ", flush=True)
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            if "choices" in parsed and parsed["choices"]:
                html_content = parsed["choices"][0]["message"]["content"].strip()
                # Remove markdown code block markers if present
                if html_content.startswith("```html"):
                    html_content = html_content[7:]
                if html_content.endswith("```"):
                    html_content = html_content[:-3]
                html_content = html_content.strip()
                print("✓")
                return html_content
        print("(failed)")
    except Exception as e:
        print(f"(Error: {type(e).__name__})")
    
    return generate_fallback_html(korean_translation, english_sentence, sentence_story)


def generate_fallback_html(korean_translation: str, english_sentence: str, sentence_story: str = "") -> str:
    """Fallback HTML if GPT fails"""
    from datetime import datetime
    
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    # Build Korean narrative with links
    korean_words = korean_translation.split()
    korean_with_links = ""
    for word in korean_words:
        korean_with_links += f'<a href="https://search.naver.com/search.naver?query=보이니치+해석+{word}">{word}</a> '
    
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>보이니치 원고의 신비로운 해석</title>
    <style>
        :root {{
            color-scheme: light;
            --bg: #f6f1e8;
            --ink: #2d2a26;
            --muted: #6a6257;
            --accent: #b85c38;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: "Nanum Myeongjo", "Noto Serif KR", serif;
            background: var(--bg);
            color: var(--ink);
            line-height: 1.8;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 24px;
        }}
        header {{
            text-align: center;
            padding: 20px;
            background-color: var(--accent);
            color: white;
            border-radius: 10px;
            margin-bottom: 40px;
        }}
        h1 {{
            font-size: 36px;
            margin-bottom: 12px;
        }}
        header p {{
            font-size: 0.9em;
            margin-top: 10px;
        }}
        section {{
            margin: 30px 0;
            padding: 20px;
            background: white;
            border: 2px solid var(--accent);
            border-radius: 10px;
        }}
        h2 {{
            font-size: 24px;
            margin-bottom: 16px;
            color: var(--accent);
        }}
        section p {{
            margin: 12px 0;
            line-height: 2;
        }}
        ul {{
            margin-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
            line-height: 1.6;
        }}
        a {{
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid var(--accent);
        }}
        a:hover {{
            opacity: 0.8;
        }}
        .story {{
            font-style: italic;
            background-color: #f0f0f0;
            padding: 12px;
            border-left: 4px solid var(--accent);
        }}
        footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 24px;
            border-top: 1px solid var(--muted);
            color: var(--muted);
            font-size: 14px;
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            section {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>보이니치 원고의 신비로운 해석</h1>
            <p>N/B 알고리즘 엔진을 통한 AI 해석</p>
            <p style="font-size: 0.85em; margin-top: 5px; opacity: 0.9;">작성일: {today}</p>
        </header>
        
        <section>
            <h2>알고리즘 설명</h2>
            <p>
                이 프로젝트는 <strong>N/B 코드 알고리즘</strong>을 사용하여 보이니치 원고를 해석합니다:
            </p>
            <ul>
                <li><strong>BIT_MAX_NB</strong>: 각 문자를 유니코드 값으로 변환 후, 가중치를 적용하여 전방향으로 누적</li>
                <li><strong>BIT_MIN_NB</strong>: 동일한 방식으로 후방향으로 누적</li>
                <li><strong>매칭 알고리즘</strong>: 보이니치 단어의 (BIT_MAX_NB, BIT_MIN_NB) 값과 가장 가까운 영어 단어를 탐색</li>
                <li><strong>중복 방지</strong>: 최근 5개 단어에 패널티를 적용하여 단어의 다양성 확보</li>
                <li><strong>GPT 번역</strong>: 매칭된 영어 단어를 개별적으로 한국어로 번역</li>
            </ul>
            <p>
                이를 통해 보이니치 원고의 1495개 영어 데이터베이스와의 무작위 숫자 비교가 아닌, 
                수학적 거리 함수를 기반으로 한 의미 있는 해석을 제공합니다.
            </p>
        </section>
        
        <section>
            <h2>영문 원문</h2>
            <p>
                N/B 알고리즘으로 매칭된 100개 영어 단어들입니다.
                각 단어는 보이니치 원문과 수학적으로 가장 유사한 영어 단어입니다.
            </p>
            <p class="story">"{english_sentence}"</p>
        </section>
        
        <section>
            <h2>GPT 완성 문장</h2>
            <p>
                N/B 알고리즘으로 매칭된 100개 영어 단어들을 연결하여 만든 연속적인 문장입니다.
                이는 무의미한 보이니치 원문을 의미 있는 영어로 변환한 결과입니다.
            </p>
            <p class="story">"{sentence_story}"</p>
        </section>
        
        <section>
            <h2>GPT 이야기 풀이</h2>
            <p>
                보이니치 원고의 신비로운 해석을 한국어로 풀어낸 이야기입니다.
                각 단어들이 담고 있는 의미를 연결하여 하나의 서사적 맥락을 형성합니다.
            </p>
            <p style="line-height: 2; font-size: 0.95em;">
                {korean_with_links}
            </p>
        </section>
        
        <section>
            <h2>참고 자료 및 링크</h2>
            <ul>
                <li><a href="https://www.voynich.nu/intro.html" target="_blank">Voynich Manuscript Official Website</a> - 보이니치 원고 공식 정보</li>
                <li><a href="file:///E:/Ai%20project/%EB%B3%B4%EC%9D%B4%EB%8B%88%EC%B9%98/[xn--3e0bx5eku0am2irhf.xn--3e0b707e]%202026.02.15%E2%80%94%EA%B5%AD%EC%9D%B8%ED%84%B0%EB%84%B7.%ED%95%9C%EA%B5%AD%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EA%B4%80%EB%A6%AC%20%EB%B3%B4%EA%B3%A0%EC%84%9C%20ver%200.1.mht" target="_blank">도메인 관리 보고서</a> - 프로젝트 상세 보고</li>
            </ul>
        </section>
        
        <footer>
            <p>© 2026 Voynich Manuscript Analysis Project</p>
            <p>Generated: {today} | All Rights Reserved</p>
        </footer>
    </div>
</body>
</html>"""


def main() -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate final index.html using GPT AI")
    parser.add_argument("--output", default="index.html", help="Output HTML file")
    parser.add_argument("--use-gpt", action="store_true", default=True, help="Use GPT for generation")
    args = parser.parse_args()
    
    print("Loading content...")
    data = load_files()
    
    if not data["korean_translation"]:
        print("ERROR: No Korean translation found")
        return 1
    
    print(f"✓ Loaded {len(data['korean_translation'].split())} Korean words")
    print(f"✓ Loaded English sentence with {len(data['english_sentence'].split())} words")
    
    # Generate HTML
    if args.use_gpt:
        html_content = generate_html_with_gpt(data["korean_translation"], data["english_sentence"], data["sentence_story"])
    else:
        html_content = generate_fallback_html(data["korean_translation"], data["english_sentence"], data["sentence_story"])
    
    # Save
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT_DIR / output_path
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(html_content)
    
    print(f"✓ index.html generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
