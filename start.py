import streamlit as st
import subprocess
import json

page_by_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://media.geeksforgeeks.org/wp-content/uploads/20210724022305/toright-660x322.png");
background-size: cover;
}

[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}

[data-testid="stToolbar"]{
right: 2rem;
}
</style>
"""

st.markdown(page_by_img, unsafe_allow_html = True)

def load_user_database():
    try:
        with open("user_database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user database to file
def save_user_database(user_database):
    with open("user_database.json", "w") as file:
        json.dump(user_database, file)

# Initialize session state
if 'user_database' not in st.session_state:
    st.session_state.user_database = load_user_database()

def register(username, password):
    st.session_state.user_database[username] = password
    save_user_database(st.session_state.user_database)

def login(username, password):
    if username in st.session_state.user_database and st.session_state.user_database[username] == password:
        return True
    else:
        return False

def main():
    st.title("Login Page")

    # Sidebar to switch between login and registration
    mode = st.sidebar.radio("Mode", ("Login", "Register"))

    if mode == "Register":
        st.subheader("Create New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_username in st.session_state.user_database:
                st.error("Username already exists. Please choose another.")
            elif new_password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            else:
                register(new_username, new_password)
                st.success("Registration successful. Please login now.")

    elif mode == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success("Login successful!")

                # Execute the desired Streamlit script using subprocess
                subprocess.Popen(["streamlit", "run", "app.py"])
                # Terminate the current Streamlit script
                raise SystemExit
            else:
                st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
