import os
import re
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize Firebase
cred = credentials.Certificate("firebase_service_account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize OpenAI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for testing in ThunderClient/Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class NotesRequest(BaseModel):
    subject: str
    main_topic: str
    sub_topic: str
    additional_details: str

# Function to clean AI response
def clean_text(text):
    return re.sub(r"\*+", "", text).strip()  # Remove *, ** symbols

# Function to fetch existing notes from Firebase
def check_existing_notes(subject, topic):
    doc_ref = db.collection("Library").document(subject)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get(f"{topic}_notes")
    return None

# Function to store AI-generated notes in Firebase
def store_notes_in_firebase(subject, topic, notes):
    db.collection("Library").document(subject).set({f"{topic}_notes": notes}, merge=True)

# AI Notes Generation API
@app.post("/generate_notes")
async def generate_notes(request: NotesRequest):
    # Check if notes exist
    existing_notes = check_existing_notes(request.subject, request.main_topic)
    if existing_notes:
        return {"subject": request.subject, "main_topic": request.main_topic, "notes": existing_notes}

    try:
        # Call AI model to generate notes
        completion = client.chat.completions.create(
            model="google/gemma-3-1b-it:free",
            messages=[{"role": "user", "content": f"Generate detailed notes on {request.main_topic}. Focus on: {request.sub_topic}. Additional details: {request.additional_details}."}]
        )

        # Extract and clean response
        notes = clean_text(completion.choices[0].message.content)
        
        # Store in Firebase
        store_notes_in_firebase(request.subject, request.main_topic, notes)
        return {"subject": request.subject, "main_topic": request.main_topic, "notes": notes}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

# Fetch API for Notes
@app.get("/fetch_notes")
async def fetch_notes(subject: str, topic: str):
    notes = check_existing_notes(subject, topic)
    return {"subject": subject, "main_topic": topic, "notes": notes or "No notes available"}
