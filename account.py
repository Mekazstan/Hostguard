import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import os
import bcrypt
from dotenv import load_dotenv
from utils.show_button import show_logout_button

# Load the environment variables from .env file
load_dotenv()

# Access the configuration variables
cookie_name = os.getenv('COOKIE_NAME')
cookie_key = os.getenv('COOKIE_KEY')

# Assume you have a boolean flag indicating successful login
successful_login = False

# Initialize the SQLite database connection
conn = sqlite3.connect('hostguard.db', check_same_thread=False)
c = conn.cursor()

# Create table to store user data
def create_users_table():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, email TEXT)')

# Add user to the SQLite database
def add_userdata(username, password, email):
    c.execute('INSERT INTO userstable(username, password, email) VALUES (?, ?, ?)', (username, password, email))
    conn.commit()
    
# Function to check if the email already exists in the database
def email_exists(email):
    c.execute('SELECT * FROM userstable WHERE email = ?', (email,))
    return c.fetchone() is not None

# Authenticate user
def login_user(email, password):
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')
    
    # Retrieve the user's data
    c.execute('SELECT * FROM userstable WHERE email = ?', (email,))
    user_data = c.fetchone()
    # If user_data is not None, then the email exists in the database
    if user_data:
        print('1')
        # user_data[1] is the index for the password in the database
        # Check if the hashed password matches the one in the database
        try:
            # Assuming user_data[1] is the hashed password retrieved from the database
            stored_hashed_password = user_data[1]
            # Directly compare the hashed password from the database with the input password
            if bcrypt.checkpw(password_bytes, stored_hashed_password):
                print('2')
                return user_data
        except Exception as e:
            print(f"Error during password comparison: {e}")

    return None

# Main app function
def app():
    show_logout_button()
    st.title('Welcome to HostGuard :shield:')
    
    # Initialize 'usernames' in session state if it doesn't exist
    if 'usernames' not in st.session_state:
        st.session_state['usernames'] = {}

    # Authentication
    authenticator = stauth.Authenticate(
        st.session_state,
        cookie_name,
        cookie_key
    )

    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None

    if st.session_state['authentication_status'] is None:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            create_users_table()
            username = st.text_input("Enter your unique username")
            # Convert the password string to bytes
            password_bytes = password.encode('utf-8')
            
            # Generate a salt
            salt = bcrypt.gensalt()
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            if st.button('Create my account'):
                if not email_exists(email):
                    # Add user data to SQLite database
                    add_userdata(username, hashed_password, email)
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
                else:
                    st.error('An account with this email already exists. Please log in or recover your password.')
        else:
            if st.button('Login'):
                try:
                    # Authenticate user
                    result = login_user(email, password)
                    if result:
                        st.session_state['authentication_status'] = 'Authenticated'
                        st.session_state['username'] = result[0]
                        st.session_state['email'] = result[2]
                        st.success('Logged in as {}. Please navigate to the HomePage from the pane..'.format(email))                     
                    else:
                        st.warning('Incorrect Username/Password')
                except:
                    st.warning('User cannot be found. Try sign up 👍')

    if st.session_state['authentication_status'] == 'Authenticated':
        st.subheader('Welcome to HostGuard, {}!'.format(st.session_state['username']))
    #     # User is logged in, show logout button
    #     if st.button('Logout'):
    #         st.session_state['authentication_status'] = None
    #         st.session_state['username'] = None
    #         st.session_state['email'] = None
    #         st.write('You have been logged out.')

    # Rest of the app code
    # ...

# Run the app
if __name__ == '__main__':
    app()