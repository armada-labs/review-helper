import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(
    page_title="Review Responder",
    page_icon="✨",
    layout="centered"
)

# 2. THE STYLING (Production Grade)
st.markdown("""
<style>
    /* 1. RESET & BASICS */
    .stApp {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    
    /* Remove standard Streamlit top padding so it fits tight in an iframe */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* HIDE HEADER/FOOTER */
    header, footer, #MainMenu {visibility: hidden !important;}

    /* 2. INPUT FIELDS (Clean, White, Blue Focus) */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
        padding: 12px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }

    /* 3. RADIO BUTTONS (The "Card" Look) */
    /* Container for the cards */
    div[role="radiogroup"] {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    /* The individual cards */
    div[role="radiogroup"] label {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        padding: 10px 20px !important;
        border-radius: 50px !important; /* Pill shape */
        color: #64748B !important;
        transition: all 0.2s ease;
        margin-right: 0px !important;
        cursor: pointer;
    }
    
    /* Hover State */
    div[role="radiogroup"] label:hover {
        border-color: #2563EB !important;
        color: #2563EB !important;
        background-color: #EFF6FF !important;
    }
    
    /* SELECTED STATE (We hijack the internal span to style the active card) */
    /* Note: Streamlit doesn't expose a clean 'checked' class on the label, 
       so we rely on the primaryColor config to handle the dot, 
       and this CSS handles the general card feel. */

    /* 4. THE CTA BUTTON (Welcoming Blue) */
    div.stButton > button:first-child {
        background-color: #2563EB !important; /* SaaS Blue */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important; /* Slightly rounded, professional */
        padding: 14px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: background-color 0.2s;
    }
    div.stButton > button:first-child:hover {
        background-color: #1D4ED8 !important; /* Darker blue on hover */
    }

    /* 5. SUCCESS BOX */
    .stAlert {
        background-color: #EFF6FF !important; /* Very light blue */
        border: 1px solid #DBEAFE !important;
        color: #1E40AF !important;
    }
    
</style>
""", unsafe_allow_html=True)

# 3. Securely load API Key
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception as e:
    st.error("No API Key found. Please add ANTHROPIC_API_KEY to your secrets.")
    st.stop()

# 4. The UI Layout
st.title("✨ Review Responder")
st.markdown("Paste a review below to generate a professional reply.")

# 5. The Input Form
with st.form("review_form"):
    
    # Review Input
    review_text = st.text_area(
        "Review content",
        height=150, 
        placeholder="Paste the customer review here...",
        label_visibility="collapsed"
    )
    
    st.write("") # Spacer
    
    st.markdown("#### Choose your vibe:")
    tone = st.radio(
        "Tone", 
        ["🙏 Grateful", "🤝 Polite & Firm", "⚡ Short"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.write("") # Spacer
    
    # Business Name
    business_name = st.text_input(
        "Business Name", 
        placeholder="Your Business Name (Optional)",
        label_visibility="collapsed"
    )
    
    st.write("") # Spacer
    
    submitted = st.form_submit_button("Generate Reply")

# 6. The Output
if submitted and review_text:
    with st.spinner("Drafting..."):
        try:
            system_prompt = f"""
            You are a professional business owner.
            Write a response to a customer review.
            Business Name: {business_name if business_name else 'The Business'}
            Tone: {tone}
            
            Rules:
            - Be polite, empathetic, and professional.
            - Do NOT mention specific platform names.
            - Keep it under 60 words.
            - Return ONLY the response text.
            """

            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": review_text}
                ]
            )
            
            reply = message.content[0].text
            
            st.markdown("---") 
            st.markdown("### ✅ Your Draft")
            
            st.success(reply, icon="✍️")
            st.code(reply, language="text")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")
