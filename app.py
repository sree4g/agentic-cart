import streamlit as st
from google import genai

st.set_page_config(page_title="AgenticCart - AI Upsell & Checkout", page_icon="🛒", layout="centered")

st.title("🛒 AgenticCart: Autonomous Upsell & Checkout Agent")
st.caption("AI-powered cart companion that recommends complementary items and generates dynamic checkout actions.")

# Input API Key securely via UI
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# Merchant catalog context
CATALOG = """
- Product: Pro Running Shoes (₹2,999) | Category: Footwear
- Product: Anti-Sweat Compression Socks (₹399) | Category: Apparel (Frequently paired with Running Shoes)
- Product: Insulated Steel Water Bottle (₹599) | Category: Accessories (Frequently paired with Running Shoes)
- Product: Smart Fitness Band (₹1,999) | Category: Electronics
"""

st.subheader("1. Merchant Cart Setup")
selected_product = st.selectbox(
    "Select item currently in customer's cart:",
    ["Pro Running Shoes (₹2,999)", "Smart Fitness Band (₹1,999)"]
)

user_intent = st.text_input(
    "Customer prompt / chat message:",
    value="I am about to check out. Do you recommend anything else before I pay?"
)

if st.button("Generate Agentic Upsell & Checkout"):
    if not api_key:
        st.error("Please provide a Gemini API Key to run the agent.")
    else:
        with st.spinner("AI Agent analyzing cart and generating response..."):
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an autonomous e-commerce checkout assistant.
            Available Catalog:
            {CATALOG}

            Customer's Current Cart Item: {selected_product}
            Customer's Message: {user_intent}

            Your tasks:
            1. Recommend the single best complementary product from the catalog.
            2. Give a brief, persuasive reason explaining why it complements their cart.
            3. Provide a formatted mock checkout summary including total calculated cost.
            4. Add a clear call-to-action link button text (e.g. [Pay with Razorpay]).
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            st.markdown("### Agent Output")
            st.info(response.text)
