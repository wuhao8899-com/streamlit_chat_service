import streamlit as st
import os
import sys
import re
from langchain_openai import ChatOpenAI
# 调用方式（使用 LCEL 语法或直接构造 messages）
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from embedding.zhipuai_embedding import ZhipuAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv, find_dotenv
from langchain.chains import ConversationalRetrievalChain
from memory_module import memory

_ = load_dotenv(find_dotenv())
st.title('🦜🔗 动手学大模型应用开发')
#输入密码
api_key = st.sidebar.text_input('OpenAI API Key', type ='password')
# 历史聊天记录存储
if 'history' not in st.session_state:
    st.session_state['history'] = []
# langchain自动的存储
if 'memory' not in st.session_state:
    st.session_state['memory'] = memory
# 选择哪种应答的模式
selected_method = st.radio(
        "你想选择哪种模式进行对话？",
        ["None", "qa_chain", "chat_qa_chain"],
        captions 
= ["不使用检索问答的普通模式", "不带历史记录的检索问答模式", "带历史记录的检索问答模式"])
# 获得大语言模型
# def getllm(fun):
#     try:
#         llm = ChatOpenAI(
#             openai_api_key = api_key,  # 你的密钥
#             openai_api_base ="https://api.gptsapi.net/v1",  # 自定义 API 地址
#             model_name ='gpt-4-turbo',  # 根据你的服务商支持的模型名称调整
#             temperature = 0
#         )

#     except Exception as e:
#         st.warning("检查你的api_key")
# 用于显示
def showStr():
    for data in  st.session_state.history:
        str1 = data["user"]
        messages.chat_message("user").write(str1)
        str2 = data["assistant"]
        messages.chat_message("assistant").write(str2)
# 获得向量的数据库
def getVectordb():
    # 加载向量数据库
    embedding = ZhipuAIEmbeddings()
    persist_directory = "D:\\code_project/knowledge_db/chroma_db" # 数据库存储路径
    # 准备好向量的数据库
    vectordb = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )
    return vectordb
# 单次的问答链,带检索
def getAskByTemple(text, llm):
    vectordb = getVectordb()
    # 这里的context我们不需要管，lanchain会去数据库索引到相关的context填入
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    """
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                    template=template)
    # 数据库的数据来源
    retriever= vectordb.as_retriever()
    #这是一个问答链
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever = retriever ,
        return_source_documents= True,
        chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
    result = qa_chain({"query": text})
    temp = {}
    temp["user"] = text
    temp["assistant"] = result['result']
    st.session_state.history.append(temp)
    showStr()
# 直接的问答
def getResponseByNone(text, llm):
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
    showStr()
# 直接的问答
def getResponseByChain_memory(text, llm):
    vectordb = getVectordb()
    # 数据库的数据来源
    retriever= vectordb.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever= retriever,
        memory= st.session_state.memory)
    result = qa({"question": text})
    temp = {}
    temp["user"] = text
    temp["assistant"] = result["answer"]
    st.session_state.history.append(temp)
    showStr()
# 对话消息框
messages = st.container(height=300)
prompt = st.chat_input("Say something", key="user_input")

callback_method = {
    "None":getResponseByNone,
    "qa_chain":getAskByTemple,
    "chat_qa_chain":getResponseByChain_memory,
}

if prompt:
    if not api_key:
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    elif not api_key.startswith('sk-'):
        st.warning('检查你的拼写', icon='⚠')
    else:
        try:
            llm = ChatOpenAI(
                openai_api_key = api_key,  # 你的密钥
                openai_api_base ="https://api.gptsapi.net/v1",  # 自定义 API 地址
                model_name ='gpt-4-turbo',  # 根据你的服务商支持的模型名称调整
                temperature = 0
            )
            test_prompt = "Hello, how are you?"
            response = llm.invoke(test_prompt)
            if response:
                print("llm 初始化成功并可以正常工作！")
                callback_method.get(selected_method, getAskByTemple)(prompt, llm)
            else:
                print("检查你的api去")
        except Exception as e:
            st.warning("检查你的api_key")
        