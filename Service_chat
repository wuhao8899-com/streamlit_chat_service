import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

# 配置OpenAI密钥
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# 初始化聊天模型
@st.cache_resource
def load_chain():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500
    )

llm = load_chain()

# 构建聊天界面
st.title("🤖 智能客服系统")
st.caption("基于 LangChain + Streamlit 构建")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(SystemMessage(content="你是一个专业客服助手，用中文友好回答问题"))

# 显示历史消息
for msg in st.session_state.messages[1:]:  # 跳过系统提示
    with st.chat_message("assistant" if msg.type == "system" else "user"):
        st.markdown(msg.content)

# 处理用户输入
if prompt := st.chat_input("请输入您的问题"):
    # 添加用户消息
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成回复
    with st.chat_message("assistant"):
        response = llm(st.session_state.messages)
        st.markdown(response.content)
        st.session_state.messages.append(response)
