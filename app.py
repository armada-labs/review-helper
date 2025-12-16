import streamlit as st
import anthropic

# 1. Page Configuration
st.set_page_config(
    page_title="Review Response Helper",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .stTextArea textarea {font-size: 16px !important;}
    div[data-testid="stMarkdownContainer"] p {font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

# 2. The Header - NOW GENERIC
st.title("✨ The Universal Review Responder")
st.markdown("Paste a review from **any platform** (Google, Facebook, TripAdvisor, Checkatrade, etc.), and I'll write a professional reply instantly.")

# 3. Securely load API Key
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception as e:
    st.error("No API Key found. Please add ANTHROPIC_API_KEY to your secrets.")
    st.stop()

# 4. The Input Form
with st.form("review_form"):
    review_text = st.text_area("Paste the customer review here:", height=150, placeholder="e.g. The service was fast but the price was a bit high...")
    
    # Updated Tones
    tone = st.radio("Choose your tone:", ["🙏 Grateful & Professional", "🤝 Polite & Firm (for unfair reviews)", "⚡ Short & Friendly"], horizontal=True)
    
    business_name = st.text_input("Your Business Name (Optional):", placeholder="e.g. Ealing Plumbing & Heating")
    
    submitted = st.form_submit_button("✨ Generate Reply", type="primary")

# 5. The Magic
if submitted and review_text:
    with st.spinner("Drafting the perfect response..."):
        try:
            # Platform-agnostic prompt
            system_prompt = f"""
            You are a professional business owner.
            Write a response to a customer review.
            Business Name: {business_name if business_name else 'The Business'}
            Tone: {tone}
            
            Rules:
            - Be polite, empathetic, and professional.
            - Do NOT mention specific platform names (like 'Thanks for the Google review') unless the user explicitly mentioned it.
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
            
            # 6. Improved Output UI
            st.markdown("### ✅ Here is your reply:")
            st.info(reply, icon="✍️")
            
            st.code(reply, language=None)
            st.caption("👆 Click the copy icon in the top right of the box above to copy.")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")