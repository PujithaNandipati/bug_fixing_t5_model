import streamlit as st
import requests
import psycopg2
import pandas as pd

# --- DATABASE CONFIG ---
DB_CONFIG = {
    "host": "localhost",
    "database": "bug_fix_db",
    "user": "postgres",
    "password": "puji123"  # Change this
}

# --- SESSION STATE INIT ---
if "username" not in st.session_state:
    st.session_state["username"] = None

# --- LOGIN FUNCTION ---
def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username and password:
            # You can replace this with a DB check
            st.session_state["username"] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Please enter both username and password.")

# --- LOAD BUG HISTORY FROM DB ---
def load_bug_fixes():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query("SELECT id, username, code, suggested_fix, bug_type, created_at FROM bugs ORDER BY created_at DESC", conn)
    conn.close()
    return df

# --- BUG FIX DASHBOARD ---
def bug_fix_dashboard():
    st.title("Bug Fix History")
    df = load_bug_fixes()
    st.dataframe(df, use_container_width=True)

# --- BUG FIXER PAGE ---
def bug_fixer():
    st.title("Bug Fixer")

    user_code = st.text_area("Paste your buggy code here:")

    if st.button("Fix My Code"):
        if not user_code.strip():
            st.warning("Please enter some code.")
        else:
            with st.spinner("Sending to AI model..."):
                try:
                    response = requests.post("http://localhost:5000/fix", json={
                        "code": user_code,
                        "user": st.session_state["username"]
                    })
                    result = response.json()

                    if "fixed_code" in result:
                        st.success("Fix received!")
                        st.subheader("Suggested Fix")
                        st.code(result["fixed_code"], language="python")
                    else:
                        st.error("Error: " + result.get("error", "Unknown error"))

                except requests.exceptions.ConnectionError:
                    st.error("Flask API not running. Start the backend server.")

# --- MAIN APP LOGIC ---
def main():
    if not st.session_state["username"]:
        login()
    else:
        st.sidebar.write(f"👤 Logged in as: {st.session_state['username']}")
        page = st.sidebar.radio("Navigate", ["Bug Fixer", "Bug History", "Logout"])

        if page == "Bug Fixer":
            bug_fixer()
        elif page == "Bug History":
            bug_fix_dashboard()
        elif page == "Logout":
            st.session_state["username"] = None
            st.experimental_rerun()

# --- RUN APP ---
if __name__ == "__main__":
    main()
