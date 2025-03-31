import streamlit as st
from langchain_openai import ChatOpenAI
# 调用方式（使用 LCEL 语法或直接构造 messages）
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

st.title('🦜🔗 动手学大模型应用开发')
#输入密码
api_key = st.sidebar.text_input('OpenAI API Key', type ='password')

# 根据大模型回答问题
def getResponse(text):
    llm = ChatOpenAI(
        openai_api_key = api_key,  # 你的密钥
        openai_api_base ="https://api.gptsapi.net/v1",  # 自定义 API 地址
        model_name ='gpt-4-turbo'  # 根据你的服务商支持的模型名称调整
    )
    try:
        response = llm.invoke(
            [SystemMessage(content='你是一个智能回答助手，可以帮助回答问题'),
            HumanMessage(content=text)
        ])
        output_parser = StrOutputParser()
        str = output_parser.invoke(response)
        try:
            st.info(str)
        except Exception as e:
            raise ValueError(
                "你的key是无效的的"
            )
    except Exception as e:
        st.warning('你的apikey无效', icon='⚠')


with st.form('my_form'):
    # 输入框
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    # 输入按钮配套
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not api_key:
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        elif not api_key.startswith('sk-'):
            st.warning('检查你的拼写', icon='⚠')
        else:
            getResponse(text)
    else:
        st.warning('没有输入openkey', icon='⚠')


