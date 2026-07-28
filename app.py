import streamlit as st
from supabase import create_client
from datetime import datetime

SUPABASE_URL = "https://dytytdxoihelpgtavsvb.supabase.co"
SUPABASE_KEY = "sb_publishable_jzIDCwW6cU_t-vCiUsrK7g_0RfE-IOv"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Ka Chat App", page_icon="💬")
st.title("💬 Ka Live Chat App")

# ========== LOGIN/SIGNUP ==========
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Login", "Signup"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("Login a dik lo")
    
    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Signup"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("Signup a hlawhtling! Email check rawh")
            except Exception as e:
                st.error("Email hi a lo awm tawh")
else:
    st.write(f"Welcome, {st.session_state.user.email}")
    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
    
    st.divider()
    # Heta tang hian message form a kal chhunzawm
    with st.form("message_form", clear_on_submit=True):
        message = st.text_input("I message")
        submitted = st.form_submit_button("Thawn 🔥")
        if submitted and message:
            data = {
                "name": st.session_state.user.email,
                "message": message,
                "created_at": datetime.now().isoformat()
            }
            supabase.table("messages").insert(data).execute()
            st.rerun()

    # Message en na...
