from fpdf import FPDF
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="CORTEXA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# FUTURISTIC CSS
# =====================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

    .stApp {
        background:
            radial-gradient(circle at top left, #172554 0%, transparent 25%),
            radial-gradient(circle at bottom right, #0f172a 0%, transparent 25%),
            linear-gradient(135deg, #020617, #0f172a, #111827);
        color: white !important;
        overflow-x: hidden;
    }

    header { background: transparent !important; }
    .block-container { padding-top: 2rem !important; }

    html, body, p, span, div, label { color: white !important; }
    h1, h2, h3, h4, h5, h6 { color: white !important; }

    .animated-bg {
        position: fixed;
        width: 100%; height: 100%;
        top: 0; left: 0;
        background: radial-gradient(circle, rgba(56,189,248,0.12), transparent 60%);
        animation: pulse 6s infinite alternate;
        z-index: -1;
    }

    @keyframes pulse {
        from { transform: scale(1); opacity: 0.4; }
        to   { transform: scale(1.3); opacity: 1; }
    }

    section[data-testid="stSidebar"] {
        background: rgba(2,6,23,0.85);
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    .brain-icon {
        font-size: 120px;
        text-align: center;
        margin-bottom: -10px;
        animation: brainFloat 3s ease-in-out infinite, brainGlow 2s infinite alternate;
    }

    @keyframes brainFloat {
        0%   { transform: translateY(0px); }
        50%  { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes brainGlow {
        from { filter: drop-shadow(0px 0px 12px rgba(56,189,248,0.3)); }
        to   { filter: drop-shadow(0px 0px 40px rgba(56,189,248,0.9)); }
    }

    .hero-title {
        position: relative;
        text-align: center;
        font-size: 95px;
        font-weight: 900;
        letter-spacing: 5px;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: cortexGlow 2s infinite alternate;
    }

    @keyframes cortexGlow {
        from { text-shadow: 0px 0px 15px rgba(56,189,248,0.4), 0px 0px 30px rgba(129,140,248,0.25); }
        to   { text-shadow: 0px 0px 40px rgba(56,189,248,0.95), 0px 0px 70px rgba(129,140,248,0.8); }
    }

    .hero-title::before {
        content: "";
        position: absolute;
        top: 50%; left: -5%;
        width: 110%; height: 8px;
        background: linear-gradient(90deg, transparent, rgba(56,189,248,0.9), rgba(129,140,248,1), rgba(34,211,238,0.9), transparent);
        filter: blur(8px);
        animation: electricFlow 2s linear infinite;
        z-index: -1;
    }

    @keyframes electricFlow {
        0%   { transform: translateX(-120%); opacity: 0; }
        20%  { opacity: 1; }
        80%  { opacity: 1; }
        100% { transform: translateX(120%); opacity: 0; }
    }

    .hero-subtitle {
        text-align: center;
        font-size: 30px;
        font-family: 'Exo 2', sans-serif;
        color: #f8fafc !important;
        margin-top: -15px;
        margin-bottom: 55px;
        animation: subtitleBounce 2.5s ease-in-out infinite;
    }

    @keyframes subtitleBounce {
        0%   { transform: translateY(0px); }
        25%  { transform: translateY(-5px); }
        50%  { transform: translateY(0px); }
        75%  { transform: translateY(-3px); }
        100% { transform: translateY(0px); }
    }

    .stTextInput label {
        color: #e2e8f0 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    .stTextInput input {
        background: rgba(15,23,42,0.75) !important;
        color: white !important;
        border: 1px solid rgba(56,189,248,0.18) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        font-size: 18px !important;
        box-shadow: 0px 0px 18px rgba(56,189,248,0.08);
    }

    .stTextInput input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    .stButton button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 18px;
        font-size: 18px;
        font-weight: 700;
        transition: 0.3s ease;
        box-shadow: 0px 0px 28px rgba(99,102,241,0.35);
    }

    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 40px rgba(56,189,248,0.45);
    }

    .flashcard {
        background: linear-gradient(145deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95));
        border: 1px solid rgba(56,189,248,0.12);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 24px;
        transition: 0.3s ease;
        box-shadow: 0px 0px 30px rgba(56,189,248,0.08);
    }

    .flashcard:hover {
        transform: translateY(-6px);
        box-shadow: 0px 0px 45px rgba(56,189,248,0.18);
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.04);
        color: white !important;
        border-radius: 14px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: 700;
        margin-right: 10px;
    }

    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#38bdf8, #818cf8);
        border-radius: 10px;
    }

    /* Chat bubbles */
    .chat-user {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        border-radius: 18px 18px 4px 18px;
        padding: 14px 20px;
        margin: 10px 0 10px 20%;
        color: white;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(37,99,235,0.3);
    }
    .chat-ai {
        background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95));
        border: 1px solid rgba(56,189,248,0.15);
        border-radius: 18px 18px 18px 4px;
        padding: 14px 20px;
        margin: 10px 20% 10px 0;
        color: white;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(56,189,248,0.1);
    }
    .chat-label {
        font-size: 12px;
        opacity: 0.6;
        margin-bottom: 4px;
        font-family: 'Exo 2', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    </style>

    <div class="animated-bg"></div>
    """,
    unsafe_allow_html=True
)

# =====================================
# GEMINI API
# =====================================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown("# 🚀 CORTEXA")
    st.markdown("---")

    st.markdown(
        """
        ## 🧠 What is CORTEXA?

        CORTEXA is a futuristic AI-powered lecture
        intelligence system that transforms YouTube
        lectures into an interactive learning experience.
        """
    )

    st.markdown("---")

    st.markdown(
        """
        ## ⚡ What CORTEXA Can Do

        ✅ Generate Smart Notes  
        ✅ Create AI Flashcards  
        ✅ Build Interactive Quizzes  
        ✅ Voice-Based AI Tutor  
        ✅ Understand Lectures  
        ✅ Answer Doubts Instantly  
        ✅ Improve Learning Speed  
        """
    )

    st.markdown("---")
    st.info("Built using Gemini AI + Streamlit")

# =====================================
# HERO SECTION
# =====================================

st.markdown(
    """
    <div class="brain-icon">🧠</div>
    <div class="hero-title">CORTEXA</div>
    <div class="hero-subtitle">Futuristic AI Lecture Intelligence System</div>
    """,
    unsafe_allow_html=True
)

# =====================================
# URL INPUT
# =====================================

video_url = st.text_input(
    "📺 Paste YouTube Video URL",
    placeholder="https://youtube.com/watch?v=..."
)

# =====================================
# SESSION STATE
# =====================================

for key in ["notes", "flashcards", "quiz", "transcript", "current_question", "formatted_quiz", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "chat_history" else []

# =====================================
# VIDEO ID EXTRACTOR
# =====================================


def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        query = parse_qs(parsed_url.query)
        if "v" in query:
            return query["v"][0]
    return None

# =====================================
# YOUTUBE EMBED PREVIEW
# =====================================


if video_url:
    vid_id = extract_video_id(video_url)
    if vid_id:
        st.markdown(
            f"""
            <div style="display:flex; justify-content:center; margin-bottom:20px;">
                <iframe width="720" height="405"
                    src="https://www.youtube.com/embed/{vid_id}"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                    style="border-radius:20px; box-shadow:0 0 40px rgba(56,189,248,0.25);">
                </iframe>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================
# GET TRANSCRIPT
# =====================================


def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Could not extract video ID from URL.")
    transcript_list = YouTubeTranscriptApi().fetch(video_id)
    full_text = " ".join([entry.text.strip() for entry in transcript_list])
    if not full_text.strip():
        raise ValueError("Transcript is empty.")
    return full_text

# =====================================
# CONTENT GENERATORS
# =====================================


def generate_notes(transcript):
    prompt = f"""
    Convert this lecture transcript into structured study notes:
    - Smart Notes with clear headings
    - Key Concepts explained simply
    - Important Bullet Points
    - Easy Explanations for beginners

    Transcript:
    {transcript[:15000]}
    """
    return model.generate_content(prompt).text


def generate_flashcards(transcript):
    prompt = f"""
    Create 10-15 flashcards from this lecture.

    Strict format:
    Q: Question here
    A: Answer here

    Make questions test understanding, not just recall.

    Transcript:
    {transcript[:15000]}
    """
    return model.generate_content(prompt).text


def generate_quiz(transcript):
    prompt = f"""
    Create 5 multiple choice quiz questions from this lecture.

    STRICT FORMAT — follow exactly:

    Question: <question text>
    A) <option>
    B) <option>
    C) <option>
    D) <option>
    Correct: <letter only, e.g. A>

    Transcript:
    {transcript[:12000]}
    """
    return model.generate_content(prompt).text

# =====================================
# PDF EXPORT
# =====================================


def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(200, 12, title, ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    clean_text = (
        content
        .replace("•", "-")
        .replace("—", "-")
        .replace("→", "->")
        .replace("✅", "[OK]")
        .replace("❓", "Q:")
        .replace("✨", "")
        # Strip non-latin1 characters to avoid FPDF encoding errors
    )
    # Encode safely
    safe_text = clean_text.encode(
        "latin-1", errors="replace").decode("latin-1")
    pdf.multi_cell(0, 8, safe_text)
    file_name = "/tmp/" + title.replace(" ", "_") + ".pdf"
    pdf.output(file_name)
    return file_name

# =====================================
# VOICE INPUT
# =====================================


def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio. Please try again."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# =====================================
# GENERATE BUTTON
# =====================================


if st.button("✨ Generate AI Study Material"):
    if video_url:
        with st.spinner("🧠 Processing Lecture..."):
            try:
                transcript = get_transcript(video_url)
                notes = generate_notes(transcript)
                flashcards = generate_flashcards(transcript)
                quiz = generate_quiz(transcript)

                st.session_state.notes = notes
                st.session_state.flashcards = flashcards
                st.session_state.quiz = quiz
                st.session_state.transcript = transcript
                # FIX: clear cached quiz & chat when new video is processed
                st.session_state.formatted_quiz = quiz
                st.session_state.chat_history = []

                st.success("🚀 Study Material Generated!")

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a YouTube URL")

# =====================================
# MAIN CONTENT TABS
# =====================================

if st.session_state.notes:

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Smart Notes",
        "🧠 Flashcards",
        "🧪 Quiz",
        "🤖 AI Tutor"
    ])

    # ─── NOTES TAB ───────────────────────────────────────────
    with tab1:

        st.markdown(
            """
            <style>
            /* Fix code blocks hidden by white background */
            .stMarkdown code {
                background: rgba(15, 23, 42, 0.9) !important;
                color: #7dd3fc !important;
                border: 1px solid rgba(56,189,248,0.25) !important;
                border-radius: 8px !important;
                padding: 2px 8px !important;
                font-family: 'Courier New', monospace !important;
                font-size: 15px !important;
            }
            .stMarkdown pre {
                background: rgba(15, 23, 42, 0.9) !important;
                border: 1px solid rgba(56,189,248,0.25) !important;
                border-radius: 12px !important;
                padding: 16px !important;
                overflow-x: auto !important;
            }
            .stMarkdown pre code {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                color: #7dd3fc !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.notes)

        st.markdown("---")

        # FIX: PDF export button is now actually wired up
        if st.button("📄 Download Notes as PDF"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_path = create_pdf(
                        "CORTEXA Smart Notes", st.session_state.notes)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Click to Download",
                            data=f,
                            file_name="CORTEXA_Smart_Notes.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"PDF error: {e}")

    # ─── FLASHCARDS TAB ──────────────────────────────────────
    with tab2:

        st.caption("💡 Click a card to flip and reveal the answer")

        # Inject CSS once — pure CSS checkbox flip, no JS needed
        st.markdown("""
<style>
.fc-wrap {
    margin-bottom: 20px;
}
/* Hide the checkbox */
.fc-toggle {
    display: none;
}
.fc-front, .fc-back {
    width: 100%;
    box-sizing: border-box;
    border-radius: 20px;
    padding: 22px 20px;
    cursor: pointer;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    line-height: 1.65;
    transition: box-shadow 0.25s ease;
}
.fc-front {
    display: block;
    background: linear-gradient(145deg, rgba(30,41,59,0.97), rgba(15,23,42,0.97));
    border: 1px solid rgba(56,189,248,0.22);
    box-shadow: 0 0 28px rgba(56,189,248,0.10);
    color: white !important;
    font-weight: 700;
    text-align: center;
}
.fc-back {
    display: none;
    background: linear-gradient(145deg, rgba(6,95,70,0.97), rgba(4,120,87,0.97));
    border: 1px solid rgba(16,185,129,0.3);
    box-shadow: 0 0 28px rgba(16,185,129,0.12);
    color: white !important;
    text-align: center;
}
/* When checkbox is checked, swap front/back */
.fc-toggle:checked ~ .fc-front {
    display: none;
}
.fc-toggle:checked ~ .fc-back {
    display: block;
}
.fc-front:hover { box-shadow: 0 0 44px rgba(56,189,248,0.30); }
.fc-back:hover  { box-shadow: 0 0 44px rgba(16,185,129,0.30); }
.fc-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.5;
    margin-bottom: 10px;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

        cards = st.session_state.flashcards.split("Q:")
        cols = st.columns(2)
        index = 0

        for card in cards:
            if "A:" in card:
                question, answer = card.split("A:", 1)
                question = question.replace("**", "").strip()
                answer = answer.replace("**", "").strip()

                q_len = len(question)
                a_len = len(answer)
                q_fs = "8px" if q_len > 300 else "9px" if q_len > 200 else "10px" if q_len > 120 else "11px"
                a_fs = "11px" if a_len > 300 else "12px" if a_len > 200 else "13px" if a_len > 120 else "14px"

                with cols[index % 2]:
                    # label[for] targets the hidden checkbox — clicking label toggles it
                    st.markdown(f"""
<div class="fc-wrap">
  <input type="checkbox" class="fc-toggle" id="fc_{index}">
  <label for="fc_{index}" class="fc-front" style="font-size:{q_fs}; display:block;">
    <div class="fc-label">Question · click to reveal answer</div>
    {question}
  </label>
  <label for="fc_{index}" class="fc-back" style="font-size:{a_fs};">
    <div class="fc-label">Answer · click to go back</div>
    {answer}
  </label>
</div>
""", unsafe_allow_html=True)

                index += 1

        st.markdown("---")

        # PDF export for flashcards
        if st.button("📄 Download Flashcards as PDF"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_path = create_pdf(
                        "CORTEXA Flashcards", st.session_state.flashcards)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Click to Download",
                            data=f,
                            file_name="CORTEXA_Flashcards.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"PDF error: {e}")

    # ─── QUIZ TAB ────────────────────────────────────────────
    with tab3:

        quiz_blocks = st.session_state.formatted_quiz.split("Question:")
        question_number = 0

        for block in quiz_blocks:
            if "Correct:" not in block:
                continue

            lines = [l.strip() for l in block.split("\n") if l.strip()]
            question = lines[0]
            options = []
            correct = ""

            for line in lines[1:]:
                if line.startswith(("A)", "B)", "C)", "D)")):
                    options.append(line)
                elif line.startswith("Correct:"):
                    correct = line.replace("Correct:", "").strip()

            if not options or not correct:
                continue

            st.markdown(
                f'<div class="flashcard"><h2>❓ Question {question_number + 1}: {question}</h2></div>',
                unsafe_allow_html=True
            )

            selected = st.radio(
                "Choose your answer:",
                options,
                key=f"quiz_{question_number}",
                index=None
            )

            if st.button("Submit Answer", key=f"submit_{question_number}"):
                if selected is None:
                    st.warning("Please select an answer first.")
                elif selected.startswith(correct):
                    st.success("✅ Correct Answer!")
                    st.balloons()
                else:
                    st.error(f"❌ Wrong! The correct answer was: **{correct}**")

            st.markdown("---")
            question_number += 1

    # ─── AI TUTOR TAB ────────────────────────────────────────
    with tab4:

        st.markdown("### 🤖 Chat with CORTEXA Tutor")
        st.caption("Ask anything about the lecture — by typing or speaking.")

        # FIX: render full chat history (not just last answer)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-user"><div class="chat-label">You</div>{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-ai"><div class="chat-label">🧠 CORTEXA</div>{msg["content"]}</div>',
                    unsafe_allow_html=True
                )

        # Voice input
        col_voice, col_clear = st.columns([1, 1])
        with col_voice:
            if st.button("🎤 Speak Question"):
                voice_text = listen_to_voice()
                st.session_state.current_question = voice_text
                st.success(f"Heard: {voice_text}")

        with col_clear:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.session_state.current_question = ""
                st.rerun()

        # Text input — pre-fill with voice result if available
        default_q = st.session_state.current_question
        user_question = st.text_input(
            "Ask your doubt here:",
            value=default_q,
            key="question_box"
        )

        final_question = user_question.strip()

        if st.button("🚀 Ask AI Tutor") and final_question:
            with st.spinner("🤖 Thinking..."):
                tutor_prompt = f"""
You are CORTEXA, a futuristic AI tutor.

STRICT RULES:
- Answer ONLY based on the lecture content below
- Explain clearly and concisely
- If the answer is not in the lecture, say so honestly

Lecture:
{st.session_state.transcript[:12000]}

Student Question:
{final_question}
"""
                try:
                    response = model.generate_content(tutor_prompt)
                    answer = response.text

                    # FIX: append to chat history instead of replacing
                    st.session_state.chat_history.append(
                        {"role": "user",      "content": final_question})
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer})
                    st.session_state.current_question = ""

                    st.rerun()

                except Exception as e:
                    st.error(f"AI Tutor error: {e}")
