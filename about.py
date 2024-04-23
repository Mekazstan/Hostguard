import streamlit as st

def app():
    st.header('HostGuard is a website created for users to track and monitor changes made to local \
                 directories & actively send alerts to the admin.')
    st.subheader(':blue[How it works?]')
    st.markdown("This application monitors changes in a specified folder on your computer by finding all files within it \
    and generating unique codes, called MD5 hashes, for each file's content. \
    It then saves these file names and hashes in text files for future reference. \
    When run again, the script compares the current files and hashes with the saved ones to detect any changes, \
    such as new files, modifications, or deletions. It provides a report of these changes, \
    making it useful for keeping track of folder activity and detecting any unauthorized alterations.")
    st.markdown('Created by: Onyeabor Chiagozie Daniel')
    st.markdown('Contact via mail: [danikuldaniel@gmail.com]')
    