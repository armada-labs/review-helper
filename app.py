import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(
    page_title="Review Responder",
    page_icon="✨",
    layout="centered"
)

# 2. THE STYLING (Fixed Light Mode)
st.markdown("""
<style>
    /* Force the main app background to soft gray */
    .stApp {
        background-color: #F3F4F6 !important;
    }

    /* TEXT AREAS & INPUTS */
    /* Force white background and dark text */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        color: #111827 !important; /* Dark text */
        caret-color: #111827; /* Dark cursor */
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Input placeholder text color */
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #9CA3AF !important; 
    }

    /* Focus state */
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #24A19C !important;
        box-shadow: 0 0 0 2px rgba(36, 161, 156, 0.2) !important;
    }

    /* LABELS (The 'Choose your vibe' text) */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #1F2937 !important;
    }
    
    /* RADIO BUTTONS (The Tone Cards) */
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5E7EB !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        margin-right: 8px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #24A19C !important;
        color: #24A19C !important;
    }

    /* THE BUTTON (Teal & Pill Shaped) */
    div.stButton > button:first-child {
        background-color: #24A19C !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(36, 161, 156, 0.4) !important;
        width: 100% !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #1D8F8A !important;
        transform: translateY(-1px);
    }
    
    /* Hide extra spacing */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Hide standard elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
st.markdown("Paste a review below. I'll write a calm, professional reply for you.")

# 5. The Input Form
with st.form("review_form"):
    
    # Input Area
    review_text = st.text_area(
        "Review content",
        height=150, 
        placeholder="Paste the review text here...",
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
    
    business_name = st.text_input(
        "Business Name", 
        placeholder="Your Business Name (Optional)",
        label_visibility="collapsed"
    )
    
    st.write("") # Spacer
    
    submitted = st.form_submit_button("Generate Reply")

# 6. The Output
if submitted and review_text:
    with st.spinner("Writing..."):
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
            
            st.caption("Copy the text below:")
            st.code(reply, language="text")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")