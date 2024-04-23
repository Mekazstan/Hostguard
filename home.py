import streamlit as st
import os
from utils.show_button import show_logout_button

def app():
    show_logout_button()
    # Check if the user is authenticated
    if 'authentication_status' in st.session_state and st.session_state['authentication_status'] == 'Authenticated':
        # Get the username of the currently logged-in user
        username = st.session_state.get('username', 'Guest')
        st.header(f"Hi {username}, Let's help you monitor your files and folders!")

        # Input field for directory path
        directory_path = st.text_input("Enter the directory path to monitor:")

        # Button to initiate monitoring
        if st.button("Start Monitoring"):
            if os.path.isdir(directory_path):
                st.success(f"Monitoring initiated for directory: {directory_path}")
                # Call function to start monitoring process
            else:
                st.error("Invalid directory path. Please enter a valid path.")
    else:
        # If the user is not authenticated, redirect them to the account page
        st.query_params["page"] = "account"
        st.warning("You need to log in to view this page.")
        if st.button("Go to Login"):
            # Update the session state to indicate that the login page should be shown
            st.session_state['show_login'] = True
            # Rerun the app to reflect the changes
            st.experimental_rerun()