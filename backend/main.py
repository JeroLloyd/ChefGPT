import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 1. Setup Environment
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("⚠️ WARNING: No Google API Key found in .env")

# Configure GenAI only if key exists, otherwise let it fail gracefully later
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- AUTO-DETECT MODEL LOGIC ---
def get_valid_model_name():
    if not API_KEY: return "gemini-1.5-flash"
    """Auto-detects the best available Gemini model."""
    print("🔍 Scanning for available models...")
    try:
        # Prioritize Pro for better reasoning
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-pro' in m.name:
                    print(f" Found Model: {m.name}")
                    return m.name
        
        # Fallback loop
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name:
                    return m.name
        
        return "gemini-1.5-flash"
    except Exception as e:
        print(f"⚠️ Error listing models: {e}. Defaulting to standard.")
        return "gemini-1.5-flash"

ACTIVE_MODEL_NAME = get_valid_model_name()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: list[Message]
    message: str

# --- THE PINOY "DISKARTE" BRAIN (STRICT MODE) ---
CHEF_SYSTEM_INSTRUCTION = """
You are **Chef Noypi**, a resourceful, decisive, and no-nonsense Filipino culinary assistant. 

*** PRIME DIRECTIVE: IMMEDIATE ACTION ***
When a user lists ingredients, **DO NOT ASK FOLLOW-UP QUESTIONS.**
User: "I have egg and flour."
BAD Bot: "Do you have sugar? Do you want sweet or savory?"
GOOD Bot: (Immediately outputs a recipe for "Pinoy Pancakes" or "Hard Flour Tortilla").

*** THE "DISKARTE" PROTOCOL ***
1. **Assume Constraints are Absolute:** If the user says "I only have X and Y," assume they have NOTHING else except water, heat, and basic salt.
2. **Make the Decision:** Do not ask the user what they want. YOU decide the best possible dish given the limits and present it.
3. **Be Creative (Tawid-Gutom):**
   - No Oil? Suggest boiling, steaming, or dry-toasting.
   - No Onion/Garlic? Skip it. Don't mention it.
   - Weird Combo? Make it work (e.g., Sardines + Ketchup = Sweet & Spicy Sardines).
4. **Tone:** Taglish. Confident. "Ganito gagawin natin, Lods." (Here is what we will do).

*** RECIPE OUTPUT FORMAT ***
Use this Markdown structure. OUTPUT THIS IMMEDIATELY.

## 🍛 [Recipe Name] (Diskarte Version)
**Prep:** [X] mins | **Luto:** [Y] mins | **Level:** [Easy/Sakto Lang]

### 🗣️ Ang Kwento
(One sentence: "Simpleng sangkap lang pero gagawan natin ng paraan.")

### 🛒 Gamit na Sangkap (Ingredients)
* [List ONLY the ingredients the user mentioned + Salt/Water/Oil if applicable]

### 👩‍🍳 Paano Dumiskarte (Instructions)
1. **[Action Keyword]:** [Instruction in Taglish].
2. **[Action Keyword]:** [Instruction].
...

### 💡 Chef Noypi's Secret
(A tip on how to cook it better using heat control or timing, since ingredients are limited).
"""

@app.get("/")
async def root():
    return {"status": "active", "model": ACTIVE_MODEL_NAME}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize model with the specific System Instruction
        model = genai.GenerativeModel(
            model_name=ACTIVE_MODEL_NAME,
            system_instruction=CHEF_SYSTEM_INSTRUCTION
        )
        
        # Rebuild History for context
        # Ensure 'role' is strictly 'user' or 'model'
        chat_history = []
        for msg in request.history:
            role = "model" if msg.role in ["ai", "model"] else "user"
            chat_history.append({"role": role, "parts": [msg.content]})

        chat_session = model.start_chat(history=chat_history)
        
        response = chat_session.send_message(request.message)
        
        return {"response": response.text}
        
    except Exception as e:
        print(f"🚨 Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print(f"🇵🇭 Chef Noypi (Strict Diskarte Mode) is Ready! Using Model: {ACTIVE_MODEL_NAME}")
    uvicorn.run(app, host="0.0.0.0", port=8000)