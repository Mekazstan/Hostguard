import streamlit as st
import os
from utils.components import changed_files, create_hashfile, deleted_files, find_files, generate_md5, new_files, read_file
from utils.show_button import show_logout_button
import sqlite3


# Initialize SQLite database connection
conn = sqlite3.connect('hostguard.db')
c = conn.cursor()

# Function to create the file monitoring table if it doesn't exist
def create_file_monitoring_table():
    c.execute('''CREATE TABLE IF NOT EXISTS file_monitoring (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 directory_path TEXT,
                 username TEXT,
                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')
    conn.commit()
    
# Function to insert monitored directory path into the database
def insert_monitored_path(directory_path, username):
    # Check if the directory path already exists
    c.execute("SELECT * FROM file_monitoring WHERE directory_path = ? AND username = ?", (directory_path, username))
    existing_path = c.fetchone()
    if existing_path:
        st.warning("This directory path is already being monitored.")
        return
    
    # If the path is unique, insert it into the database
    create_file_monitoring_table()
    c.execute("INSERT INTO file_monitoring (directory_path, username) VALUES (?, ?)", (directory_path, username))
    conn.commit()
    
# Function to retrieve monitored paths for a specific user
def get_monitored_paths(username):
    c.execute("SELECT directory_path FROM file_monitoring WHERE username=?", (username,))
    monitored_paths = c.fetchall()
    return [path[0] for path in monitored_paths]

# Function to monitor the path
def monitor_path(directory_path):
    # Replace '/' and '\' characters in directory_path with '_'
    filename = directory_path.replace('/', '_').replace('\\', '_')
    
    found_files = find_files(directory_path)
    var_generate_md5 = generate_md5(found_files)
    create_hashfile(directory_path, found_files, var_generate_md5)
    
    if os.path.exists(f"{filename}_0.txt") and os.path.exists(f"{filename}_1.txt"):
        old_file = read_file(f"{filename}_1.txt")
        new_file = read_file(f"{filename}_0.txt")
        
        var_changed_files = changed_files(old_file, new_file)
        var_deleted_files = deleted_files(old_file, new_file)
        var_new_files = new_files(old_file, new_file)
        
        print("Report")
        print("------")
        if var_changed_files == [] and var_deleted_files == [] and var_new_files == []:
            print("There where no changes in the folder")
        else:
            print("WARNING!\n")
            print("NEW FILES")
            print("---------")
            for i in var_new_files:
                print(i)

            print("\n")
            print("CHANGED FILES")
            print("-------------")
            for i in var_changed_files:
                print(i)

            print("\n")
            print("REMOVED FILES")
            print("-------------")
            for i in var_deleted_files:
                print(i)

def app():
    show_logout_button()
    # Check if the user is authenticated
    if 'authentication_status' in st.session_state and st.session_state['authentication_status'] == 'Authenticated':
        # Get the username of the currently logged-in user
        username = st.session_state.get('username', 'Guest')
        st.header(f"Hi {username}👋, What folder or do you want to monitor?")

        # Input field for directory path
        directory_path = st.text_input("Enter the directory path:")

        # Button to initiate monitoring
        if st.button("Add Path"):
            if os.path.isdir(directory_path) or os.path.isfile(directory_path):
                # Call function to insert monitored directory path into the database
                insert_monitored_path(directory_path, username)
                monitor_path(directory_path)
                st.success(f"Path {directory_path} Saved.")   
            else:
                st.error("Invalid directory path. Please enter a valid path.")
                
        # Display actively monitored paths for the currently logged-in user
        try:
            monitored_paths = get_monitored_paths(username)
            if monitored_paths:
                st.markdown("### :blue[Your Added Paths]")
                for idx, path in enumerate(monitored_paths, 1):
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.write(f"{idx}. {path}")
                    with col2:
                        if st.button("Start Monitoring", key=f"monitor_{idx}"):
                            # Start monitoring
                            monitor_path(directory_path)
                            st.success(f"Monitoring started for path: {idx}")
        except:
            pass
    else:
        # If the user is not authenticated, redirect them to the account page
        st.query_params["page"] = "account"
        st.warning("You need to log in to view this page.")
        if st.button("Go to Login"):
            # Update the session state to indicate that the login page should be shown
            st.session_state['show_login'] = True
            # Rerun the app to reflect the changes
            st.experimental_rerun()