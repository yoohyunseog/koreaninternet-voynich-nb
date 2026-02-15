# -*- coding: utf-8 -*-
"""
Generate GPT story interpretation and update index.html
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Dict

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_content() -> Dict[str, str]:
    """Load Korean translation and English sentence from voynich_to_english_sentence.txt"""
    result = {
        "korean_translation": "",
        "english_sentence": "",
    }
    
    sent_file = ROOT_DIR / "outputs" / "voynich_to_english_sentence.txt"
    if sent_file.exists():
        with sent_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            in_sentence = False
            in_translation = False
            translation_lines = []
            for line in lines:
                if line.startswith("Sentence:"):
                    in_sentence = True
                    in_translation = False
                elif line.startswith("GPT Translation"):
                    in_sentence = False
                    in_translation = True
                elif line.startswith("Details:"):
                    break
                elif in_sentence and line.strip():
                    result["english_sentence"] = line.strip()
                elif in_translation and line.strip():
                    translation_lines.append(line.strip())

            if translation_lines:
                result["korean_translation"] = " ".join(translation_lines)
    
    return result


def generate_story_with_gpt(korean_translation: str, english_sentence: str) -> str:
    """Generate story interpretation using GPT"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "GPT 해석 생성 실패: API 키가 없습니다."
    
    prompt = f"""당신은 신비로운 고대 원고를 해석하는 역사가이자 철학자입니다.

다음은 보이니치 원고를 N/B 알고리즘으로 매칭한 한국어 단어들입니다:

{korean_translation}

원래 영어 매칭 결과:
{english_sentence}

이 단어들의 의미를 연결하여 보이니치 원고가 담고 있을 수 있는 신비로운 이야기, 철학적 의미, 또는 은유적 해석을 한국어로 3-4문단으로 작성해주세요.

요구사항:
1. 신비롭고 깊이 있는 톤
2. 단어들의 연결성을 찾아 의미있는 서사 구성
3. 역사적, 철학적, 또는 영적 해석 포함
4. 아름답고 우아한 한국어 표현
5. 총 3-4문단, 각 문단은 3-4줄
6. 최소 1000자 이상
7. HTML tag 사용 금지, 순수 텍스트만

이야기만 출력하세요. 설명은 제외."""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a mystical interpreter of ancient manuscripts. Generate poetic and philosophical interpretations in Korean."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8,
        "max_tokens": 1500,
    }
    
    try:
        print("GPT가 이야기 풀이를 생성 중...", end=" ", flush=True)
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
                story = parsed["choices"][0]["message"]["content"].strip()
                print("✓")
                return story
        print("(실패)")
    except Exception as e:
        print(f"(오류: {type(e).__name__})")
    
    return "GPT 해석 생성 실패"


def update_index_html(korean_translation: str, story: str, english_sentence: str) -> int:
    """Update index.html with English/Korean lists and the GPT story"""
    index_path = ROOT_DIR / "index.html"

    if not index_path.exists():
        print(f"ERROR: {index_path} 파일을 찾을 수 없습니다.")
        return 1

    with index_path.open("r", encoding="utf-8") as f:
        content = f.read()

    def build_links(words: list[str]) -> str:
        links = []
        for word in words:
            clean = word.strip()
            if not clean:
                continue
            links.append(
                f'<a href="https://search.naver.com/search.naver?query=\ubcf4\uc774\ub2c8\uce58+\ud574\uc11d+{clean}">{clean}</a>'
            )
        return ",\n                ".join(links) + "."

    english_words = english_sentence.split()
    korean_words = korean_translation.split()
    english_links = build_links(english_words)
    korean_links = build_links(korean_words)

    patterns = {
        "english_links": r'(<h2>\uc601\ubb38 \uc6d0\ubb38 .*?<p class="word-links">)(.*?)(</p>)',
        "english_story": r'(<div class="english-story">)(.*?)(</div>)',
        "korean_links": r'(<h2>\ud55c\uad6d\uc5b4 \ubc88\uc5ed</h2>\s*<p class="word-links">)(.*?)(</p>)',
        "story_box": r'(<div class="story-box">)(.*?)(</div>)',
    }

    def replace_block(src: str, pattern: str, replacement: str, label: str) -> str:
        if not re.search(pattern, src, re.DOTALL):
            print(f"ERROR: {label} 영역을 찾을 수 없습니다.")
            raise ValueError(label)
        return re.sub(pattern, replacement, src, flags=re.DOTALL, count=1)

    try:
        new_content = replace_block(
            content,
            patterns["english_links"],
            f"\\1\n                {english_links}\n            \\3",
            "영문 링크",
        )
        new_content = replace_block(
            new_content,
            patterns["english_story"],
            f"\\1{english_sentence}\\3",
            "영문 문장",
        )
        new_content = replace_block(
            new_content,
            patterns["korean_links"],
            f"\\1\n                {korean_links}\n            \\3",
            "한국어 링크",
        )
        new_content = re.sub(
            patterns["story_box"],
            f"\\1{story}\\3",
            new_content,
            flags=re.DOTALL,
            count=1,
        )
    except ValueError:
        return 1

    with index_path.open("w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ index.html 업데이트 완료: {index_path}")
    return 0


def main() -> int:
    print("=" * 50)
    print("보이니치 원고 GPT 이야기 풀이 생성")
    print("=" * 50)
    
    print("\n파일 로딩...")
    data = load_content()
    
    if not data["korean_translation"]:
        print("ERROR: 한국어 번역을 찾을 수 없습니다.")
        return 1
    
    print(f"✓ 한국어 번역 로드: {len(data['korean_translation'].split())}개 단어")
    print(f"✓ 영어 문장 로드: {len(data['english_sentence'].split())}개 단어")
    
    # Generate story with GPT
    story = generate_story_with_gpt(data["korean_translation"], data["english_sentence"])
    
    if "실패" in story:
        print(story)
        return 1
    
    print(f"\n생성된 이야기 풀이:")
    print("-" * 50)
    print(story)
    print("-" * 50)
    
    # Update index.html
    print("\nindex.html 업데이트 중...")
    result = update_index_html(data["korean_translation"], story, data["english_sentence"])
    
    if result == 0:
        print("\n✓ 완료! index.html이 한국어 번역과 GPT 이야기 풀이로 업데이트되었습니다.")
    
    return result


if __name__ == "__main__":
    raise SystemExit(main())
