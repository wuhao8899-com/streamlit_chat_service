import streamlit as st
from langchain_openai import ChatOpenAI
# 调用方式（使用 LCEL 语法或直接构造 messages）
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

st.title('🦜🔗 动手学大模型应用开发')
#输入密码
api_key = st.sidebar.text_input('OpenAI API Key', type ='password')

if 'history' not in st.session_state:
    st.session_state['history'] = []
# 根据大模型回答问题
def getResponse(text):
    try:
        llm = ChatOpenAI(
            openai_api_key = api_key,  # 你的密钥
            openai_api_base ="https://api.gptsapi.net/v1",  # 自定义 API 地址
            model_name ='gpt-4-turbo'  # 根据你的服务商支持的模型名称调整
        )
        response = llm.invoke(
            [SystemMessage(content='你是一个智能回答助手，可以帮助回答问题'),
            HumanMessage(content=text)
        ])
        output_parser = StrOutputParser()
        str = output_parser.invoke(response)
        temp = {}
        temp["user"] = text
        temp["assistant"] = str
        st.session_state.history.append(temp)
        for data in  st.session_state.history:
            str1 = data["user"]
            messages.chat_message("user").write(str1)

            str2 = data["assistant"]
            messages.chat_message("assistant").write(str2)

    except Exception as e:
        st.warning('检查你的key配置', icon='⚠')

# 对话消息框
messages = st.container(height=300)
prompt = st.chat_input("Say something", key="user_input")
if prompt:
    if not api_key:
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    elif not api_key.startswith('sk-'):
        st.warning('检查你的拼写', icon='⚠')
    else:
        str = getResponse(prompt)


