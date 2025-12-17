import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(page_title="Review Responder", page_icon="✨", layout="centered")

# 2. Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reply" not in st.session_state:
    st.session_state.reply = ""

# 3. THE DESIGN SYSTEM (CSS Injection)
st.markdown("""
<style>
    /* IMPORT FONT: Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* 1. GLOBAL RESET */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp {
        background-color: #FFFFFF !important;
    }
    /* Constrain width to look like an App, not a website */
    .block-container {
        max-width: 600px !important;
        padding-top: 5rem !important;
        padding-bottom: 2rem !important;
    }
    /* Hide Header/Footer */
    header, footer, #MainMenu {display: none !important;}
    
    /* Remove default Form styling */
    [data-testid="stForm"] {border: none !important; padding: 0 !important;}

    /* 2. TYPOGRAPHY */
    h1 {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 32px !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }
    /* The "Subtitle" text */
    p, .stMarkdown p {
        color: #6F6F6F !important;
        font-size: 16px !important;
        text-align: center;
        line-height: 1.5;
    }
    
    /* 3. INPUT FIELDS (Review & Business Name) */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        color: #1F2937 !important;
        box-shadow: none !important;
    }
    /* Focus State: The Purpley Blue */
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #7C90FF !important;
        box-shadow: 0 0 0 3px rgba(124, 144, 255, 0.1) !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #9CA3AF !important;
    }

    /* 4. TONE SELECTOR (The "Cards") */
    /* This transforms the radio buttons into clickable rectangles */
    div[role="radiogroup"] {
        gap: 12px;
        display: flex;
        justify-content: center;
        margin-bottom: 24px;
    }
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        cursor: pointer;
        transition: all 0.2s ease;
        
        /* HACK: Center text and remove the radio circle space */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Hide the default radio circle */
    div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }
    
    /* SELECTED STATE (Uses the :has selector) */
    div[role="radiogroup"] label:has(input:checked) {
        border-color: #7C90FF !important;
        background-color: #EEF2FF !important; /* Very faint purple bg */
        color: #7C90FF !important;
        font-weight: 600 !important;
    }
    /* Hover State */
    div[role="radiogroup"] label:hover {
        border-color: #7C90FF !important;
        color: #7C90FF !important;
    }
    /* Force text color inside label */
    div[role="radiogroup"] label p {
        margin: 0 !important;
        font-size: 14px !important;
        color: inherit !important;
    }

    /* 5. PRIMARY BUTTON (Generate Reply) */
    div.stButton > button {
        background-color: #7C90FF !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: opacity 0.2s;
        box-shadow: 0 4px 12px rgba(124, 144, 255, 0.2) !important;
    }
    div.stButton > button:hover {
        opacity: 0.9;
        box-shadow: 0 6px 16px rgba(124, 144, 255, 0.3) !important;
    }
    div.stButton > button:active {
        transform: scale(0.99);
    }
    
    /* RESULT BOX Styling */
    .result-box {
        background-color: #F8FAFC;
        border: 1px solid #F1F5F9;
        border-radius: 12px;
        padding: 24px;
        color: #374151;
        font-size: 16px;
        line-height: 1.6;
        margin: 24px 0;
    }

</style>
""", unsafe_allow_html=True)

# 4. API SETUP
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except:
    pass

# 5. UI LOGIC

# --- HOME VIEW ---
if st.session_state.page == "home":
    
    # Custom HTML Header to ensure colors match exactly
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 32px;'>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)

    with st.form("main_form", clear_on_submit=False):
        
        # 1. Review Input
        review_text = st.text_area(
            "Review",
            height=180, 
            placeholder="Paste the customer review here...",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # 2. Business Name Input
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
        
        # 4. Button
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

# --- RESULT VIEW ---
elif st.session_state.page == "result":
    
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #000; font-weight: 600; margin-top: 20px;'>Your reply</h3>", unsafe_allow_html=True)
    
    # The Result Box
    st.markdown(f"""
    <div class="result-box">
        {st.session_state.reply}
    </div>
    """, unsafe_allow_html=True)
    
    # Back Button
    # We use columns to center the button in Streamlit because st.button is full-width by default in our CSS above
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Reply to another"):
            st.session_state.page = "home"
            st.session_state.reply = ""
            st.rerun()
