import streamlit as st

question1 = "Are you here to buy insurance?"
question2 = "Great - what type of insurance are you looking for?"
question3 = "What date do you need insurance to be effective?"
question4 = "What is the reason you are purchasing insurance?"
question5 = "What is the name of your business?"
question6 = "This is what we found about your business. Does this look correct?"
question7 = "Great! Please provide an email address and password to create your account."
question8 = "Excellent! A link will be emailed/texted to you so you can complete your application later."

options1 = ["Yes", "No"]
options2 = ["General Liability", "Contents", "Contents and Building", "Building Only"]
options3 = ["ASAP", "Specific Date"]
options4 = ["Purchase building", "New purchase", "Expiration of policy", "Starting new business", "Other"]

# Initialize session state
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
    st.session_state.messages = [{"role": "assistant", "content": question1}]
    st.session_state.responses = {}

# Set Chat
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(name=message['role']):
            st.markdown(message['content'])

# Prompt container logic
def update_messages(user_message, assistant_message):
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    st.session_state.current_step += 1
    st.rerun()

if st.session_state.current_step == 1:
    prompt_container = st.empty()
    with prompt_container.container():
        if st.button("Yes"):
            st.session_state.responses["response1"] = "Yes"
            update_messages("Yes", question2)
        elif st.button("No"):
            st.session_state.responses["response1"] = "No"
            update_messages("No", "Please come back if you would like to buy insurance.")
            st.session_state.current_step = 8

elif st.session_state.current_step == 2:
    prompt_container = st.empty()
    with prompt_container.container():
        selectbox_type = st.selectbox("Select from the list:", options=options2, index=None)
        if st.button("Submit"):
            st.session_state.responses["response2"] = selectbox_type
            update_messages(selectbox_type, question3)

elif st.session_state.current_step == 3:
    prompt_container = st.empty()
    with prompt_container.container():
        if st.button("ASAP"):
            st.session_state.responses["response3"] = "ASAP"
            update_messages("ASAP", question4)
        elif st.button("Specific Date"):
            effectivedate = st.date_input("Select desired effective date:")
            if st.button("Submit Date"):
                st.session_state.responses["response3"] = effectivedate.strftime('%Y-%m-%d')
                update_messages(effectivedate.strftime('%Y-%m-%d'), question4)

elif st.session_state.current_step == 4:
    prompt_container = st.empty()
    with prompt_container.container():
        reasonselect = st.selectbox("Select reason below:", options=options4, index=None)
        if st.button("Submit"):
            st.session_state.responses["response4"] = reasonselect
            update_messages(reasonselect, question5)

elif st.session_state.current_step == 5:
    prompt_container = st.empty()
    with prompt_container.container():
        chatinput = st.chat_input("Enter name of business here")
        if chatinput:
            st.session_state.responses["response5"] = chatinput
            update_messages(chatinput, question6)

elif st.session_state.current_step == 6:
    st.session_state.messages.append({"role": "assistant", "content": question7})
    st.session_state.current_step = 7
    st.rerun()

elif st.session_state.current_step == 7:
    prompt_container = st.empty()
    with prompt_container.container():
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            st.session_state.responses["response6"] = email
            st.session_state.responses["response7"] = password
            update_messages(f"Email: {email}", question8)

elif st.session_state.current_step == 8:
    st.session_state.messages.append({"role": "assistant", "content": "Thank you! A link will be emailed/texted to you so you can complete your application later."})
    st.session_state.current_step = None
    st.experimental_rerun()
