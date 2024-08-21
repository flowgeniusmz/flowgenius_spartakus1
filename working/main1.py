import streamlit as st

# Initialize session state
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
    st.session_state.responses = {}
    st.session_state.messages = []

# Define the steps and their corresponding options
steps = [
    {"question": "Are you here to buy insurance?", "options": ["Yes", "No"]},
    {"question": "What type of insurance are you interested in?", "options": ["General liability", "Contents", "Contents and Building", "Building only"], "conditional": True},
    {"question": "What date do you need insurance to be effective?", "options": ["ASAP", "Specific date"]},
    {"question": "Reason behind purchasing insurance", "options": ["Purchase building", "New purchase", "Expiration of policy", "Starting new business", "Other"]},
    {"question": "What is the name of your Business?", "options": []},
    {"question": "AI Assistant - Please provide the following information", "options": ["Date of formation", "Address", "Ownership", "Website URL"]}
]


# Function to display chat messages
def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Set Inital Display

chat_container = st.container(border=True)
prompt_container = st.container(border=True)
with prompt_container:
    prompt = st.chat_input(placeholder="Please enter your responses here.")