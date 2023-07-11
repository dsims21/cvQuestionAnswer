import streamlit as st
import openai

openai_api_key=st.secrets["OPENAI_API_KEY"]
with open("public/resume.txt", "r") as f:
    baseResume = f.read()

st.title("ResumeGPT")
st.text("Engage in an AI-powered conversation to explore Daniel's career.") 
st.text("Your conversation is private to your session.")

openai.api_key = openai_api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.messages.append({"role": "system", "content": "You are a powerful chatbot. Do not make up information. You are designed to answer questions about this document: " + baseResume})

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        

prompt = st.chat_input("Ask ResumeGPT about Daniel.")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages = st.session_state.messages[-5:]
    del st.session_state.messages[0]
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages if m["role"]
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "") # type: ignore
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response) # Assistant's response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    full_response = full_response[32000-len(full_response):]