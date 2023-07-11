import streamlit as st
import openai
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.vectorstores import Chroma
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain import OpenAI
# from langchain.chains import RetrievalQA
# from langchain.document_loaders import DirectoryLoader, TextLoader
# import magic
# import os
# import nltk

openai_api_key=st.secrets["OPENAI_API_KEY"]
with open("public/resume.txt", "r") as f:
    baseResume = f.read()

# Get your loader ready
# loader = DirectoryLoader('../data/PaulGrahamEssaySmall/', glob='**/*.txt')
# loader = TextLoader('public/test.txt')
# documents = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)
# embeddings = OpenAIEmbeddings()

# persist_directory = 'db'
# vectordb = Chroma.from_documents(persist_directory=persist_directory,embedding=embeddings, documents=texts)
# vectordb.persist()
# vectordb = None

# retriever = vectordb.as_retriever()
# docs = retriever.get_relevant_documents("What did McCarthy discover?")

# docsearch = FAISS.from_documents(texts, embeddings)
# llm = OpenAI(openai_api_key=openai_api_key)     
# qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())        
# query = "What did McCarthy discover?"
# qa.run(query)

st.title("ResumeGPT - Ask Anything About Daniel's CV")

openai.api_key = openai_api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.messages.append({"role": "system", "content": "You are a powerful chatbot designed to answer questions about this document: " + baseResume})

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        

prompt = st.chat_input("You can ask any question about Daniel...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    with st.chat_message("user"):
        st.markdown(prompt)

    # with st.chat_message("system"):
    #     st.markdown("You are a powerful chatbot designed to answer questions about this document: " + baseResume)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                # {"role": "system", "content": "You are a powerful chatbot designed to answer questions about this document: " + baseResume},
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
    st.session_state.messages = st.session_state.messages[-5:]