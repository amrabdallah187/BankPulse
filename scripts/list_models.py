import google.generativeai as genai
import os
import sys

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY environment variable is not set.")
        sys.exit(1)

    genai.configure(api_key=api_key)

    print("\n--- ✅ Your Available Models ---")
    for m in genai.list_models():
      # Check if the model supports the 'generateContent' method needed for the chatbot
      if 'generateContent' in m.supported_generation_methods:
        print(m.name)
    print("----------------------------------")
    print("\nACTION: Copy the most recent 'gemini-pro' model name from this list.")
    print("It will likely be 'models/gemini-1.0-pro' or a similar variant.")

except Exception as e:
    print(f"❌ An error occurred: {e}")
