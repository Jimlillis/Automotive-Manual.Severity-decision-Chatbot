import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv

# Φόρτωση των μεταβλητών περιβάλλοντος από το αρχείο .env
load_dotenv()

# Αρχικοποίηση του FastAPI App
app = FastAPI(title="AutoAssist Data API", description="API για τα δεδομένα χρηστών και οχημάτων")

# --- ΡΥΘΜΙΣΗ CORS ---
# Απαραίτητο για να επιτρέπει στη React (που τρέχει συνήθως στο port 5173 ή 3000) 
# να ζητάει δεδομένα από αυτόν τον server χωρίς να μπλοκάρεται από τον browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], # Ή βάλε ["*"] για να τα επιτρέπεις όλα προσωρινά
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ΡΥΘΜΙΣΗ SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Δεν βρέθηκαν τα κλειδιά του Supabase στο αρχείο .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Το Data API τρέχει κανονικά!"}


@app.get("/api/users")
def get_all_users():
    """Επιστρέφει όλους τους χρήστες για τη σελίδα του Login"""
    try:
        response = supabase.table("users").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Σφάλμα κατά την ανάκτηση χρηστών: {str(e)}")


@app.get("/api/dashboard-data/{user_id}")
def get_dashboard_data(user_id: int):
    """Επιστρέφει τα στοιχεία του χρήστη και τα οχήματά του για το Dashboard"""
    try:
        # 1. Φέρνουμε τα στοιχεία του χρήστη
        user_response = supabase.table("users").select("*").eq("user_id", user_id).execute()
        
        # Αν η λίστα είναι άδεια, σημαίνει ότι δεν υπάρχει ο χρήστης
        if not user_response.data:
            raise HTTPException(status_code=404, detail="Ο χρήστης δεν βρέθηκε")
            
        # Παίρνουμε το πρώτο (και μοναδικό) στοιχείο της λίστας
        user_data = user_response.data[0] # Επιστρέφει το user object με όλα τα πεδία του, π.χ. {"user_id": 1, "name": "Vicky", ...}
        
        # 2. Φέρνουμε τα αυτοκίνητα του χρήστη
        cars_response = supabase.table("cars").select("*").eq("owner_id", user_id).execute()
        
        return {
            "user": user_data,
            "cars": cars_response.data
        }
        
    except HTTPException:
        raise # Αναπαράγουμε το δικό μας 404 error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Σφάλμα βάσης δεδομένων: {str(e)}")