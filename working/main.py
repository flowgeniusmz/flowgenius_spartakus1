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

# Function to handle user input and update session state
def handle_user_input(current_step, user_input):
    st.session_state.responses[current_step] = user_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    next_step = current_step + 1
    if next_step < len(steps):
        if "conditional" in steps[next_step] and st.session_state.responses[current_step] != "Yes":
            next_step += 1
        st.session_state.current_step = next_step
        st.session_state.messages.append({"role": "assistant", "content": steps[next_step]["question"]})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "Thank you! A link will be emailed/texted to you so you can complete your application later."})
        st.session_state.current_step = None

# Display chat messages
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": steps[0]["question"]})

display_chat_messages()

# Restart the process
if st.button("Start Over"):
    st.session_state.current_step = 0
    st.session_state.responses = {}
    st.session_state.messages = [{"role": "assistant", "content": steps[0]["question"]}]

# Display the current question and get user input
current_step = st.session_state.current_step
if current_step is not None:
    step = steps[current_step]
    if step["options"]:
        response = st.selectbox(step["question"], step["options"], key=f"step_{current_step}")
    else:
        response = st.text_input(step["question"], key=f"step_{current_step}")

    if st.button("Submit"):
        if response:
            handle_user_input(current_step, response)

    # Allow users to go back to the previous step
    if current_step > 0 and st.button("Previous"):
        st.session_state.current_step -= 1
        st.session_state.messages.pop()  # Remove the current question
        st.session_state.messages.pop()  # Remove the user's last answer

# Display user responses at the end
if st.session_state.current_step is None:
    st.write("User responses:")
    for step, response in st.session_state.responses.items():
        st.write(f"Q{step + 1}: {steps[step]['question']} - {response}")
