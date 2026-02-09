import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# We will get this URL from Make.com in the next step.
# For now, keep this placeholder.
WEBHOOK_URL = "https://hook.us1.make.com/REPLACE_ME_LATER"

st.set_page_config(page_title="Insurance Assistant", page_icon="🤖")

# --- CHATBOT UI SETUP ---
st.title("🤖 Insurance Assistant")
st.caption("I calculate premiums using your Google Sheets logic.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I can help you calculate your insurance plan. Please fill in the details in the sidebar and click Calculate."}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "card_html" in message:
            st.html(message["card_html"])

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Your Details")
    name = st.text_input("Name", "Himanshu")
    age = st.number_input("Age", 18, 60, 29)
    cover_age = st.number_input("Cover Till Age", 19, 85, 60)
    expenses = st.number_input("Monthly Expenses (₹)", 10000, 500000, 50000, step=5000)
    smoker = st.selectbox("Smoker?", ["No", "Yes"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    calculate_btn = st.button("Calculate Plan", type="primary")

# --- THE LOGIC ---
if calculate_btn:
    # 1. User message (Visual only)
    st.session_state.messages.append({"role": "user", "content": f"Calculate for {name}, Age {age}, Expenses {expenses}"})
    with st.chat_message("user"):
        st.write(f"Calculate for {name}, Age {age}, Expenses {expenses}")

    # 2. Call Make.com (The "Brain")
    with st.chat_message("assistant"):
        with st.spinner("Consulting the Google Sheet..."):
            try:
                # Send data to Make.com
                payload = {
                    "name": name,
                    "age": age,
                    "cover_age": cover_age,
                    "expenses": expenses,
                    "smoker": smoker,
                    "gender": gender
                }
                
                # Check if URL is still the placeholder
                if "REPLACE_ME" in WEBHOOK_URL:
                    st.error("🚨 Setup Needed: You haven't added the Make.com Webhook URL to app.py yet!")
                    st.stop()

                response = requests.post(WEBHOOK_URL, json=payload)
                
                # Get the JSON answer back
                if response.status_code == 200:
                    data = response.json()
                    
                    # 3. Create the HTML Card
                    html_card = f"""
                    <div style="font-family: sans-serif; background-color: #f4f7f9; padding: 20px; border-radius: 12px; border: 1px solid #ddd;">
                        <div style="background: linear-gradient(135deg, #0061ff 0%, #60efff 100%); padding: 15px; border-radius: 8px; color: white; text-align: center; margin-bottom: 15px;">
                            <p style="margin:0; font-size: 12px; opacity: 0.9;">RECOMMENDED COVER</p>
                            <h2 style="margin: 5px 0;">₹ {data.get('cover', '0')} Cr</h2>
                        </div>
                        <div style="background: white; padding: 10px; border-radius: 8px;">
                            <div style="display:flex; justify-content:space-between; border-bottom:1px solid #eee; padding: 8px 0;">
                                <b>HDFC Life</b> <span style="color:#0061ff; font-weight:bold;">₹ {data.get('hdfc', '0')}/mo</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; border-bottom:1px solid #eee; padding: 8px 0;">
                                <b>ICICI Pru</b> <span style="color:#0061ff; font-weight:bold;">₹ {data.get('icici', '0')}/mo</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; padding: 8px 0;">
                                <b>Max Life</b> <span style="color:#0061ff; font-weight:bold;">₹ {data.get('max', '0')}/mo</span>
                            </div>
                        </div>
                    </div>
                    """
                    
                    st.write(f"Here is the analysis for **{name}**:")
                    st.html(html_card)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"Here is the analysis for **{name}**:",
                        "card_html": html_card
                    })
                else:
                    st.error(f"Error: {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")
