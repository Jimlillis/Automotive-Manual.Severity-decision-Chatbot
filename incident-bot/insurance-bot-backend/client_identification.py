import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import google.generativeai as genai
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# --- Configurations ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Supabase Setup
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- System Prompt ---
# Ζητάμε από το AI να απαντάει ΠΑΝΤΑ σε JSON format για να μπορούμε να το ελέγχουμε
SYSTEM_INSTRUCTION = """
Είσαι ο AI Πράκτορας της Ασφαλιστικής "AutoGuard". 

ΚΑΝΟΝΕΣ:
1. Αν είναι το ΠΡΩΤΟ μήνυμα, συστήσου: "Γεια σας! Είμαι ο ψηφιακός βοηθός της AutoGuard. Πώς μπορώ να σας βοηθήσω σήμερα;"
2. Αν ο χρήστης αναφέρει βλάβη (RA) ή ατύχημα (AC):
   - Αν ΔΕΝ έχεις την πινακίδα, ζήτα την ευγενικά.
3. Αν ο χρήστης λέει κάτι άσχετο, πες: "Ευχαριστώ, εξυπηρετώ μόνο Ατυχήματα και Βλάβες."

ΠΡΕΠΕΙ ΝΑ ΑΠΑΝΤΑΣ ΑΠΟΚΛΕΙΣΤΙΚΑ ΣΕ JSON ΜΟΡΦΗ: 
{
    "intent": "RA" | "AC" | "OTHER",
    "extracted_plate": "STRING_OR_NULL",
    "reply": "ΤΟ ΜΗΝΥΜΑ ΣΟΥ ΠΡΟΣ ΤΟΝ ΧΡΗΣΤΗ" 
}
"""

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=SYSTEM_INSTRUCTION
)

class ChatMessage(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)

# --- Helper Function: Database Lookup ---
def lookup_user_by_plate(plate: str):
    try:
        # Ψάχνουμε στον πίνακα cars και κάνουμε join με τον πίνακα users
        # Στο Supabase το join γίνεται αυτόματα αν υπάρχουν Foreign Keys
        result = supabase.table("cars").select("*, users(*)").eq("licence_plate", plate.upper()).execute()
        if result.data:
            return result.data[0] # Επιστρέφει το πρώτο car μαζί με το user object
        return None
    except Exception as e:
        print(f"DB Error: {e}")
        return None

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Προετοιμασία ιστορικού
        formatted_history = [{"role": m.role, "parts": [m.text]} for m in request.history]
        chat_session = model.start_chat(history=formatted_history)
        
        # 2. Κλήση Gemini
        response = chat_session.send_message(request.message)
        
        # 3. Parsing του JSON από το AI
        try: 
            # Καθαρισμός του κειμένου από τυχόν markdown (```json ...)
            clean_json = response.text.replace('```json', '').replace('```', '').strip() # Αφαιρούμε τυχόν markdown tags
            ai_data = json.loads(clean_json)
        except:
            # Fallback αν το AI δεν απαντήσει σε καθαρό JSON
            return {"reply": response.text, "status": "raw_text"}

        final_reply = ai_data.get("reply") 
        plate = ai_data.get("extracted_plate")

        # 4. Λογική Αναζήτησης στη Βάση
        if plate and plate != "NULL":
            user_data = lookup_user_by_plate(plate)
            if user_data:
                customer_name = user_data['users']['full_name']
                car_model = f"{user_data['brand']} {user_data['model']}"
                # Εμπλουτίζουμε την απάντηση
                final_reply = f"Σας βρήκα! Είστε ο/η {customer_name} με το {car_model};"
            else:
                final_reply = f"Δεν βρήκα την πινακίδα {plate} στο σύστημά μας. Μήπως την γράψατε λάθος;"

        return {
            "reply": final_reply,
            "intent": ai_data.get("intent"),
            "plate": plate,
            "status": "success"
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)