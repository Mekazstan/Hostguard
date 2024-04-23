import streamlit as st
import account

def app():
    # Check if the user is authenticated
    if 'authentication_status' in st.session_state and st.session_state['authentication_status'] == 'Authenticated':
        st.header("Welcome to the homepage!")
        # Add the rest of your homepage content here
    else:
        # If the user is not authenticated, redirect them to the account page
        st.query_params["page"] = "account"
        st.warning("You need to log in to view this page.")
        if st.button("Go to Login"):
            # Update the session state to indicate that the login page should be shown
            st.session_state['show_login'] = True
            # Rerun the app to reflect the changes
            st.experimental_rerun()