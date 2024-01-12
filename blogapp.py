import streamlit as st 
from openai import OpenAI
import time 
import random 

client: OpenAI = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.title('Meeshi Blog Generator App')
# st.subheader('Hello Api Meeshi')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])


prompt: str = st.chat_input('say something')

if prompt:
    
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message('user'):
        st.markdown(prompt)

    



    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ' ' 

        for response in client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                # {"role":m['role'],"content":m['content']} for m in st.session_state.messages
                {"role":"system","content":"you are trainded analyze topic and generate the blog must contain 1550 wor ds to 3000 word not less then 1500"},
                {"role":"user","content":f"analyze the topic and generate a blog. the topic is {prompt}. the blog should contian the formate. 1-title (no more than one line) 2-introduction (give introduction about the topic) 3-add 2/3 subheading and explain them 4- body (should describe the fact and findings)"}
                ], 
                stream = True
            ):
                full_response += (response.choices[0].delta.content or " ")
                message_placeholder.markdown(full_response +"▌")
        
        message_placeholder.markdown(full_response)
    

    st.session_state.messages.append({"role":"assistant","content":full_response})


