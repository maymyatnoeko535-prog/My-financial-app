import streamlit as st
import pandas as pd
from datetime import date

# App ရဲ့ ခေါင်းစဉ်နဲ့ ပုံစံကို သတ်မှတ်ခြင်း
st.set_page_config(page_title="Money Tracker", page_icon="💰")

st.title("💰 နေ့စဉ်သုံးငွေ မှတ်တမ်း")
st.markdown("---")

# အချက်အလက်များကို ခေတ္တသိမ်းဆည်းရန် (Session State)
if 'balance' not in st.session_state:
    st.session_state.balance = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

# --- ၁။ အသုံးစရိတ် ကြိုတင်သတ်မှတ်ခြင်း ---
with st.sidebar:
    st.header("⚙️ Settings")
    new_budget = st.number_input("လစာ သို့မဟုတ် အသုံးစရိတ် သတ်မှတ်ရန်", min_value=0.0, step=1000.0)
    if st.button("သတ်မှတ်မည်"):
        st.session_state.balance = new_budget
        st.success(f"ယခုလအတွက် {new_budget:,.0f} MMK သတ်မှတ်ပြီးပါပြီ။")

# --- ၂။ လက်ကျန်ငွေ ပြသခြင်း ---
st.subheader("📊 လက်ရှိအခြေအနေ")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="လက်ကျန်ငွေ", value=f"{st.session_state.balance:,.0f} MMK")

# --- ၃။ အသုံးစရိတ်အသစ် ထည့်သွင်းခြင်း ---
st.subheader("📝 အသုံးစရိတ်အသစ် ထည့်ရန်")
with st.form("expense_form", clear_on_submit=True):
    amount = st.number_input("သုံးလိုက်သည့် ပမာဏ", min_value=0.0, step=500.0)
    note = st.text_input("အကြောင်းအရာ (ဥပမာ - နေ့လည်စာ၊ ကားခ)")
    submit_button = st.form_submit_button("စာရင်းသွင်းမည်")

    if submit_button:
        if amount > 0:
            st.session_state.balance -= amount
            # မှတ်တမ်းထဲ ထည့်ခြင်း
            new_entry = {
                "ရက်စွဲ": date.today().strftime("%d-%m-%Y"),
                "အကြောင်းအရာ": note,
                "ပမာဏ": amount
            }
            st.session_state.history.insert(0, new_entry) # အသစ်ကို အပေါ်ဆုံးကပြရန်
            st.rerun()
        else:
            st.warning("ကျေးဇူးပြု၍ ပမာဏတစ်ခုခု ရိုက်ထည့်ပါ။")

# --- ၄။ သုံးစွဲမှုမှတ်တမ်း ဇယားပြသခြင်း ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 သုံးစွဲမှုမှတ်တမ်း")
    df = pd.DataFrame(st.session_state.history)
    st.table(df)
else:
    st.info("မှတ်တမ်း မရှိသေးပါ။")
