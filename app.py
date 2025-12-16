import streamlit as st
import anthropic

# 1. Page Config
st.set_page_config(
    page_title="Review Responder",
    page_icon="✨",
    layout="centered"
)

# 2. THE STYLING (Light Mode "Clean Search" Look)
st.markdown("""
<style>
    /* Main Background - Soft Gray like the reference image */
    .stApp {
        background-color: #F3F4F6;
        color: #1F2937; /* Dark Gray text */
    }

    /* INPUTS: White cards with subtle borders */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Focus state for inputs */
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #24A19C;
        box-shadow: 0 0 0 2px rgba(36, 161, 156, 0.2);
    }

    /* THE BUTTON: Teal, Pill-shaped, and Clean */
    div.stButton > button:first-child {
        background-color: #24A19C;
        color: white;
        border-radius: 50px; /* Full pill shape */
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(36, 161, 156, 0.4);
        transition: all 0.2s;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #1D8F8A;
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(36, 161, 156, 0.5);
    }

    /* RADIO BUTTONS (The Tones) - Light Cards */
    div[role="radiogroup"] > label {
        background-color: #FFFFFF;
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        color: #374151;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        margin-right: 10px;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #24A19C;
        color: #24A19C;
    }
    
    /* Result Box Container */
    .element-container {
        margin-bottom: 1rem;
    }

    /* Hide standard Streamlit header/footer */
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
st.markdown(
    """
    <p style='color: #4B5563; font-size: 1.1rem; margin-bottom: 2rem;'>
    Paste a review below. I'll write a calm, professional reply for you.
    </p>
    """, 
    unsafe_allow_html=True
)

# 5. The Input Form
with st.form("review_form"):
    # We use a white background card approach for the input
    review_text = st.text_area(
        "Review",
        height=150, 
        placeholder="Paste the review text here...",
        label_visibility="collapsed"
    )
    
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
            
            # Using 'st.success' gives a nice green/white box in light mode
            st.success(reply, icon="✍️")
            
            # The Copy Button (Native)
            st.caption("Copy the text below:")
            st.code(reply, language="text")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")