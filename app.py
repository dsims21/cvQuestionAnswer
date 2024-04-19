import streamlit as st
import openai
import mysql.connector
from datetime import datetime

openai_api_key=st.secrets["OPENAI_API_KEY"]

# MySQL connection details
db_host = st.secrets["DB_HOST"]
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASS"]
db_name = st.secrets["DB_NAME"]

with open("public/resume.txt", "r") as f:
    baseResume = f.read()

st.title("ResumeGPT")
st.write("Engage in an AI-powered conversation to explore Daniel's career. Your conversation is private to your session.") 

openai.api_key = openai_api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-0125-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.messages.append({"role": "system", "content": "You are a powerful chatbot designed to answer questions about this document: " + baseResume})

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        

prompt = st.chat_input("Ask ResumeGPT about Daniel.")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Establish a connection to the MySQL database
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        # Get the current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert the user's prompt into the MySQL database
        db_cursor = db_connection.cursor()
        insert_query = "INSERT INTO user_prompts (prompt, time) VALUES (%s, %s)"
        db_cursor.execute(insert_query, (prompt,))
        db_connection.commit()
        db_cursor.close()
        
        # Close the MySQL connection
        db_connection.close()
        
    except mysql.connector.Error:
        # Silently handle the error and proceed without notifying the user
        pass

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
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    full_response = full_response[32000-len(full_response):]
    st.markdown("   ") # Assistant's response
    st.markdown("   ") # Assistant's response
    st.markdown("   ") # Assistant's response
    st.markdown("   ") # Assistant's response
    st.markdown("   ") # Assistant's response
    st.markdown("   ") # Assistant's response