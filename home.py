import streamlit as st
import os
from utils.components import (
    changed_files, create_hashfile, deleted_files,
    find_files, generate_md5, new_files, read_file
)
from utils.send_email import send_email
from utils.show_button import show_logout_button
import sqlite3
import time
from threading import Thread, Event


# Initialize SQLite database connection
conn = sqlite3.connect('hostguard.db', check_same_thread=False)
c = conn.cursor()

# Initialize a dictionary to store active monitoring threads
active_threads = {}

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
    # If the path is unique, insert it into the database
    # Check if the directory path already exists
    c.execute("SELECT * FROM file_monitoring WHERE directory_path = ? AND username = ?", (directory_path, username))
    existing_path = c.fetchone()
    if existing_path:
        st.warning("This directory path is already being monitored.")
        return
    
    c.execute("INSERT INTO file_monitoring (directory_path, username) VALUES (?, ?)", (directory_path, username))
    conn.commit()
    
# Function to retrieve monitored paths for a specific user
def get_monitored_paths(username):
    c.execute("SELECT directory_path FROM file_monitoring WHERE username=?", (username,))
    monitored_paths = c.fetchall()
    return [path[0] for path in monitored_paths]

# Function to monitor the path
def monitor_path(email, directory_path, stop_event):
    # Replace '/' and '\' characters in directory_path with '_'
    filename = directory_path.replace('/', '_').replace('\\', '_')
    
    while not stop_event.is_set():
        found_files = find_files(directory_path)
        var_generate_md5 = generate_md5(found_files)
        create_hashfile(directory_path, found_files, var_generate_md5)
        
        if os.path.exists(f"{filename}_0.txt") and os.path.exists(f"{filename}_1.txt"):
            old_file = read_file(f"{filename}_1.txt")
            new_file = read_file(f"{filename}_0.txt")
            
            var_changed_files = changed_files(old_file, new_file)
            var_deleted_files = deleted_files(old_file, new_file)
            var_new_files = new_files(old_file, new_file)
            
            if var_changed_files != [] or var_deleted_files != [] or var_new_files != []:
                email_subject = "HostGuard Report: Changes Detected"
                email_message = f"Changes were detected in the monitored directory {directory_path}:\n\n"
                email_message += "NEW FILES\n"
                email_message += "---------\n"
                for file in var_new_files:
                    email_message += file + "\n"

                email_message += "\nCHANGED FILES\n"
                email_message += "-------------\n"
                for file in var_changed_files:
                    email_message += file + "\n"

                email_message += "\nREMOVED FILES\n"
                email_message += "-------------\n"
                for file in var_deleted_files:
                    email_message += file + "\n"

                # Send the email
                try:
                    send_email(email, email_subject, email_message)
                except Exception as e:
                    print(f"Didn't send see error ==> {e}")
                    
        # Wait for 2 minutes before checking again
        time.sleep(10)

def app():
    show_logout_button()
    create_file_monitoring_table()
    # Check if the user is authenticated
    if 'authentication_status' in st.session_state and st.session_state['authentication_status'] == 'Authenticated':
        # Get the username of the currently logged-in user
        username = st.session_state.get('username', 'Guest')
        email = st.session_state.get('email', 'tester@gmail.com')
        st.header(f"Hi {username}👋, What folder or do you want to monitor?")

        # Input field for directory path
        directory_path = st.text_input("Enter the directory path:")

        # Button to initiate monitoring
        if st.button("Add Path"):
            if os.path.isdir(directory_path) or os.path.isfile(directory_path):
                # Call function to insert monitored directory path into the database
                insert_monitored_path(directory_path, username)
                # monitor_path(email, directory_path, stop_event)
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
                            stop_event = Event()
                            active_threads[path] = stop_event
                            Thread(target=monitor_path, args=(email, path, stop_event)).start()   
                            st.success(f"Path {idx} is being monitored.")  
                            
                # Check if there are active monitoring threads
                if active_threads:
                    if st.button("Stop Monitoring"):
                        st.write("You have an actively running process/es. Do you want to stop all?")
                        for stop_event in active_threads.values():
                            stop_event.set()
                            del stop_event
                        active_threads.clear()
                        st.success("All monitoring processes stopped successfully.")         
        except Exception as e:
            print(e)
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