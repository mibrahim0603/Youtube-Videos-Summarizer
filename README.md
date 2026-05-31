# 🎥 YouTube Video Study Hub & AI Tutor

An interactive web application that transforms standard educational YouTube videos into comprehensive study suites. By combining managed transcript extraction proxy layers with the **Gemini 2.5 Flash** model, the platform automatically generates crisp syncopated study notes, active-recall flashcards, and interactive conceptual multiple-choice quizzes.

[Live App](https://youtube-videos-summarizer-gdpsqprwjbajf4msh7cwfo.streamlit.app/)
---

## 🚀 Key Features

* **⚡ Automated Transcript Extraction:** Bypasses standard IP blocks by utilizing an infrastructure proxy pipeline (`Supadata API`) to extract text from public YouTube links.
* **📝 Synthesized Notes:** Generates structured, high-yield study notes broken down by core contextual themes.
* **🎴 Active Recall Flashcards:** Provides a fluid, interactive digital card deck interface (click-to-flip) generated entirely by AI from the video's core takeaways.
* **🧠 Comprehensive Quizzes:** Tests retention with custom multi-choice assessments featuring live grading and instant answer validation.
* **🔒 Strict JSON Structuring:** Utilizes standard Pydantic schema validation inside a FastAPI wrapper to ensure seamless parsing into the user interface.

---

## 🛠️ The System Architecture

[YouTube Link Input]
⬇
[Supadata Proxy API Extraction] -> (Fetches timestamped dialogue array)
⬇
[FastAPI Backend Pipeline] -> (Cleans & aggregates text chunks)
⬇
[Gemini 2.5 Flash API] -> (Enforces strict JSON schema generation via Pydantic)
⬇
[Next.js React Frontend Dashboard] -> (Renders modular Notes, Flashcards & Quiz elements)


---

## 🧰 Tech Stack

* **Frontend:** Next.js 15+ (React), Tailwind CSS, Lucide Icons
* **Backend:** Python 3.10+, FastAPI, Uvicorn
* **AI Engine:** Google GenAI SDK (`gemini-2.5-flash`)
* **Data Scraper:** Supadata API (Transcript Management Proxy)

---

## 💻 Environment Setup & Local Dev

This project is fully optimized for **GitHub Codespaces**. Follow these sequential steps to boot your local instances.

### 🔑 1. Configure Repository Secrets
To keep API credentials secure, add the following parameters under your **GitHub Repository Settings ➔ Secrets and Variables ➔ Codespaces**:
* `GEMINI_API_KEY`: *Your Google Gemini API developer key*
* `SUPADATA_API_KEY`: *Your Supadata.ai transcription proxy key*

*If your Codespace session is already running, run the command palette (`Ctrl+Shift+P`) and choose `Codespaces: Restart Codespace` to load your changes.*

---

### 🐍 2. Backend Initialization (Terminal 1)

1. Navigate into the backend layer and install Python dependencies:
   ```bash
   cd backend
   pip3 install fastapi uvicorn requests google-genai pydantic

    Run the Uvicorn application server instance:
    Bash

    python3 main.py

    Note: Ensure your backend maps over host 0.0.0.0 inside cloud container topologies.

    CRITICAL STEP: Go to the Ports tab inside the Codespace panel toolbar. Right-click on Port 8000 and change its Port Visibility from Private to Public. Copy the generated Forwarded Address link string.

⚛️ 3. Frontend Initialization (Terminal 2)

    Open a second split terminal pane and navigate to your client folder:
    Bash

    cd frontend
    npm install

    Open src/app/page.tsx and map your network query address parameter near the fetch() handler block to use your active public Port 8000 Forwarded URL link:
    TypeScript

    const res = await fetch('[https://your-unique-codespace-8000.app.github.dev/api/process-video](https://your-unique-codespace-8000.app.github.dev/api/process-video)', {

    Spin up the Next.js development server:
    Bash

    npm run dev

    Click the Open in Browser popup notification window prompt on Port 3000 to interact with your finished live portal hub interface!

🛑 How to Turn Off the Environment Safely

To ensure you don't accumulate unexpected active compute hours in the cloud container:

    Target both terminal tabs sequentially and tap Ctrl + C to drop out of the Node.js and Python live listening states.

    Open your VS Code command palette (Ctrl+Shift+P), type Stop, and execute Codespaces: Stop Current Codespace.