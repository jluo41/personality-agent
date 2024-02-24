import streamlit as st
from prompt_template import SYSTEM_PROMPT
from openai import OpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

st.set_page_config(page_title="AI Chat", 
                   page_icon="🦙", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    model = st.text_input("model", value='gpt4')
    temperature = float(st.text_input("temperature", value=0))


model_to_apimodelname = {
    'gpt3.5': {'model': 'gpt-3.5-turbo-1106', 'openai_api_key': openai_api_key},
    'gpt4':   {'model': 'gpt-4-0125-preview', 'openai_api_key': openai_api_key},
}

st.title("哄哄哄模拟器 💬🦙")
st.info("模拟情侣吵架", icon="📃")

system_prompt = st.text_area("定义你自己的Agent", value = SYSTEM_PROMPT)
SYSTEM_MESSAGE = {'role': 'system', 'content': system_prompt}

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", 
         "content": "你好，我是哄哄哄模拟器，我会模拟情侣吵架。你可以输入你的问题，我会尽量帮你解决。"}
        # AIMessage(content = "你好，我是哄哄哄模拟器，我会模拟情侣吵架。你可以输入你的问题，我会尽量帮你解决。")
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("你的问题是什么？"): # Prompt for user input and save to chat history
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    para = model_to_apimodelname[model]
    chat = ChatOpenAI(temperature = temperature, **para)
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            messages = [SYSTEM_MESSAGE] + st.session_state.messages
            # print(messages)
            response = chat.invoke(messages).content
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)