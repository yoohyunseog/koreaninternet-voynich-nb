# -*- coding: utf-8 -*-
"""
Simple test script to diagnose GPT API issues
"""

import json
import os
import urllib.request

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key present: {bool(api_key)}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print()

# Test sentence (short version first)
test_sentence = "ox snapdragon lightning sky valley constellation"

print(f"Testing with short sentence: '{test_sentence}'")
print(f"Sentence length: {len(test_sentence)} characters")
print()

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Translate the input sentence to Korean. Keep it concise."},
        {"role": "user", "content": test_sentence},
    ],
    "temperature": 0.2,
}

print("Payload structure:")
print(f"  - Model: {payload['model']}")
print(f"  - Messages: {len(payload['messages'])} messages")
print(f"  - Content length: {len(test_sentence)} chars")
print()

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

    print("Sending request to OpenAI API...")
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        print(f"Response received: {len(body)} bytes")
        print()

    parsed = json.loads(body)
    
    if "choices" in parsed and len(parsed["choices"]) > 0:
        translation = parsed["choices"][0]["message"]["content"].strip()
        print(f"✓ Translation successful!")
        print(f"  Korean: {translation}")
    else:
        print(f"✗ Unexpected response structure")
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        
except json.JSONDecodeError as e:
    print(f"✗ JSON parsing error: {e}")
except urllib.error.HTTPError as e:
    print(f"✗ HTTP error: {e.code}")
    print(f"  Error body: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
