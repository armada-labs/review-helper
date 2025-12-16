import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(page_title="Review Responder", page_icon="✨", layout="centered")

# 2. Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reply" not in st.session_state:
    st.session_state.reply = ""

# 3. THE "PIXEL PERFECT" CSS
st.markdown("""
<style>
    /* GLOBAL CLEANUP */
    .stApp {
        background-color: #FFFFFF !important;
    }
    .block-container {
        max-width: 680px !important;
        padding-top: 4rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* REMOVE THE UGLY FORM BORDER */
    [data-testid="stForm"] {
        border: 0px solid transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* TEXT STYLING */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        color: #000000 !important;
        padding-bottom: 0px !important;
    }
    p {
        text-align: center !important;
        color: #666666 !important;
        font-size: 1rem !important;
        margin-bottom: 2rem !important;
    }

    /* INPUT FIELDS (Clean & Soft) */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important; /* Very light gray */
        border-radius: 8px !important;
        color: #111827 !important;
        font-size: 15px !important;
        padding: 12px !important;
        box-shadow: none !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #6366F1 !important; /* Periwinkle focus */
        box-shadow: 0 0 0 1px #6366F1 !important;
    }

    /* RADIO BUTTONS (The "Card" Look) */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center; /* Center them */
        gap: 12px;
        width: 100%;
        margin-top: 10px;
    }
    
    /* The individual option container */
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        width: auto !important;
        flex-grow: 0 !important; /* Don't stretch */
        transition: all 0.2s;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Hover effect */
    div[role="radiogroup"] label:hover {
        border-color: #6366F1 !important;
        color: #6366F1 !important;
    }

    /* THE BLUE BUTTON (Exact Match) */
    div.stButton > button {
        background-color: #6366F1 !important; /* Periwinkle Blue */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        margin: 20px auto 0px auto !important; /* Center horizontally */
        display: block !important;
        width: 200px !important;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3) !important;
    }
    div.stButton > button:hover {
        background-color: #4F46E5 !important; /* Darker on hover */
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Hide the Streamlit footer/header */
    header, footer, #MainMenu {display: none !important;}

</style>
""", unsafe_allow_html=True)

# 4. API SETUP
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except:
    pass

# 5. UI LOGIC
if st.session_state.page == "home":
    
    # Custom Header (Centered)
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)

    with st.form("main_form", clear_on_submit=False):
        
        # Review Input
        review_text = st.text_area(
            "Review",
            height=160, 
            placeholder="Paste the customer review here...",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # Business Name Input
        business_name = st.text_input(
            "Business Name", 
            placeholder="Add your business name (optional)",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # Tone Header
        st.markdown("<p style='margin-bottom: 8px !important;'>What tone would you like to reply with?</p>", unsafe_allow_html=True)
        
        # Tone Selection
        tone = st.radio(
            "Tone", 
            ["Grateful", "Polite & Firm", "Short"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Submit Button
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
    
    # Header
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)
    
    # Result Area
    st.markdown("<h2 style='text-align: center; font-size: 1.8rem; margin-top: 1rem;'>Your reply</h2>", unsafe_allow_html=True)
    
    # The Blue Result Box
    st.markdown(f"""
    <div style="
        background-color: #F8FAFC; 
        border: 1px solid #EEF2FF; 
        border-radius: 12px; 
        padding: 30px; 
        color: #334155; 
        font-size: 16px; 
        line-height: 1.6; 
        margin: 20px 0 40px 0;
        text-align: left;">
        {st.session_state.reply}
    </div>
    """, unsafe_allow_html=True)
    
    # Back Button
    if st.button("Reply to another"):
        st.session_state.page = "home"
        st.session_state.reply = ""
        st.rerun()
