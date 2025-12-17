import streamlit as st
import anthropic

# Page config
st.set_page_config(
    page_title="Review responder",
    page_icon="✨",
    layout="centered"
)

# Global styles
st.markdown(
    """
<style>
    .stApp {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     -sans-serif;
    }

    /* Tighter centered layout */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
        max-width: 780px !important;
        margin: 0 auto !important;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Title and subtitle */
    .app-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
        color: #020617;
    }
    .app-subtitle {
        text-align: center;
        font-size: 0.98rem;
        color: #6b7280;
        margin-bottom: 2.5rem;
    }

    /* Card that wraps the whole form */
    .review-card {
        max-width: 720px;
        margin: 0 auto;
        background: #f9fafb;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        padding: 24px 24px 20px;
        box-sizing: border-box;
    }

    /* Inputs */
    .stTextArea textarea,
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        color: #111827 !important;
        padding: 12px 14px !important;
        font-size: 0.98rem !important;
    }
    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.35) !important;
    }

    /* Make the second text input sit a little closer to the textarea */
    .review-card .stTextInput {
        margin-top: 0.75rem;
        margin-bottom: 1.1rem;
    }

    /* Radio buttons styled as pills */
    .stRadio > div {
        flex-direction: row !important;
        gap: 12px;
    }

    .stRadio label[data-baseweb="radio"] {
        background-color: #f9fafb;
        border-radius: 999px;
        border: 1px solid #e5e7eb;
        padding: 8px 22px;
        font-size: 0.95rem;
        color: #111827;
        cursor: pointer;
        transition: all 0.15s ease;
    }

    .stRadio label[data-baseweb="radio"]:hover {
        border-color: #6366f1;
        background-color: #eef2ff;
    }

    /* Selected pill (uses :has which is supported in modern browsers) */
    .stRadio label[data-baseweb="radio"]:has(input:checked) {
        border-color: #6366f1;
        background-color: #eef2ff;
    }

    /* Primary outlined buttons (Generate / Reply to another) */
    div.stButton > button:first-child {
        background-color: #ffffff !important;
        color: #4f46e5 !important;
        border-radius: 10px !important;
        border: 1px solid #a855f7 !important;
        padding: 10px 18px !important;
        font-weight: 500 !important;
        font-size: 0.96rem !important;
        width: auto !important;
        transition: background-color 0.12s ease, box-shadow 0.12s ease,
                    transform 0.06s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #f5f3ff !important;
        box-shadow: 0 0 0 1px rgba(148, 163, 184, 0.4);
        transform: translateY(-1px);
    }

    /* Space above generate button inside card */
    .review-card div.stButton {
        margin-top: 1.2rem;
    }

    /* Reply section */
    .reply-wrapper {
        max-width: 720px;
        margin: 3rem auto 0 auto;
    }
    .reply-title {
        text-align: center;
        font-size: 1.35rem;
        font-weight: 600;
        margin-bottom: 1.3rem;
        color: #020617;
    }
    .reply-box {
        background-color: #eef2ff;
        border-radius: 18px;
        padding: 20px 22px;
        border: 1px solid #e0e7ff;
        font-size: 0.98rem;
        color: #111827;
        line-height: 1.6;
        margin-bottom: 1.6rem;
    }

</style>
""",
    unsafe_allow_html=True,
)

# API client
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception:
    st.error("No API key found. Please add ANTHROPIC_API_KEY to your secrets.")
    st.stop()

# Session state for reply
if "generated_reply" not in st.session_state:
    st.session_state.generated_reply = ""

# Header
st.markdown('<div class="app-title">Review responder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Paste a review below to generate a professional reply.</div>',
    unsafe_allow_html=True,
)

# Form inside the card
st.markdown('<div class="review-card">', unsafe_allow_html=True)

with st.form("review_form", clear_on_submit=False):
    review_text = st.text_area(
        label="Review",
        height=150,
        placeholder="Paste the customer review here...",
        label_visibility="collapsed",
        key="review_text",
    )

    business_name = st.text_input(
        label="Business name",
        placeholder="Add your business name (optional)",
        label_visibility="collapsed",
        key="business_name",
    )

    tone = st.radio(
        "Tone",
        ["Grateful", "Polite & Firm", "Short"],
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="tone_choice",
    )

    submitted = st.form_submit_button("Generate reply")

st.markdown("</div>", unsafe_allow_html=True)

# Call Anthropic and store reply
if submitted and review_text.strip():
    with st.spinner("Generating your reply"):
        system_prompt = f"""
You are a professional business owner replying to an online review.

Business name: {business_name if business_name else "the business"}
Tone: {tone}

Write a short, friendly and professional response.

Rules:
- Be polite, empathetic and clear.
- Do not mention the name of any review platform.
- Make it sound natural and human.
- Keep it under 60 words.
- Return only the reply text.
        """.strip()

        try:
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": review_text}],
            )
            st.session_state.generated_reply = message.content[0].text.strip()
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Reply view
if st.session_state.generated_reply:
    st.markdown('<div class="reply-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="reply-title">Your reply</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="reply-box">{st.session_state.generated_reply}</div>',
        unsafe_allow_html=True,
    )

    # Left aligned "Reply to another"
    if st.button("Reply to another", key="reply_another"):
        st.session_state.generated_reply = ""
        st.session_state.review_text = ""
        st.session_state.business_name = ""
        try:
            st.rerun()
        except Exception:
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)
