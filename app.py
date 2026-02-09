import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# PASTE YOUR MAKE.COM WEBHOOK URL HERE
WEBHOOK_URL = "https://hook.eu1.make.com/owa3p5nqer5mt7hnuh92ctd1pii2r5u2"

st.set_page_config(page_title="Insurance Assistant", page_icon="🤖")

# --- CHATBOT UI SETUP ---
st.title("🤖 Insurance Assistant")
st.caption("I calculate premiums using income replacement method.")

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
        with st.spinner("Consulting our AI powered brain..."):
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
                
                response = requests.post(WEBHOOK_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 3. THE PRO DESIGN HTML CARD (Sections A, B, C)
                    html_card = f"""
                    <div style="font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f4f7f9; padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">

                      <div style="display: flex; gap: 15px; margin-bottom: 20px; flex-wrap: wrap;">

                        <div style="flex: 1; min-width: 200px; background-color: #ffffff; border: 1px solid #e1e8ed; border-radius: 12px; padding: 15px;">
                          <h3 style="margin: 0 0 12px 0; color: #1565c0; font-size: 16px; font-weight: 700;">👤 User Profile</h3>
                          <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; border-bottom: 1px dashed #eee;">
                            <span style="color: #666;">Name:</span> <span style="font-weight: 600; color: #333;">{name}</span>
                          </div>
                          <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; border-bottom: 1px dashed #eee;">
                            <span style="color: #666;">Age:</span> <span style="font-weight: 600; color: #333;">{age} Years</span>
                          </div>
                          <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; border-bottom: 1px dashed #eee;">
                            <span style="color: #666;">Cover Till:</span> <span style="font-weight: 600; color: #333;">{cover_age}</span>
                          </div>
                          <div style="display: flex; justify-content: space-between; font-size: 13px;">
                            <span style="color: #666;">Expenses:</span> <span style="font-weight: 600; color: #333;">₹ {expenses:,}</span>
                          </div>
                        </div>

                        <div style="flex: 1; min-width: 200px; background: linear-gradient(135deg, #0061ff 0%, #60efff 100%); border-radius: 12px; padding: 20px; text-align: center; color: white; display: flex; flex-direction: column; justify-content: center;">
                          <p style="margin: 0; font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">Recommended Cover</p>
                          <h1 style="margin: 8px 0; font-size: 34px; font-weight: 800;">₹ {data.get('cover', '0')} Cr</h1>
                          <div style="background: rgba(255,255,255,0.2); padding: 6px 10px; border-radius: 20px; font-size: 11px; display: inline-block;">
                            Covers inflation adjusted living expenses
                          </div>
                        </div>

                      </div>

                      <div style="background-color: #ffffff; border: 1px solid #e1e8ed; border-radius: 12px; overflow: hidden;">
                        <div style="background-color: #f8faff; padding: 12px 15px; border-bottom: 1px solid #e1e8ed;">
                          <h3 style="margin: 0; color: #444; font-size: 14px; font-weight: 700; text-transform: uppercase;">🏆 Premium Estimates</h3>
                        </div>

                        <div style="display: flex; align-items: center; padding: 15px; border-bottom: 1px solid #f0f0f0;">
                          <div style="width: 40%;">
                            <div style="font-weight: 700; color: #333; font-size: 15px;">HDFC Life</div>
                            <div style="font-size: 11px; color: #2e7d32; background: #e8f5e9; padding: 2px 6px; border-radius: 4px;">99.7% Claim Ratio</div>
                          </div>
                          <div style="width: 60%; text-align: right;">
                            <div style="font-weight: 700; color: #1565c0; font-size: 18px;">₹ {data.get('hdfc', '0')}<span style="font-size: 12px; color: #999; font-weight: 400;">/mo</span></div>
                          </div>
                        </div>

                        <div style="display: flex; align-items: center; padding: 15px; border-bottom: 1px solid #f0f0f0;">
                          <div style="width: 40%;">
                            <div style="font-weight: 700; color: #333; font-size: 15px;">ICICI Pru</div>
                            <div style="font-size: 11px; color: #ef6c00; background: #fff3e0; padding: 2px 6px; border-radius: 4px;">Terminal Illness</div>
                          </div>
                          <div style="width: 60%; text-align: right;">
                            <div style="font-weight: 700; color: #1565c0; font-size: 18px;">₹ {data.get('icici', '0')}<span style="font-size: 12px; color: #999; font-weight: 400;">/mo</span></div>
                          </div>
                        </div>

                        <div style="display: flex; align-items: center; padding: 15px;">
                          <div style="width: 40%;">
                            <div style="font-weight: 700; color: #333; font-size: 15px;">Max Life</div>
                            <div style="font-size: 11px; color: #666; background: #f5f5f5; padding: 2px 6px; border-radius: 4px;">Premium Break</div>
                          </div>
                          <div style="width: 60%; text-align: right;">
                            <div style="font-weight: 700; color: #1565c0; font-size: 18px;">₹ {data.get('max', '0')}<span style="font-size: 12px; color: #999; font-weight: 400;">/mo</span></div>
                          </div>
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
                    st.error(f"Error from Make.com: {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")
