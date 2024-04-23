import streamlit as st
from streamlit_option_menu import option_menu
import home, account, about

st.set_page_config(
        page_title="HostGuard",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:        
            app = option_menu(
                menu_title='HostGuard ',
                options=['Home','Account','About'],
                icons=['house-fill','person-circle','trophy-fill'],
                menu_icon='shield',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        if app == "Home":
            home.app()
        if app == "Account":
            account.app()    
        if app == 'About':
            about.app()    
                
    run()            
         
