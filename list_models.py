import os
import google.generativeai as genai

# Read API key from environment
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("GOOGLE_API_KEY not found in environment. Please set it first.")
    exit()

genai.configure(api_key=api_key)

# List available models
models = genai.list_models()
for m in models:
    print(m.name)
