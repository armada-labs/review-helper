import streamlit as st
import anthropic

# 1. Page Config (Browser Tab)
st.set_page_config(
    page_title="Review Responder",
    page_icon="✨",
    layout="centered"
)

# 2. THE STYLING (The Magic Part)
# We inject CSS to override Streamlit's defaults.
st.markdown("""
<style>
    /* Force a dark background color to match the reference */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* 1. ROUNDED TEXT AREA (The Input) */
    .stTextArea textarea {
        background-color: #262730;
        color: #ffffff;
        border-radius: 12px; /* Rounded corners */
        border: 1px solid #41424C; /* Subtle border */
    }
    .stTextArea textarea:focus {
        border-color: #4CAF50; /* Green glow on focus */
        box-shadow: 0 0 0 1px #4CAF50;
    }

    /* 2. THE BUTTON (No more Red!) */
    div.stButton > button:first-child {
        background-color: #24A19C; /* Calm Teal color */
        color: white;
        border-radius: 20px; /* Pill shape */
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%; /* Full width for mobile friendliness */
    }
    
    div.stButton > button:first-child:hover {
        background-color: #1B7F7A; /* Darker teal on hover */
        transform: translateY(-2px); /* Slight lift effect */
        box-shadow: 0 4px 12px rgba(36, 161, 156, 0.3);
    }

    /* 3. RADIO BUTTONS (The Tones) */
    /* Make them look like cards or cleaner text */
    div[role="radiogroup"] > label {
        background-color: #262730;
        padding: 8px 16px;
        border-radius: 8px;
        margin-right: 8px;
        border: 1px solid #41424C;
        transition: border-color 0.2s;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #24A19C;
    }

    /* 4. RESULT BOX */
    .stAlert {
        background-color: #262730;
        border: 1px solid #41424C;
        border-radius: 12px;
        color: #FAFAFA;
    }

    /* Hide the default Streamlit main menu and footer for a cleaner look */
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
    <p style='color: #9CA3AF; font-size: 1.1rem; margin-bottom: 2rem;'>
    Paste a review below from any platform. I'll write a calm, professional reply for you.
    </p>
    """, 
    unsafe_allow_html=True
)

# 5. The Input Form
with st.form("review_form"):
    review_text = st.text_area(
        "Customer Review", # Label is required but we can hide it with CSS if you prefer, keeping it for accessibility
        height=120, 
        placeholder="Paste the review text here...",
        label_visibility="collapsed" # Hides the label for that "clean search bar" look
    )
    
    st.markdown("#### Choose your vibe:")
    tone = st.radio(
        "Tone", 
        ["🙏 Grateful", "🤝 Polite & Firm", "⚡ Short"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Simple spacer
    st.write("")
    
    business_name = st.text_input(
        "Business Name (Optional)", 
        placeholder="Your Business Name (e.g. Andy's Cafe)",
        label_visibility="collapsed"
    )
    
    st.write("") # Spacer
    
    # The Button (Styled via CSS above)
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
            - Do NOT mention specific platform names unless the user explicitly mentioned it.
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
            
            st.markdown("---") # Thin divider
            st.markdown("### ✅ Your Draft")
            
            # We use st.code because it is the only way to get a 'Copy' button natively
            st.code(reply, language="text")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")