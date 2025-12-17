import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(page_title="Review Responder", page_icon="✨", layout="centered")

# 2. Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reply" not in st.session_state:
    st.session_state.reply = ""

# 3. CSS INJECTION (The "Bulletproof" Styles)
st.markdown("""
<style>
    /* IMPORT FONT INTER */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* REMOVE DEFAULT STREAMLIT PADDING & CHROME */
    .stApp { background-color: #FFFFFF; }
    .block-container {
        max-width: 700px;
        padding-top: 4rem;
        padding-bottom: 2rem;
    }
    header, footer, #MainMenu { display: none !important; }

    /* HIDE FORM BORDER */
    [data-testid="stForm"] {
        border: none;
        padding: 0;
        box-shadow: none;
    }

    /* TYPOGRAPHY */
    h1 {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 36px !important;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0.5rem !important;
    }
    p, .stMarkdown p {
        color: #6F6F6F !important;
        font-size: 16px !important;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* INPUTS (Text Area & Input) */
    .stTextArea textarea, .stTextInput input {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 16px !important;
        color: #000000 !important; /* Dark text */
        background-color: #FFFFFF !important;
        box-shadow: none !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #7C90FF !important;
        box-shadow: 0 0 0 4px rgba(124, 144, 255, 0.1) !important;
    }
    ::placeholder { color: #D1D5DB !important; opacity: 1; }

    /* RADIO BUTTONS (The "Card" Look) */
    [role="radiogroup"] {
        justify-content: center;
        gap: 12px;
        margin-bottom: 30px;
    }
    
    /* The individual label container */
    [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0px !important; /* Fix spacing inside cards */
    }

    /* This targets the label box */
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 12px 0px !important; /* Vertical padding */
        width: 140px !important; /* Fixed width for uniformity */
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Hover State */
    div[role="radiogroup"] label:hover {
        border-color: #7C90FF !important;
        color: #7C90FF !important;
    }

    /* Selected State (Blue Border + Blue Text) */
    div[role="radiogroup"] label:has(input:checked) {
        border-color: #7C90FF !important;
        color: #7C90FF !important;
        background-color: #F5F7FF !important;
    }
    
    /* Hide the actual radio circle */
    div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }
    
    /* Text inside the radio button */
    div[role="radiogroup"] label p {
        font-weight: 500 !important;
        font-size: 15px !important;
        margin: 0 !important;
        padding: 0 !important;
        color: inherit !important;
    }

    /* THE GENERATE BUTTON (The specific fix for your screenshot) */
    [data-testid="stFormSubmitButton"] {
        display: flex;
        justify-content: center;
    }
    
    [data-testid="stFormSubmitButton"] button {
        background-color: #7C90FF !important;
        color: white !important;
        border: none !important;
        padding: 14px 40px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        width: 240px !important; /* Match mockup width */
        transition: background-color 0.2s;
        box-shadow: 0 4px 6px -1px rgba(124, 144, 255, 0.3) !important;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #6A7FD6 !important;
    }
    
    [data-testid="stFormSubmitButton"] button:active {
        transform: translateY(1px);
    }
    
    /* Result Box */
    .result-box {
        background-color: #F8FAFC;
        border: 1px solid #EEF2FF;
        border-radius: 12px;
        padding: 32px;
        color: #334155;
        font-size: 16px;
        line-height: 1.6;
        margin: 20px 0 40px 0;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# 4. API SETUP
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except:
    pass

# 5. UI LOGIC

if st.session_state.page == "home":
    
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)

    # Use clear_on_submit=False to keep inputs if needed, or True to clear.
    with st.form("main_form", clear_on_submit=False):
        
        # 1. Review Input
        review_text = st.text_area(
            "Review",
            height=200, 
            placeholder="Paste the customer review here...",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # 2. Business Name
        business_name = st.text_input(
            "Business Name", 
            placeholder="Add your business name (optional)",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # 3. Tone Selector
        st.markdown("<p style='margin-bottom: 12px !important; font-size: 15px !important;'>What tone would you like to reply with?</p>", unsafe_allow_html=True)
        
        tone = st.radio(
            "Tone", 
            ["Grateful", "Polite & Firm", "Short"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # 4. The Button - We use the native form submit but styled via CSS above
        submitted = st.form_submit_button("Generate reply")
        
        if submitted and review_text:
            try:
                system_prompt = f"""
                You are a business owner. Write a response to a review.
                Business Name: {business_name if business_name else 'The Business'}
                Tone: {tone}
                Rules: Polite, professional, under 60 words. No platform names.
                Return ONLY the text.
                """
                
                message = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    system=system_prompt,
                    messages=[{"role": "user", "content": review_text}]
                )
                
                st.session_state.reply = message.content[0].text
                st.session_state.page = "result"
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")

elif st.session_state.page == "result":
    
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #000; font-weight: 600; font-size: 24px; margin-top: 20px;'>Your reply</h3>", unsafe_allow_html=True)
    
    # Result Display
    st.markdown(f"""
    <div class="result-box">
        {st.session_state.reply}
    </div>
    """, unsafe_allow_html=True)
    
    # "Reply to Another" Button
    # We create a centered container for the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Reply to another", type="primary"):
            st.session_state.page = "home"
            st.session_state.reply = ""
            st.rerun()
