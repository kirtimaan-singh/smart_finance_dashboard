import streamlit as st

USER_CREDENTIALS = {
    "admin": "admin123",
    "finance_user": "finance2026"
}

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("<h2 style='text-align: center; color: #00D2FF;'>Smart Business Finance Login</h2>", unsafe_allow_html=True)
    
    with st.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid Username or Password")
    return False

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()
