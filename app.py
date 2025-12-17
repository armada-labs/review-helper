import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(
    page_title="Review responder",
    page_icon="✨",
    layout="centered"
)

# 2. Styling
st.markdown(
    """
<style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Helvetica Neue", Arial, sans-serif;
    }

    /* Tight, centered layout */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
        max-width: 720px !important;
        margin: 0 auto !important;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Title and subtitle */
    .app-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .app-subtitle {
        text-align: center;
        font-size: 0.98rem;
        color: #6B7280;
        margin-bottom: 2.4rem;
    }

    /* Inputs */
    .stTextArea textarea,
    .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        color: #111827 !important;
        padding: 12px 14px !important;
        font-size: 0.98rem !important;
    }
    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.35) !important;
    }

    /* Tone buttons as pills */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    div[role="radiogroup"] label {
        background-color: #F9FAFB !important;
        border: 1px solid #E5E7EB !important;
        padding: 8px 22px !important;
        border-radius: 999px !important;
        color: #6B7280 !important;
        font-size: 0.95rem !important;
        cursor: pointer;
        transition: all 0.16s ease;
        margin-right: 0 !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #4F46E5 !important;
        background-color: #EEF2FF !important;
        color: #4F46E5 !important;
    }

    /* Primary button */
    div.stButton > button:first-child {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        margin-top: 0.5rem !important;
        transition: background-color 0.16s ease, transform 0.08s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #4338CA !important;
        transform: translateY(-1px);
    }

    /* Reply section */
    .reply-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 3rem 0 1rem 0;
    }

    .reply-box {
        background-color: #EEF2FF;
        border-radius: 18px;
        padding: 20px 22px;
        border: 1px solid #E0E7FF;
        font-size: 0.98rem;
        color: #111827;
        line-height: 1.6;
        margin-bottom: 1.8rem;
    }

    .reply-to-another button {
        width: 220px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. Securely load API Key
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception:
    st.error("No API key found. Please add ANTHROPIC_API_KEY to your secrets.")
    st.stop()

# 4. Session state for reply
if "generated_reply" not in st.session_state:
    st.session_state.generated_reply = ""

# 5. Header
st.markdown('<div class="app-title">Review responder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Paste a review below to generate a professional reply.</div>',
    unsafe_allow_html=True,
)

# 6. Input form
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

# 7. Generate reply
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

# 8. Reply display screen
if st.session_state.generated_reply:
    st.markdown('<div class="reply-title">Your reply</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="reply-box">{st.session_state.generated_reply}</div>',
        unsafe_allow_html=True,
    )

    # "Reply to another" button - resets the state
    col = st.container()
    with col:
        if st.button("Reply to another", key="reply_another", help="Start a new reply"):
            st.session_state.generated_reply = ""
            st.session_state.review_text = ""
            st.session_state.business_name = ""
            try:
                st.rerun()
            except Exception:
                st.experimental_rerun()
