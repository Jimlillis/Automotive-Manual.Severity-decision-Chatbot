# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Ρύθμιση Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction="Είσαι βοηθός ασφαλιστικής. Εξυπηρετείς ΜΟΝΟ Οδική Βοήθεια (RA) και Φροντίδα Ατυχήματος (AC). Μην απαντάς σε τίποτα άλλο εκτός από αυτά. Προσπάθησε να πάρεις: Όνομα, Πινακίδα, Τοποθεσία, Περιγραφή."
)

app = FastAPI()

# 🛡️ ΚΡΙΣΙΜΟ: Επιτρέπουμε στη React να μιλήσει με το FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Σε production βάλε το URL της React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str # 'user' ή 'model'
    text: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return JSONResponse(
                status_code=500,
                content={
                    "reply": "Λείπει το GEMINI_API_KEY στο backend .env.",
                    "status": "config_error"
                }
            )

        # Μετατροπή του ιστορικού στη μορφή που θέλει η Google
        formatted_history = [
            {"role": m.role, "parts": [m.text]} for m in request.history # Μετατροπή σε λίστα από dicts με 'role' και 'parts'
        ]
        
        # Έναρξη chat με το ιστορικό
        chat_session = model.start_chat(history=formatted_history)
        
        # Αποστολή του νέου μηνύματος
        response = chat_session.send_message(request.message)
        
        return {
            "reply": response.text,
            "status": "success"
        }
    except Exception as e:
        error_message = str(e)
        normalized_error = error_message.lower()
        print(f"Error: {error_message}")

        if "api key was reported as leaked" in normalized_error or "api_key_invalid" in normalized_error:
            return JSONResponse(
                status_code=403,
                content={
                    "reply": "Το Gemini API key έχει απορριφθεί (leaked/invalid). Δημιούργησε νέο key και ενημέρωσε το GEMINI_API_KEY στο .env.",
                    "status": "invalid_api_key"
                }
            )

        raise HTTPException(status_code=500, detail="Internal server error while generating AI response.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)