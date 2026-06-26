import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv("api_key.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


st.set_page_config(
    page_title="AI Fake News and scam Detection",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI Fake News And Scam Detection System")
st.write("Paste any news article, headline, WhatsApp forward, or social media claim below.")

system_prompt = """
You are an expert AI Fake News and Scam Detection Assistant.

The user may provide:
1. A news article.
2. A headline.
3. A social media post.
4. A WhatsApp forward.
5. A screenshot or image.
6. A suspicious email, SMS, website, QR code, investment offer, job offer, or online message.

Analyze all provided information carefully.

Identify whether it appears to be:
- REAL
- FAKE
- MISLEADING
- SCAM
- PHISHING
- UNCERTAIN

If it appears to be a scam or phishing attempt, explain the warning signs, identify any suspicious tactics (urgency, requests for money, fake links, impersonation, etc.), and advise the user on how to stay safe.

Always reply in this format:

Verdict:
REAL / FAKE / MISLEADING / SCAM / PHISHING / UNCERTAIN

Confidence:
0–100%

Reasons:
• Point 1
• Point 2
• Point 3

Advice:
Explain how the user can verify the information and what precautions to take.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    system_instruction=system_prompt
)


news = st.text_area(
    "Paste News Here",
    height=250
)

uploaded_image = st.file_uploader(
    "📷 Upload News Image (Optional)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)






if st.button("Analyze News"):
     if news.strip() == "" and uploaded_image is None:
        st.warning("Please paste some news or upload an image.")
        st.stop()

     with st.spinner("Analyzing..."):
         if uploaded_image:
            image_data = {
                "mime_type": uploaded_image.type,
                "data": uploaded_image.getvalue()
            }

            prompt = f"""
            Analyze the following news text and the uploaded image together.

            News:
            {news}
            """

            response = model.generate_content([prompt, image_data])

         else:
            response = model.generate_content(news)

     st.success("Analysis Completed")
 

     st.markdown("## 📋 Result")

     st.write(response.text)