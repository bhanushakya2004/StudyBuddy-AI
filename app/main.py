import os
import re
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Decode and load Firebase credentials from base64 environment variable
firebase_creds_base64 = os.getenv("FIREBASE_SERVICE_ACCOUNT_BASE64")
if not firebase_creds_base64:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_BASE64 environment variable is not set")

try:
    firebase_creds_json = base64.b64decode(firebase_creds_base64).decode("utf-8")
    firebase_creds = json.loads(firebase_creds_json)
except Exception as e:
    raise ValueError(f"Error decoding FIREBASE_SERVICE_ACCOUNT_BASE64: {e}")

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize OpenAI Client (OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model for generating notes
class NotesRequest(BaseModel):
    subject: str
    main_topic: str
    sub_topic: str
    additional_details: str

# Function to clean AI response (removes Markdown symbols)
def clean_text(text):
    return re.sub(r"\*+", "", text).strip()

# Function to check if notes already exist in Firestore
def check_existing_notes(subject, topic):
    doc_ref = db.collection("Library").document(subject)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get(f"{topic}_notes", None)  # Fix: Use `.get(field, None)`
    return None

# Function to store AI-generated notes in Firestore
def store_notes_in_firebase(subject, topic, notes):
    db.collection("Library").document(subject).set({f"{topic}_notes": notes}, merge=True)

# API to generate notes using AI and store in Firebase
@app.post("/generate_notes")
async def generate_notes(request: NotesRequest):
    # Check for cached notes
    existing_notes = check_existing_notes(request.subject, request.main_topic)
    if existing_notes:
        return {"subject": request.subject, "main_topic": request.main_topic, "notes": existing_notes}

    try:
        # AI request for notes generation
        completion = client.chat.completions.create(
            model="google/gemma-3-1b-it:free",
            messages=[{
                "role": "user",
                "content": f"Generate detailed notes on {request.main_topic}. "
                           f"Focus on: {request.sub_topic}. Additional details: {request.additional_details}."
            }],
            temperature=0.7  # Optional: Adjust creativity
        )

        # Validate AI response before accessing choices
        if not completion or not completion.choices or not completion.choices[0].message:
            raise HTTPException(status_code=500, detail="AI response invalid or empty")

        # Extract and clean AI response
        notes = clean_text(completion.choices[0].message.content)

        # Store notes in Firebase
        store_notes_in_firebase(request.subject, request.main_topic, notes)
        return {"subject": request.subject, "main_topic": request.main_topic, "notes": notes}

    except Exception as e:
        print(f"Error generating notes: {e}")  # Debugging logs
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

# API to fetch notes from Firebase
@app.get("/fetch_notes")
async def fetch_notes(subject: str, topic: str):
    notes = check_existing_notes(subject, topic)
    return {"subject": subject, "main_topic": topic, "notes": notes or "No notes available"}

# Run FastAPI on Cloud Run-compatible port 8080
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))  # Ensure correct Cloud Run port
    uvicorn.run(app, host="0.0.0.0", port=port)
