# -*- coding: utf-8 -*-
import json
import os
import urllib.request

api_key = os.getenv("OPENAI_API_KEY")

# 실제 100단어 문장
sentence = "ox snapdragon lightning multiplication sky valley constellation multiplication ox valley earth ox lightning multiplication multiplication multiplication multiplication magnificence constellation hill multiplication crystal a nightingale hill snapdragon lightning nightingale constellation crystal valley lightning sky earth multiplication earth multiplication a multiplication a multiplication lightning crystal nightingale sky multiplication nightingale hill lightning multiplication ox nightingale multiplication lightning magnificence mountain lightning crystal nightingale constellation magnificence multiplication multiplication mountain a a ox magnificence valley sky sky multiplication nightingale multiplication multiplication earth magnificence hill multiplication multiplication ox ox multiplication multiplication multiplication multiplication multiplication multiplication multiplication magnificence sky ox earth multiplication sky snapdragon hill magnificence multiplication multiplication"

print(f"Sentence length: {len(sentence)} characters")
print(f"First 100 chars: {sentence[:100]}...")
print()

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Translate the input sentence to Korean. Keep it concise."},
        {"role": "user", "content": sentence},
    ],
    "temperature": 0.2,
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
    
    print("Calling API...")
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        parsed = json.loads(body)
        
        if "error" in parsed:
            print(f"API Error: {parsed['error']}")
        elif "choices" in parsed and parsed["choices"]:
            translation = parsed["choices"][0]["message"]["content"].strip()
            print(f"SUCCESS:")
            print(translation[:200])
        else:
            print("Unexpected response:", str(parsed)[:300])
            
except Exception as e:
    print(f"Exception: {type(e).__name__}: {str(e)[:200]}")
