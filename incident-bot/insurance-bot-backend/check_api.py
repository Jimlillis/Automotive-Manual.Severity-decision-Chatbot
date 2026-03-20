import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- 1. Λίστα διαθέσιμων μοντέλων ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Διαθέσιμο: {m.name}")
except Exception as e:
    print(f"Σφάλμα στη λίστα: {e}")

print("\n--- 2. Δοκιμή με Gemini 1.5 Flash ---")
try:
    # Χρησιμοποιούμε το πλήρες όνομα αν χρειαστεί
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Πες μου 'OK' αν με ακούς.")
    print(f"✅ ΕΠΙΤΥΧΙΑ! Απάντηση: {response.text}")
except Exception as e:
    print(f"❌ ΑΠΟΤΥΧΙΑ: {e}")