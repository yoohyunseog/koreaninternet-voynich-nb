# -*- coding: utf-8 -*-
"""
Add Voynich original text section to index.html
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_voynich_pairs() -> List[Tuple[str, str]]:
    """Load Voynich-English pairs from the Details section"""
    pairs = []
    sent_file = ROOT_DIR / "outputs" / "voynich_to_english_sentence.txt"
    
    if not sent_file.exists():
        return pairs
    
    with sent_file.open("r", encoding="utf-8") as f:
        in_details = False
        for line in f:
            if line.startswith("Details:"):
                in_details = True
                continue
            
            if in_details and line.strip():
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    voynich_word = parts[0]
                    english_word = parts[1]
                    pairs.append((voynich_word, english_word))
    
    return pairs


def create_voynich_section(pairs: List[Tuple[str, str]]) -> str:
    """Create HTML section with Voynich text and matches"""
    if not pairs:
        return ""
    
    links = []
    for voynich_word, english_word in pairs[:1000]:  # Limit to 1000 for readability
        escaped_voynich = (
            voynich_word.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        links.append(
            f'<a href="https://search.naver.com/search.naver?query=보이니치+해석+{english_word}" title="{escaped_voynich} → {english_word}">{escaped_voynich}</a>'
        )
    
    html = f"""
        <div class="section-card card border-0 p-4" id="voynich-original">
            <h2>보이니치 원고 원문 문자 (매칭 결과)</h2>
            <p class="mb-3">원본 보이니치 원고의 문자들을 N/B 알고리즘으로 해석한 영어 단어와 함께 표시합니다. 마우스를 올리면 매칭된 영어 단어를 확인할 수 있습니다.</p>
            <div class="word-links voynich-links">
                {",<br/>".join(links)}.
            </div>
        </div>
"""
    return html


def update_index_html(voynich_section: str, pair_count: int) -> int:
    """Update index.html with Voynich section"""
    index_path = ROOT_DIR / "index.html"
    
    if not index_path.exists():
        print(f"ERROR: {index_path} 파일을 찾을 수 없습니다.")
        return 1
    
    content = index_path.open("r", encoding="utf-8").read()
    
    # Check if section already exists and remove it
    if 'id="voynich-original"' in content:
        content = re.sub(
            r'\s*<div class="section-card card border-0 p-4" id="voynich-original">.*?</div>\s*',
            "",
            content,
            flags=re.DOTALL
        )
    
    # Find the English section and insert before it
    english_marker = '<h2>영문 원문 (N/B 매칭 결과)</h2>'
    
    if english_marker not in content:
        print("ERROR: 영문 원문 섹션을 찾을 수 없습니다.")
        return 1
    
    # Insert the Voynich section before the English section
    new_content = content.replace(
        f'        <div class="section-card card border-0 p-4">\n            {english_marker}',
        f"{voynich_section}\n        <div class=\"section-card card border-0 p-4\">\n            {english_marker}",
        1
    )
    
    # Add CSS for voynich links if not present
    if ".voynich-links" not in new_content:
        css_marker = "        .word-links {\n            line-height: 2.2;\n            font-size: 1rem;\n        }\n"
        css_block = css_marker + "\n        .voynich-links {\n            line-height: 2.4;\n            font-size: 0.9rem;\n        }\n\n        .voynich-links a {\n            border-bottom: 1px dotted var(--primary-color);\n        }\n\n        .voynich-links a:hover {\n            background-color: rgba(184, 92, 56, 0.1);\n            border-bottom: 2px solid var(--primary-color);\n        }\n"
        if css_marker in new_content:
            new_content = new_content.replace(css_marker, css_block, 1)
    
    index_path.write_text(new_content, encoding="utf-8")
    
    print(f"✓ index.html 업데이트 완료: {index_path}")
    print(f"✓ {pair_count}개의 보이니치 문자 섹션 추가")
    return 0


def main() -> int:
    print("=" * 50)
    print("보이니치 원문 문자 섹션 추가")
    print("=" * 50)
    
    pairs = load_voynich_pairs()
    if not pairs:
        print("ERROR: 보이니치-영어 매칭 쌍을 찾을 수 없습니다.")
        return 1
    
    print(f"\n✓ {len(pairs)}개의 Voynich-English 쌍 로드 완료")
    
    voynich_section = create_voynich_section(pairs)
    
    result = update_index_html(voynich_section, len(pairs))
    
    if result == 0:
        print("\n✓ 완료! index.html이 보이니치 원문 섹션으로 업데이트되었습니다.")
    
    return result


if __name__ == "__main__":
    raise SystemExit(main())
