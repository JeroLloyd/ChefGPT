# 👨‍🍳 CHEFgpt | AI Kusina Assistant

![Project Screenshot](image_95baf7.png)

> **"Anong lulutuin mo?"** (What are you cooking?)
> A resourceful, witty, and culturally aware cooking assistant powered by **Google Gemini** and **Next.js**.

![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688?style=flat-square&logo=fastapi)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC?style=flat-square&logo=tailwind-css)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=flat-square&logo=google)

## 📖 About The Project

**CHEFgpt** isn't just another recipe generator. It is built with a specific **"Diskarte Protocol"** (Resourcefulness Protocol). 

Most recipe apps ask you to buy more ingredients. CHEFgpt asks what you *already have* and creates the best possible meal out of it. It is designed for the Filipino context, understanding local ingredients (sardines, rice, egg) and constraints (no oven, limited budget).

### ✨ Key Features

* **🧠 Strict "Diskarte" Mode:** The AI is prompted to never ask for extra ingredients. If you only have eggs and flour, it will invent a recipe for just those two items.
* **🗣️ Taglish Persona:** Interacts in a natural, confident Filipino/English mix.
* **📒 Digital Cookbook:** Pin and save your favorite generated recipes to a sidebar for easy access.
* **🖨️ Print-Ready:** One-click formatting to print recipes for the kitchen.
* **🎨 Modern UI:** A dark-themed, glassmorphism-inspired interface using Tailwind CSS and Inter typography.

---

## 🛠️ Tech Stack

### Frontend
* **Framework:** [Next.js](https://nextjs.org/) (App Router)
* **Styling:** [Tailwind CSS](https://tailwindcss.com/)
* **Authentication:** [Clerk](https://clerk.com/)
* **Typography:** Inter & Geist Mono

### Backend
* **Server:** [FastAPI](https://fastapi.tiangolo.com/)
* **AI Model:** [Google Gemini API](https://ai.google.dev/) (Auto-detects Pro or Flash models)
* **Language:** Python 3.9+

---

## 🚀 Mise en place (Setup Guide)

Follow these instructions to get the kitchen running locally.

### 1. Prerequisites
* Node.js (v18+)
* Python (v3.9+)
* A Google Cloud API Key (for Gemini)
* A Clerk Account (for Authentication)

### 2. Backend Setup (The Brain)

Navigate to the backend folder (or root, depending on your structure) and set up the Python environment.

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Create a .env file in the same directory as main.py:

Code snippet
GOOGLE_API_KEY=your_google_gemini_api_key_here
Start the Backend Server:

Bash
python main.py
# Output: 🇵🇭 Chef Noypi (Strict Diskarte Mode) is Ready!
3. Frontend Setup (The Interface)
Open a new terminal and navigate to the frontend directory.

Bash
# Install Node modules
npm install
Create a .env.local file in the root of your Next.js project:

Code snippet
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=http://localhost:8000
Start the Frontend:

Bash
npm run dev
Open http://localhost:3000 in your browser.

📂 Project Structure
CHEFgpt/
├── app/
│   ├── layout.tsx       # Root layout with Clerk Provider & Font config
│   ├── page.tsx         # Main Chat Interface (State, Markdown, UI)
│   └── globals.css      # Tailwind & Custom Semantic Variables
├── main.py              # FastAPI Server & Gemini Prompt Engineering
├── requirements.txt     # Python Dependencies
├── tailwind.config.ts   # Tailwind Configuration
└── ...
🧠 The "Diskarte" Prompt
The core logic resides in main.py. The system instruction ensures the AI adheres to the following rules:

Assume Absolute Constraints: Do not suggest buying more items.

No Follow-up Questions: Immediate action based on input.

Tawid-Gutom Creativity: Suggest boiling/steaming if oil is missing; suggest weird combos if necessary.

Format: Returns a structured Markdown recipe with a "Chef's Secret" tip.

🤝 Contributing
Got a better way to cook adobo? Or a better way to code this? Contributions are welcome!

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

<div align="center">
<p>Made with ❤️ and 🍚 in the Philippines</p>
</div>