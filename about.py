import streamlit as st
from utils.show_button import show_logout_button

def app():
    show_logout_button()
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
            display: flex;
            flex-direction: column;
            height: 100vh;
            justify-content: space-between;
        }
        .header-style {
            color: #fff;
            padding: 1rem;
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .subheader-style {
            font-size: 1.8em;
            text-align: center;
            font-weight: bold;
            color: #fff;
            margin-bottom: 1rem;
        }
        .footer-style {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 0 1rem;
            color: #fff;
            text-align: center;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="header-style">HostGuard</div>', unsafe_allow_html=True)
    st.markdown('HostGuard is a website created for users to track and monitor changes made to local \
                 directories & actively send alerts to the admin.', unsafe_allow_html=True)
    st.markdown('<div class="subheader-style">How it works?</div>', unsafe_allow_html=True)
    st.markdown("This application monitors changes in a specified folder on your computer by finding all files within it \
    and generating unique codes, called MD5 hashes, for each file's content. \
    It then saves these file names and hashes in text files for future reference. \
    When run again, the script compares the current files and hashes with the saved ones to detect any changes, \
    such as new files, modifications, or deletions. It provides a report of these changes, \
    making it useful for keeping track of folder activity and detecting any unauthorized alterations.", unsafe_allow_html=True)

    # Footer with name and email
    st.markdown(
        """
        <div class="footer-style">
            Created by: Onyeabor Chiagozie Daniel<br>
            Contact via mail: <a href="mailto:danikuldaniel@gmail.com">danikuldaniel@gmail.com</a>
        </div>
        """,
        unsafe_allow_html=True
    )
