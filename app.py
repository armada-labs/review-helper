import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(page_title="Review Responder", page_icon="✨", layout="centered")

# 2. Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reply" not in st.session_state:
    st.session_state.reply = ""
if "review_text" not in st.session_state:
    st.session_state.review_text = ""
if "business_name" not in st.session_state:
    st.session_state.business_name = ""

# 3. CSS INJECTION
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
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        color: #6B7280 !important;
        font-size: 16px !important;
        text-align: center;
        margin-bottom: 2.5rem !important;
    }

    /* INPUTS (Text Area & Input) - with drop shadow */
    .stTextArea textarea, .stTextInput input {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        color: #374151 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06) !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #7C90FF !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 0 0 3px rgba(124, 144, 255, 0.15) !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder { 
        color: #9CA3AF !important; 
        opacity: 1; 
    }

    /* RADIO BUTTONS CONTAINER - center the whole group */
    [data-testid="stHorizontalBlock"]:has([role="radiogroup"]) {
        justify-content: center !important;
    }
    
    [role="radiogroup"] {
        justify-content: center !important;
        gap: 16px !important;
        display: flex !important;
        width: 100% !important;
    }
    
    /* Fix spacing inside cards */
    [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0px !important;
    }

    /* This targets the label box */
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        min-width: 130px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
    }

    /* Hover State */
    div[role="radiogroup"] label:hover {
        border-color: #7C90FF !important;
    }

    /* Selected State (Blue Border + Blue Text) */
    div[role="radiogroup"] label:has(input:checked) {
        border-color: #7C90FF !important;
        background-color: #F8F9FF !important;
    }
    
    div[role="radiogroup"] label:has(input:checked) p {
        color: #7C90FF !important;
    }
    
    /* Hide the actual radio circle completely */
    div[role="radiogroup"] label > div:first-child {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Text inside the radio button - ensure centered */
    div[role="radiogroup"] label p {
        font-weight: 500 !important;
        font-size: 15px !important;
        margin: 0 !important;
        padding: 0 !important;
        color: #374151 !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Target the inner div that wraps the text */
    div[role="radiogroup"] label > div:last-child {
        width: 100% !important;
        text-align: center !important;
    }

    /* TONE QUESTION TEXT */
    .tone-question {
        color: #6B7280 !important;
        font-size: 15px !important;
        text-align: center;
        margin-bottom: 24px !important;
    }

    /* THE GENERATE BUTTON - centered */
    [data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 16px !important;
    }
    
    [data-testid="stFormSubmitButton"] button {
        background-color: #7C90FF !important;
        color: white !important;
        border: none !important;
        padding: 14px 40px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        width: 200px !important;
        transition: background-color 0.2s;
        box-shadow: 0 4px 6px -1px rgba(124, 144, 255, 0.25) !important;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #6A7FD6 !important;
    }
    
    [data-testid="stFormSubmitButton"] button:active {
        transform: translateY(1px);
    }
    
    /* STANDARD BUTTON (Reply to another) - centered */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #7C90FF !important;
        color: white !important;
        border: none !important;
        padding: 14px 40px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        width: 200px !important;
        transition: background-color 0.2s;
        box-shadow: 0 4px 6px -1px rgba(124, 144, 255, 0.25) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #6A7FD6 !important;
    }
    
    /* Display boxes (for showing review on result page) */
    .display-box {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px 24px;
        color: #374151;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 16px;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
    }
    
    .display-box-single {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 14px 24px;
        color: #374151;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 24px;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
    }
    
    /* Result Box (Your Reply section) */
    .result-box {
        background-color: #F8F9FF;
        border: 1px solid #E8EBFF;
        border-radius: 12px;
        padding: 24px 28px;
        color: #374151;
        font-size: 15px;
        line-height: 1.7;
        margin: 16px 0 40px 0;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
    }
    
    /* Section heading */
    .section-heading {
        color: #000000;
        font-weight: 600;
        font-size: 28px;
        text-align: center;
        margin-top: 32px;
        margin-bottom: 16px;
    }
    
    /* Button container */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 16px;
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
    st.markdown("<p class='subtitle'>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)

    with st.form("main_form", clear_on_submit=False):
        
        # 1. Review Input
        review_text = st.text_area(
            "Review",
            height=180, 
            placeholder="Paste the customer review here...",
            label_visibility="collapsed"
        )
        
        st.write("")
        
        # 2. Business Name
        business_name = st.text_input(
            "Business Name", 
            placeholder="Add your business name (optional)",
            label_visibility="collapsed"
        )
        
        st.write("")
        
        # 3. Tone Selector
        st.markdown("<p class='tone-question'>What tone would you like to reply with?</p>", unsafe_allow_html=True)
        
        tone = st.radio(
            "Tone", 
            ["Grateful", "Polite & Firm", "Short"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("")
        
        # 4. Submit Button
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
                st.session_state.review_text = review_text
                st.session_state.business_name = business_name
                st.session_state.page = "result"
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")

elif st.session_state.page == "result":
    
    st.markdown("<h1>Review responder</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Paste a review below to generate a professional reply.</p>", unsafe_allow_html=True)
    
    # Show the original review
    st.markdown(f"""
    <div class="display-box">
        {st.session_state.review_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Show business name if provided
    if st.session_state.business_name:
        st.markdown(f"""
        <div class="display-box-single">
            {st.session_state.business_name}
        </div>
        """, unsafe_allow_html=True)
    
    # Your Reply heading
    st.markdown("<h2 class='section-heading'>Your reply</h2>", unsafe_allow_html=True)
    
    # Result Display
    st.markdown(f"""
    <div class="result-box">
        {st.session_state.reply}
    </div>
    """, unsafe_allow_html=True)
    
    # "Reply to Another" Button - centered via CSS
    if st.button("Reply to another", type="primary"):
        st.session_state.page = "home"
        st.session_state.reply = ""
        st.session_state.review_text = ""
        st.session_state.business_name = ""
        st.rerun()
