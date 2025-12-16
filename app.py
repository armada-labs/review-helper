import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="Ealing Review Helper",
    page_icon="🤖",
    layout="centered"
)

# 2. The Header
st.title("🤖 The Local Business Review Helper")
st.markdown("Paste a Google Review below, and I'll write a professional reply for you instantly.")

# 3. Securely load API Key (from Streamlit Secrets)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("No API Key found. This app is for demo purposes.")
    st.stop()

# 4. The Input Form
with st.form("review_form"):
    # Input: The Customer's Review
    review_text = st.text_area("Paste the customer review here:", height=150, placeholder="e.g. The coffee was great but the service was a bit slow...")
    
    # Input: The Vibe
    tone = st.radio("Choose your tone:", ["🙏 Grateful & Professional", "😅 Apologetic & Reassuring", "⚡ Short & Sweet"], horizontal=True)
    
    # Input: Business Name (Optional)
    business_name = st.text_input("Your Business Name (Optional):", placeholder="e.g. Andy's Cafe")
    
    submitted = st.form_submit_button("✨ Generate Reply")

# 5. The Magic (AI Generation)
if submitted and review_text:
    with st.spinner("Drafting the perfect response..."):
        try:
            # The Prompt Engineering
            system_prompt = f"""
            You are a professional, friendly, and local business owner in Ealing, London.
            Write a response to a customer review.
            Business Name: {business_name if business_name else 'The Business'}
            Tone: {tone}
            
            Rules:
            - Be polite and empathetic.
            - Mention 'Ealing' or 'local' if it feels natural.
            - Keep it under 60 words.
            - Do not use hashtags.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini", # Cheap and fast
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": review_text}
                ],
                temperature=0.7
            )
            
            reply = response.choices[0].message.content
            
            # 6. The Output
            st.success("Here is your reply:")
            st.code(reply, language=None) # formatted as code for one-click copy
            st.caption("Tip: Copy this and paste it straight into Google/Facebook.")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")