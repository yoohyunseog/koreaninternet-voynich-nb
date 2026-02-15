# -*- coding: utf-8 -*-
"""
Generate HTML page from voynich_to_english_sentence.txt using GPT AI.

This script:
1. Reads the English sentence and Korean translation from voynich_to_english_sentence.txt
2. Uses GPT to generate a narrative interpretation for each word/phrase
3. Adds Naver search links with contextual queries (full summary + keyword)
4. Outputs formatted HTML
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Dict

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_voynich_translation(filepath: str) -> Dict[str, str]:
    """Load English sentence and Korean translation from file"""
    file_path = Path(filepath)
    if not file_path.is_absolute():
        file_path = ROOT_DIR / file_path
    
    with file_path.open("r", encoding="utf-8") as handle:
        content = handle.read()
    
    # Parse the file
    lines = content.split("\n")
    result = {
        "english_sentence": "",
        "korean_translation": "",
        "details": []
    }
    
    in_sentence = False
    in_translation = False
    in_details = False
    
    for i, line in enumerate(lines):
        if line.startswith("Sentence:"):
            in_sentence = True
            in_translation = False
            in_details = False
            continue
        elif line.startswith("GPT Translation"):
            in_sentence = False
            in_translation = True
            in_details = False
            continue
        elif line.startswith("Details:"):
            in_sentence = False
            in_translation = False
            in_details = True
            continue
        
        if in_sentence and line.strip():
            result["english_sentence"] += line.strip() + " "
        elif in_translation and line.strip():
            result["korean_translation"] += line.strip() + " "
        elif in_details and line.strip() and "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 2:
                result["details"].append({
                    "voynich": parts[0].strip(),
                    "english": parts[1].strip(),
                    "score": float(parts[2]) if len(parts) > 2 else 0
                })
    
    result["english_sentence"] = result["english_sentence"].strip()
    result["korean_translation"] = result["korean_translation"].strip()
    
    return result


def summarize_with_gpt(text: str, focus: str = "보이니치") -> str:
    """Generate a concise summary using GPT (max 30 chars for search query)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return focus
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a concise Korean writer. Generate a very brief description (under 15 Korean characters) that captures the essence. Reply with ONLY the Korean description, no explanation."
            },
            {
                "role": "user",
                "content": f"Summarize in Korean: {text}"
            }
        ],
        "temperature": 0.3,
        "max_tokens": 30,
    }
    
    try:
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
        
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            if "choices" in parsed and parsed["choices"]:
                summary = parsed["choices"][0]["message"]["content"].strip()
                return summary[:15]
    except Exception as e:
        pass
    
    return focus


