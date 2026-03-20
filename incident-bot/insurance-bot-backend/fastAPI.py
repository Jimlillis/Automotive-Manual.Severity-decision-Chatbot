import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Φόρτωση ρυθμίσεων
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Insurance AI Bot API")

# Ρύθμιση του μοντέλου (Gemini 1.5 Flash)
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction="Είσαι ένας βοηθός ασφαλιστικής εταιρείας. Εξυπηρετείς ΜΟΝΟ περιπτώσεις Οδικής Βοήθειας (Road Assistance) και Φροντίδας Ατυχήματος (Accident Care). Αν ο χρήστης ζητήσει οτιδήποτε άλλο, απάντησε: 'Ευχαριστώ, εξυπηρετώ μόνο Ατυχήματα και Βλάβες. Εαν προκειται για μια απο τις δυο περιπτώσεις που εξυπηρετεις, απαντησε οτι θα ερθει συντομα τεχνικος στο σημειο χωρις κατι πιο συγκεκριμενο.'"
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "bot": "Gemini Flash 1.5"}

@app.post("/chat")
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        print(f"--- Νέο αίτημα: {request.message} ---")
        
        # Έλεγχος αν το API Key φορτώθηκε
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("🔴 ΣΦΑΛΜΑ: Το GEMINI_API_KEY είναι κενό στο .env!")
            return {"reply": "Internal Configuration Error: No API Key", "status": "error"}

        # Κλήση Gemini
        response = model.generate_content(request.message)
        
        # Έλεγχος αν η απάντηση μπλοκαρίστηκε από φίλτρα ασφαλείας
        if not response.parts:
            print("⚠️ Το Gemini μπλόκαρε την απάντηση (Safety Filters).")
            return {"reply": "Η ερώτηση μπλοκαρίστηκε από τα φίλτρα ασφαλείας.", "status": "blocked"}

        print(f"✅ Απάντηση Gemini: {response.text}")
        return {"reply": response.text, "status": "success"}

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}") # Αυτό θα εμφανιστεί στο Terminal σου!
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)