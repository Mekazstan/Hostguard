import streamlit as st

def show_logout_button():
    if st.session_state.get('authentication_status') == 'Authenticated':
        # Apply styling to your Streamlit app at the beginning
        st.markdown(
            """
            <style>
            .element-container:has(#button-after) + div button {
                /* APPLY YOUR STYLING HERE */
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #dc3545; /* Red color */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                cursor: pointer;
            }
            .element-container:has(#button-after) + div button:hover {
                background-color: #bb2d3b; /* Darker red color on hover */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Insert an empty <span> element with the id 'button-after' before the button you want to style
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

        # Show the logout button
        if st.button('Logout', key='logout'):
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['email'] = None
            st.write('You have been logged out.')