def generate_narrative_with_gpt(korean_words: List[str], context: str = "") -> str:
    """Generate a poetic narrative for the Korean words using GPT"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        words_str = " ".join(korean_words[:20])
        return f"이 구절은 {words_str}을(를) 담고 있습니다."
    
    words_str = " ".join(korean_words[:15])  # Use first 15 words
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a poetic Korean writer interpreting ancient mystical texts. Generate a 2-3 sentence narrative description. Write in Korean only."
            },
            {
                "role": "user",
                "content": f"Create a poetic interpretation of these words: {words_str}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100,
    }
    
    try:
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
        
        print(f"  > Calling GPT for: {words_str[:40]}...", end=" ", flush=True)
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            if "choices" in parsed and parsed["choices"]:
                narrative = parsed["choices"][0]["message"]["content"].strip()
                print("✓")
                return narrative
        print("(no response)")
    except urllib.error.HTTPError as e:
        print(f"(HTTP {e.code})")
        try:
            error_body = e.read().decode("utf-8")
            print(f"  Error: {error_body[:100]}")
        except:
            pass
    except urllib.error.URLError as e:
        print(f"(Network error: {str(e)[:50]})")
    except KeyboardInterrupt:
        print("(cancelled by user)")
        raise
    except (json.JSONDecodeError, ValueError, OSError, Exception) as e:
        print(f"(Error: {type(e).__name__})")
    
    # Fallback to simple interpretation
    fallback = f"이 구절은 {words_str}의 신비로운 의미를 담고 있으며, 보이니치 원고의 중심 주제를 반영한다."
    return fallback


def build_html_with_links(data: Dict, narratives: List[str] = None, chunks: List[List[str]] = None) -> str:
    """Build HTML with Naver search links for each narrative section"""
    korean_words = data["korean_translation"].split()
    
    # If narratives not provided, generate them
    if narratives is None:
        chunk_size = 12
        chunks = [
            korean_words[i:i + chunk_size]
            for i in range(0, len(korean_words), chunk_size)
        ]
        narratives = []
        for chunk in chunks:
            narrative = generate_narrative_with_gpt(chunk)
            narratives.append(narrative)
    
    if chunks is None:
        chunk_size = 12
        chunks = [
            korean_words[i:i + chunk_size]
            for i in range(0, len(korean_words), chunk_size)
        ]
    
    # Build HTML
    html_content = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Voynich Interpretation - 보이니치 해석</title>
    <style>
      :root {{
        color-scheme: light;
        --bg: #f6f1e8;
        --ink: #2d2a26;
        --muted: #6a6257;
        --accent: #b85c38;
      }}
      body {{
        margin: 0;
        font-family: "Nanum Myeongjo", "Noto Serif KR", serif;
        background: var(--bg);
        color: var(--ink);
        line-height: 1.8;
      }}
      .wrap {{
        max-width: 900px;
        margin: 0 auto;
        padding: 48px 24px 72px;
      }}
      h1 {{
        font-size: 28px;
        margin: 0 0 12px;
      }}
      .tagline {{
        color: var(--muted);
        margin-bottom: 24px;
      }}
      .narrative-section {{
        margin: 32px 0;
        padding: 20px;
        background: rgba(184, 92, 56, 0.05);
        border-left: 4px solid var(--accent);
      }}
      .narrative-section p {{
        margin: 12px 0;
      }}
      .search-link {{
        display: inline-block;
        margin-top: 12px;
        padding: 8px 12px;
        background: var(--accent);
        color: white;
        text-decoration: none;
        border-radius: 4px;
        font-size: 14px;
      }}
      .search-link:hover {{
        opacity: 0.9;
      }}
      .keywords {{
        color: var(--muted);
        font-size: 12px;
        margin-top: 8px;
      }}
      footer {{
        margin-top: 48px;
        padding-top: 24px;
        border-top: 1px solid var(--muted);
        color: var(--muted);
        font-size: 14px;
        text-align: center;
      }}
    </style>
  </head>
  <body>
    <main class="wrap">
      <h1>Voynich Interpretation</h1>
      <div class="tagline">보이니치 원고의 신비로운 해석</div>

      <section>
        <h2>해석 내용</h2>
"""
    
    # Add narrative sections with search links
    for i, narrative in enumerate(narratives):
        if i < len(chunks):
            chunk = chunks[i]
            keywords = " ".join(chunk[:3])  # First 3 words as keywords
            
            # Generate search query summary
            summary = summarize_with_gpt(narrative)
            search_query = f"보이니치 해석 {summary}"
            
            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query, safe='')
            
            html_content += f"""
      <div class="narrative-section">
        <p>{narrative}</p>
        <div class="keywords">키워드: {keywords}</div>
        <a href="https://search.naver.com/search.naver?query={encoded_query}" 
           target="_blank" rel="noopener noreferrer" class="search-link">
          네이버 검색 →
        </a>
      </div>
"""
    
    # Add footer with original data
    english_preview = data['english_sentence'][:200] + ("..." if len(data['english_sentence']) > 200 else "")
    korean_preview = data['korean_translation'][:200] + ("..." if len(data['korean_translation']) > 200 else "")
    
    html_content += f"""
      <section style="margin-top: 48px;">
        <h2>원본 데이터</h2>
        <p><strong>영어 문장:</strong><br>{english_preview}</p>
        <p><strong>한국어 번역:</strong><br>{korean_preview}</p>
      </section>

      <footer>
        <p>© 2026 Voynich Manuscript Analysis | Generated with GPT AI</p>
        <p>Data source: outputs/voynich_to_english_sentence.txt</p>
      </footer>
    </main>
  </body>
</html>
"""
    
    return html_content


def build_html_with_links_v2(data: Dict, narratives: List[str], chunks: List[List[str]]) -> str:
    """Alias for backward compatibility"""
    return build_html_with_links(data, narratives, chunks)


def main() -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate HTML from Voynich translation using GPT AI")
    parser.add_argument("--input", default="outputs/voynich_to_english_sentence.txt", help="Input translation file")
    parser.add_argument("--output", default="voynich_interpretation.html", help="Output HTML file")
    parser.add_argument("--use-gpt", action="store_true", help="Use GPT for narrative generation (requires API)")
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_voynich_translation(args.input)
    
    if not data["korean_translation"]:
        print("ERROR: No Korean translation found in file")
        return 1
    
    word_count = len(data["korean_translation"].split())
    print(f"Loaded {word_count} words")
    
    # Split into chunks
    korean_words = data["korean_translation"].split()
    chunk_size = 12
    chunks = [
        korean_words[i:i + chunk_size]
        for i in range(0, len(korean_words), chunk_size)
    ]
    
    narratives = []
    
    if args.use_gpt:
        print(f"Generating narrative with GPT AI ({len(chunks)} sections)...")
        try:
            for i, chunk in enumerate(chunks, 1):
                print(f"[{i}/{len(chunks)}]", end=" ")
                narrative = generate_narrative_with_gpt(chunk)
                narratives.append(narrative)
                # Add small delay between requests to avoid rate limiting
                if i < len(chunks):
                    time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n(Cancelled by user)")
            if len(narratives) == 0:
                print("No narratives generated, using default interpretations")
                narratives = None
        print(f"\n✓ Generated {len(narratives)} narratives")
    
    # If no narratives generated, use defaults
    if not narratives:
        print("Generating default narratives...")
        narratives = [
            f"이 구절은 {' '.join(chunk[:3])}의 신비로운 의미를 담고 있다."
            for chunk in chunks
        ]
        print(f"✓ Generated {len(narratives)} default narratives")
    
    # Generate HTML
    print("Building HTML...")
    html_content = build_html_with_links(data, narratives, chunks[:len(narratives)])
    
    # Save
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT_DIR / output_path
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(html_content)
    
    print(f"✓ HTML generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
