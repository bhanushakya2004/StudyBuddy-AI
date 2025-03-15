

# **StudyBuddy AI - AI-Powered Notes Generator** 📚🤖  

**StudyBuddy AI** is a FastAPI-based service that generates **detailed engineering notes** using AI. The generated notes are stored in **Firebase Firestore** to minimize API load and provide quick access to previously generated content.  

## **✨ Features**  
✅ AI-generated detailed notes based on subject and topic  
✅ Firebase caching to avoid redundant API calls  
✅ FastAPI backend for high performance  
✅ Environment variable support for API keys  
✅ CORS-enabled for easy frontend integration  

---

## **📂 Project Structure**  
```
StudyBuddy-AI/
│── firebase_service_account.json   # (DO NOT COMMIT - Add to .gitignore)
│── .env                            # Environment variables (API keys, Firebase config)
│── main.py                         # FastAPI backend
│── requirements.txt                 # Python dependencies
│── .gitignore                      # Ignore sensitive files
│── README.md                       # Project documentation
```

---

## **🚀 Setup & Installation**  

### **🔹 Prerequisites**  
Ensure you have the following installed:  
- Python 3.8+  
- Firebase Firestore account  
- OpenRouter API key  

---

### **🔹 1. Clone the Repository**  
```bash
git clone https://github.com/bhanushakya2004/StudyBuddy-AI.git
cd StudyBuddy-AI
```

---

### **🔹 2. Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### **🔹 3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

### **🔹 4. Setup Environment Variables**  
Create a `.env` file and add:  
```
OPENROUTER_API_KEY=your_openrouter_api_key
```

---

### **🔹 5. Add Firebase Credentials**  
- **Do NOT commit `firebase_service_account.json` to GitHub.**  
- Download your **Firebase service account JSON** from Firebase Console.  
- Save it as `firebase_service_account.json` in the root folder.  

---

### **🔹 6. Run the FastAPI Server**  
```bash
uvicorn main:app --reload
```
The API will be available at:  
🚀 **http://127.0.0.1:8000**

---

## **🛠️ API Endpoints**  

### **1️⃣ Generate Notes**  
**URL:** `/generate_notes`  
**Method:** `POST`  
**Body (JSON):**  
```json
{
  "subject": "Computer Science",
  "main_topic": "Data Structures",
  "sub_topic": "Binary Trees",
  "additional_details": "Explain tree traversal techniques"
}
```
**Response:**  
```json
{
  "subject": "Computer Science",
  "main_topic": "Data Structures",
  "notes": "Binary Trees are hierarchical data structures..."
}
```

---

### **2️⃣ Fetch Stored Notes**  
**URL:** `/fetch_data`  
**Method:** `GET`  
**Query Parameters:**  
```
subject=Computer Science  
topic=Data Structures  
data_type=notes  
```
**Response:**  
```json
{
  "subject": "Computer Science",
  "main_topic": "Data Structures",
  "data": "Binary Trees are hierarchical data structures..."
}
```

---

## **🌟 Contributing**  
Feel free to fork this repository, improve it, and submit a pull request. 🚀  

---

