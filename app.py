import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()

APP_NAME = "Lumière"
TAGLINE = "Where curiosity meets elegance"
DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

PERSONAS = {
    "✨ Classic": "You are Lumière, a refined, warm and articulate AI assistant. Be clear and concise, use Markdown when helpful.",
    "🪶 Poetic": "You are Lumière, a lyrical assistant. Answer accurately, but with graceful, evocative language and the occasional metaphor.",
    "⚡ Straight to the point": "You are Lumière. Give the shortest accurate answer possible. Use bullets when listing. No fluff.",
    "🎈 Playful": "You are Lumière, a witty, upbeat assistant. Be helpful and accurate, with light humour and a friendly emoji now and then.",
}

SUGGESTIONS = [
    ("🌌", "Explain black holes like I'm five"),
    ("💡", "Give me 5 creative side-project ideas"),
    ("✍️", "Help me write a polite follow-up email"),
    ("🧠", "Teach me a mental model for better decisions"),
]

st.set_page_config(page_title=APP_NAME, page_icon="✨", layout="centered")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,500&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }

    /* Animated aurora background */
    .stApp {
        background: linear-gradient(125deg, #0b0a12, #1a1033, #0f1a33, #2a1236, #0b0a12);
        background-size: 400% 400%;
        animation: aurora 22s ease infinite;
        color: #ece9f5;
    }
    @keyframes aurora { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }

    /* Floating glow orbs */
    .stApp::before, .stApp::after {
        content: ""; position: fixed; border-radius: 50%; filter: blur(90px);
        z-index: 0; pointer-events: none; opacity: .45;
    }
    .stApp::before { width: 420px; height: 420px; top: -120px; left: -120px;
        background: radial-gradient(circle, #ff7ac6, transparent 70%); animation: float1 16s ease-in-out infinite; }
    .stApp::after { width: 480px; height: 480px; bottom: -160px; right: -140px;
        background: radial-gradient(circle, #6d8bff, transparent 70%); animation: float2 19s ease-in-out infinite; }
    @keyframes float1 { 50% { transform: translate(90px, 70px) scale(1.15); } }
    @keyframes float2 { 50% { transform: translate(-80px, -60px) scale(1.1); } }

    .block-container { position: relative; z-index: 1; padding-top: 2rem; max-width: 780px; }

    /* Hero */
    .hero { text-align: center; padding: 0.5rem 0 1rem 0; }
    .hero .logo {
        width: 64px; height: 64px; margin: 0 auto 10px auto; border-radius: 20px;
        display: flex; align-items: center; justify-content: center; font-size: 30px;
        background: linear-gradient(135deg, #f5d9a8, #e6a8d7, #8fa6ff);
        box-shadow: 0 0 40px rgba(230,168,215,.55); animation: pulse 3.5s ease-in-out infinite;
    }
    @keyframes pulse { 50% { box-shadow: 0 0 65px rgba(143,166,255,.75); transform: scale(1.06); } }
    .hero h1 {
        font-family: 'Playfair Display', serif; font-weight: 800; font-size: 3.4rem; margin: 0;
        background: linear-gradient(90deg, #f5d9a8, #f3a6d8, #9fb4ff, #f5d9a8);
        background-size: 250% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 7s linear infinite;
    }
    @keyframes shine { to { background-position: 250% center; } }
    .hero p { font-family: 'Playfair Display', serif; font-style: italic; color: #b3acd0;
              font-size: 1.05rem; margin-top: .3rem; }

    /* Welcome card */
    .welcome { text-align:center; margin: 1.2rem auto 1.4rem auto; padding: 1.4rem 1.2rem;
        border-radius: 24px; background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.09); backdrop-filter: blur(14px); }
    .welcome h3 { font-family:'Playfair Display',serif; margin:0 0 .3rem 0; font-size:1.5rem; color:#f5e6cf; }
    .welcome span { color:#a69fc2; font-weight:300; }

    /* Suggestion chips */
    .stButton > button {
        width: 100%; min-height: 3.2rem; border-radius: 16px; text-align: left;
        border: 1px solid rgba(255,255,255,.12); color: #e8e3f7; font-weight: 400;
        background: rgba(255,255,255,.05); transition: all .25s ease;
    }
    .stButton > button:hover {
        transform: translateY(-3px); color: #fff; border-color: rgba(243,166,216,.7);
        background: linear-gradient(135deg, rgba(243,166,216,.18), rgba(143,166,255,.18));
        box-shadow: 0 10px 28px rgba(143,166,255,.22);
    }

    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 22px; padding: 1rem 1.2rem; margin-bottom: .8rem;
        background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.09);
        backdrop-filter: blur(14px); animation: rise .45s ease both;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(243,166,216,.20), rgba(143,166,255,.20));
        border: 1px solid rgba(243,166,216,.35);
        margin-left: 12%;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        margin-right: 8%; border-left: 3px solid #f5d9a8;
    }
    @keyframes rise { from { opacity:0; transform: translateY(14px); } to { opacity:1; transform:none; } }

    /* Input */
    [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background: transparent !important; }
    [data-testid="stChatInput"] > div {
        background: rgba(255,255,255,.07) !important; border-radius: 999px;
        border: 1px solid rgba(243,166,216,.4); box-shadow: 0 0 30px rgba(143,166,255,.15);
        transition: box-shadow .3s ease;
    }
    [data-testid="stChatInput"] > div:focus-within { box-shadow: 0 0 40px rgba(243,166,216,.4); }
    [data-testid="stChatInput"] textarea { color: #f1edfb; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(14,12,24,.82); backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    .side-title { font-family:'Playfair Display',serif; font-size:1.6rem; color:#f5d9a8; margin-bottom:.2rem; }
    .stat { display:inline-block; padding:.25rem .7rem; margin:.2rem .2rem 0 0; border-radius:999px;
        font-size:.75rem; background:rgba(255,255,255,.07); color:#cfc8ea; border:1px solid rgba(255,255,255,.1); }
    ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-thumb { background: rgba(255,255,255,.15); border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = None

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(f"<div class='side-title'>✨ {APP_NAME}</div>", unsafe_allow_html=True)
    persona = st.selectbox("Personality", list(PERSONAS.keys()))
    temperature = st.slider("Creativity", 0.0, 1.5, 0.7, 0.05)
    model_name = st.text_input("Model (OpenRouter)", value=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL))
    st.markdown(
        f"<span class='stat'>💬 {len(st.session_state.messages)} messages</span>"
        f"<span class='stat'>🤖 {model_name.split('/')[-1][:22]}</span>",
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("🗑️ New conversation"):
        st.session_state.messages = []
        st.rerun()
    if st.session_state.messages:
        transcript = f"# {APP_NAME} chat — {datetime.now():%Y-%m-%d %H:%M}\n\n" + "\n\n".join(
            f"**{'You' if m['role'] == 'user' else APP_NAME}:** {m['content']}"
            for m in st.session_state.messages
        )
        st.download_button("⬇️ Save conversation", transcript, file_name="lumiere_chat.md")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("OPENROUTER_API_KEY not found. Add it to a `.env` file next to app.py.")
    st.stop()


# ---------- LangChain pipeline ----------
@st.cache_resource(show_spinner=False)
def build_chain(model: str, temp: float, key: str, system_prompt: str):
    llm = ChatOpenAI(
        model=model,
        temperature=temp,
        api_key=key,
        base_url="https://openrouter.ai/api/v1",
        streaming=True,
    )
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), MessagesPlaceholder("history"), ("human", "{input}")]
    )
    return prompt | llm | StrOutputParser()


chain = build_chain(model_name, temperature, api_key, PERSONAS[persona])

# ---------- Hero ----------
st.markdown(
    f"""<div class="hero"><div class="logo">✨</div><h1>{APP_NAME}</h1><p>{TAGLINE}</p></div>""",
    unsafe_allow_html=True,
)

# ---------- Welcome + suggestions ----------
if not st.session_state.messages:
    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    st.markdown(
        f"<div class='welcome'><h3>{greeting} 👋</h3><span>Pick a spark below, or ask me anything.</span></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (icon, text) in enumerate(SUGGESTIONS):
        if cols[i % 2].button(f"{icon}  {text}", key=f"sug{i}"):
            st.session_state.pending = text
            st.rerun()

# ---------- History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍🎤" if msg["role"] == "user" else "✨"):
        st.markdown(msg["content"])

# ---------- Input ----------
user_input = st.chat_input(f"Whisper something to {APP_NAME}...") or st.session_state.pending
st.session_state.pending = None

if user_input:
    history = [
        HumanMessage(m["content"]) if m["role"] == "user" else AIMessage(m["content"])
        for m in st.session_state.messages
    ]
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍🎤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="✨"):
        try:
            with st.spinner("Lumière is thinking…"):
                stream = chain.stream({"history": history, "input": user_input})
                first = next(stream, "")

            def full_stream():
                yield first
                yield from stream

            reply = st.write_stream(full_stream())
        except Exception as e:
            reply = f"⚠️ Something went wrong: {e}"
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
