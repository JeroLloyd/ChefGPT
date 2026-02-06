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
    raise ValueError("No API Key found. Please check your .env file.")

genai.configure(api_key=API_KEY)

# --- AUTO-DETECT MODEL LOGIC ---
def get_valid_model_name():
    """Auto-detects the best available Gemini model."""
    print("🔍 Scanning for available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name:
                    print(f"✅ Found Model: {m.name}")
                    return m.name
        print("⚠️ No specific 'Flash' model found. Defaulting to standard.")
        return "gemini-1.5-flash"
    except Exception as e:
        print(f"⚠️ Error listing models: {e}. Defaulting to standard.")
        return "gemini-1.5-flash"

ACTIVE_MODEL_NAME = get_valid_model_name()
# -------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # In production, replace "*" with your actual Vercel domain (e.g., ["https://sparkai.vercel.app"])
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

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        model = genai.GenerativeModel(ACTIVE_MODEL_NAME)
        
        # Build History
        chat_history = []
        for msg in request.history:
            role = "user" if msg.role == "user" else "model"
            chat_history.append({"role": role, "parts": msg.content})

        chat_session = model.start_chat(history=chat_history)
        
        # --- THE NEW "ADAPTIVE INTELLIGENCE" SYSTEM PROMPT ---
        system_instruction = """
        [SYSTEM INSTRUCTION: You are an Adaptive Creative Decision-Support Assistant.
        Your function is NOT to produce random suggestions. Your function is to guide intelligent ideation.
        
        NON-NEGOTIABLE RULE: NEVER GENERATE IDEAS IMMEDIATELY.
        If the user asks for ideas, you MUST first diagnose context using the Protocol below.

        STRUCTURED IDEATION PROTOCOL:
        Stage 1: Objective Diagnosis (Ask about outcome, constraints, speed vs positioning).
        Stage 2: Creator Profile Construction (Build internal profile: niche, platform, skills).
        Stage 3: Controlled Idea Divergence (3-5 distinct directions, not variations).
        Stage 4: Idea Scoring (Score on Novelty, Audience Fit, Feasibility, Leverage).
        Stage 5: Feedback Loop (Mandatory - ask user to evaluate).

        ADAPTIVE RULES:
        - Remember previous suggestions.
        - Avoid duplication.
        - Refine recommendation depth based on user expertise.
        
        TRUST-CENTERED TONE:
        - Professional, structured, calm authority.
        - NO EMOJIS.
        - NO casual filler ("Here are some cool ideas!").
        - Be analytical.

        RESPONSE STRUCTURE (When delivering recommendations):
        1. Strategic Insight
        2. Recommended Directions
        3. Top Opportunity
        4. Execution Starter Steps
        5. Decision Prompt

        Under no circumstance should ideas be generated before contextual diagnosis.
        Always explain WHY a recommendation is strategically strong or weak.]
        """
        
        # Inject the system instruction invisibly into the prompt flow
        response = chat_session.send_message(f"{system_instruction}\n\nUser: {request.message}")
        
        return {"response": response.text}
        
    except Exception as e:
        print(f"🚨 Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting Adaptive Decision Engine with Model: {ACTIVE_MODEL_NAME}")
    uvicorn.run(app, host="0.0.0.0", port=8000)