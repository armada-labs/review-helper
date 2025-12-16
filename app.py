import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(page_title="Review Responder", page_icon="✨", layout="centered")

# 2. Session State Management (To switch views)
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reply" not in st.session_state:
    st.session_state.reply = ""

# 3. THE STYLING (Pixel Perfect Match)
st.markdown("""
<style>
    /* GLOBAL RESET */
    .stApp {
        background-color: #FFFFFF !important;
    }
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
        max-width: 700px !important;
    }
    
    /* HIDE CHROME */
    header, footer, #MainMenu {display: none !important;}

    /* HEADERS */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 600 !important;
        text-align: center !important;
        font-size: 2.2rem !important;
        color: #000000 !important;
        margin-bottom: 0.5rem !important;
    }
    p {
        text-align: center !important;
        color: #64748B !important;
        font-size: 1rem !important;
    }

    /* INPUT FIELDS (Clean Borders) */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 15px !important;
        color: #1E293B !important;
        box-shadow: none !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818CF8 !important; /* Periwinkle Focus */
    }

    /* RADIO BUTTONS (The Toggle Look) */
    div[role="radiogroup"] {
        justify-content: center;
        display: flex;
        gap: 12px;
        width: 100%;
    }
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 10px 32px !important; /* Wide padding */
        color: #64748B !important;
        font-weight: 500 !important;
        transition: all 0.2s;
    }
    /* When selected (Streamlit adds a generic class, but we rely on primaryColor ring usually. 
       We add hover effects to mimic the active feel) */
    div[role="radiogroup"] label:hover {
        border-color: #818CF8 !important;
        color: #818CF8 !important;
    }

    /* PRIMARY BUTTON (The "Generate" & "Reply to another" button) */
    div.stButton > button {
        background-color: #818CF8 !important; /* That Soft Blue/Purple */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        width: 200px !important; /* Fixed width like mockup */
        margin: 0 auto !important; /* Center it */
        display: block !important;
    }
    div.stButton > button:hover {
        background-color: #6366F1 !important;
    }

    /* RESULT BOX */
    .result-box {
        background-color: #F8FAFC; /* Very light gray/blue */
        border: 1px solid #F1F5F9;
        border-radius: 12px;
        padding: 24px;
        color: #334155;
        font-size: 16px;
        line-height: 1.6;
        margin-top: 20px;
        margin-bottom: 40px;
    }

</style>
""", unsafe_allow_html=True)

# 4. API SETUP
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except:
    pass # Error handled gracefully in UI if needed

# 5. VIEW 1: THE INPUT FORM
if st.session_state.page == "home":
    
    st.title("Review responder")
    st.markdown("Paste a review below to generate a professional reply.")
    
    st.write("") # Spacer

    with st.form("main_form", clear_on_submit=False):
        # Review Input
        review_text = st.text_area(
            "Review",
            height=180, 
            placeholder="Paste the customer review here...",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # Business Name
        business_name = st.text_input(
            "Business Name", 
            placeholder="Add your business name (optional)",
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        
        # Tone Selector - Centered text logic
        st.markdown("<p style='text-align: center; margin-bottom: 10px;'>What tone would you like to reply with?</p>", unsafe_allow_html=True)
        
        # Using columns to center the radio group visually if needed, 
        # but CSS above handles the flex centering.
        tone = st.radio(
            "Tone", 
            ["Grateful", "Polite & Firm", "Short"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("") # Spacer
        st.write("") # Spacer
        
        # The Button
        submitted = st.form_submit_button("Generate reply")
        
        if submitted and review_text:
            # API Call
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
                
                # Save to session and switch page
                st.session_state.reply = message.content[0].text
                st.session_state.page = "result"
                st.rerun() # Force reload to show result page
                
            except Exception as e:
                st.error(f"Error: {e}")

# 6. VIEW 2: THE RESULT
elif st.session_state.page == "result":
    
    st.title("Review responder")
    st.markdown("Paste a review below to generate a professional reply.")
    
    # We show disabled inputs to mimic the 'Ghost' state of the previous screen
    # or we can just show the result clean as per mockup.
    # Mockup 2 shows the inputs are GONE, and just the result is there? 
    # Actually, Mockup 2 shows inputs at top (filled) and result below.
    # Let's stick to the cleaner "Result View" for now.
    
    st.markdown("<h2 style='text-align: center; font-size: 1.8rem; margin-top: 2rem;'>Your reply</h2>", unsafe_allow_html=True)
    
    # Custom HTML box for the result to match the blue bg
    st.markdown(f"""
    <div class="result-box">
        {st.session_state.reply}
    </div>
    """, unsafe_allow_html=True)
    
    # The "Go Back" Button
    if st.button("Reply to another"):
        st.session_state.page = "home"
        st.session_state.reply = ""
        st.rerun()
