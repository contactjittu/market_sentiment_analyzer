"""
Diagnostic script to check available Gemini models
Run this to see what models your API key has access to.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("Checking available Gemini models...\n")

try:
    available_models = list(genai.list_models())
    
    print(f"Found {len(available_models)} models:\n")
    
    models_with_generate = []
    for model in available_models:
        model_name = model.name
        methods = getattr(model, 'supported_generation_methods', [])
        
        print(f"Model: {model_name}")
        print(f"  Supported methods: {methods}")
        
        if 'generateContent' in methods:
            models_with_generate.append(model_name)
            print(f"  ✓ Supports generateContent")
        print()
    
    if models_with_generate:
        print(f"\n✓ Models that support generateContent ({len(models_with_generate)}):")
        for model_name in models_with_generate:
            # Try to use it
            try:
                clean_name = model_name.replace('models/', '')
                model = genai.GenerativeModel(clean_name)
                print(f"  - {clean_name} (ready to use)")
            except Exception as e:
                print(f"  - {clean_name} (error: {e})")
    else:
        print("\n⚠ No models found that support generateContent")
        
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying common model names directly...")
    
    common_models = [
        'gemini-1.5-flash-latest',
        'gemini-1.5-pro-latest',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    for model_name in common_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"✓ {model_name} - Works!")
        except Exception as e:
            print(f"✗ {model_name} - Error: {str(e)[:100]}")

