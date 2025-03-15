# AI Notes Generator API

This FastAPI service generates detailed engineering notes based on user input using OpenRouter's AI.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd AI_NotesAPI
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your API key in  file.

5. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Usage

Send a  request to  with JSON data:
```json
{
  "main_topic": "Data Structures",
  "sub_topic": "Linked List",
  "additional_details": "Include real-world applications"
}
```
#   S m a r t N o t e s - A I  
 # StudyBuddy-AI
