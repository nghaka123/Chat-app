import streamlit as st
from supabase import create_client
from datetime import datetime

# ========== 1. SUPABASE CONNECT - KEY DAH SA ==========
SUPABASE_URL = "https://dytytdxoihelpgtavsvb.supabase.co"
SUPABASE_KEY = "sb_publishable_jzIDCwW6cU_t-vCiUsrK7g_0RfE-IOv"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========== 2. PAGE SETTING ==========
st.set_page_config(page_title="Ka Chat App", page_icon="💬")
st.title("💬 Ka Live Chat App")
st.write("Message lo dah ve rawh")

# ========== 3. MESSAGE THAWN NA ==========
with st.form("message_form", clear_on_submit=True):
    name = st.text_input("I hming")
    message = st.text_input("I message")
    submitted = st.form_submit_button("Thawn 🔥")

    if submitted:
        if name and message:
            # Supabase ah dah lut
            data = {
                "name": name,
                "message": message,
                "created_at": datetime.now().isoformat()
            }
            supabase.table("messages").insert(data).execute()
            st.success("I thawn thei e!")
            st.rerun()
        else:
            st.warning("Hming leh Message dah kim rawh")

st.divider()

# ========== 4. MESSAGE EN NA ==========
st.subheader("📨 Message zawng zawng")

# Supabase atang in data la chhuak
try:
    response = supabase.table("messages").select("*").order("created_at", desc=True).limit(50).execute()
    messages = response.data

    if messages:
        for msg in messages:
            time = msg['created_at'].split("T")[1][:5] # 14:30 tiang in
            st.write(f"**{msg['name']}** `[{time}]`: {msg['message']}")
    else:
        st.info("Tuman message an la thawn lo")

except Exception as e:
    st.error(f"Error: {e}")

# ========== 5. REFRESH BUTTON ==========
if st.button("🔄 Refresh"):
    st.rerun()
