import streamlit as st
import anthropic

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
    # Note: We look for "ANTHROPIC_API_KEY" now
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception as e:
    st.error("No API Key found. Please add ANTHROPIC_API_KEY to your secrets.")
    st.stop()

# 4. The Input Form
with st.form("review_form"):
    review_text = st.text_area("Paste the customer review here:", height=150, placeholder="e.g. The coffee was great but the service was a bit slow...")
    tone = st.radio("Choose your tone:", ["🙏 Grateful & Professional", "😅 Apologetic & Reassuring", "⚡ Short & Sweet"], horizontal=True)
    business_name = st.text_input("Your Business Name (Optional):", placeholder="e.g. Andy's Cafe")
    submitted = st.form_submit_button("✨ Generate Reply")

# 5. The Magic (Claude Generation)
if submitted and review_text:
    with st.spinner("Asking Claude for the perfect response..."):
        try:
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

            message = client.messages.create(
                model="claude-3-haiku-20240307", # Fast and cheap model
                max_tokens=300,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": review_text}
                ]
            )
            
            reply = message.content[0].text
            
            # 6. The Output
            st.success("Here is your reply:")
            st.code(reply, language=None)
            st.caption("Tip: Copy this and paste it straight into Google/Facebook.")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")