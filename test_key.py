# test_key.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Force load .env
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")

print("\n--- 🔍 GROQ API KEY DIAGNOSTIC ---")

if not api_key:
    print("❌ ERROR: GROQ_API_KEY was NOT found in your .env file!")
    print("Check if your file is named '.env' and NOT '.env.txt'.")
else:
    # Print key details securely
    print(f"✅ Key Found: '{api_key[:8]}...{api_key[-4:]}'")
    print(f"📏 Key Length: {len(api_key)} characters")
    
    # Check formatting errors
    if '"' in api_key or "'" in api_key:
        print("⚠️ WARNING: Your key contains QUOTES! Remove quotes from your .env file.")
    if api_key.startswith(" ") or api_key.endswith(" "):
        print("⚠️ WARNING: Your key contains EXTRA SPACES! Remove spaces around '=' in .env.")
    if not api_key.startswith("gsk_"):
        print(f"⚠️ WARNING: Key starts with '{api_key[:4]}'. Groq keys MUST start with 'gsk_'.")

    # 2. Test direct connection to Groq API
    print("\n📡 Testing connection to Groq Cloud...")
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Hello, respond with 'API KEY WORKING'"}],
            max_tokens=10
        )
        print("🎉 SUCCESS! Groq API Response:", response.choices[0].message.content.strip())
    except Exception as e:
        print("❌ API CALL FAILED:")
        print(e)

print("-----------------------------------\n")