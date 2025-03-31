# 简单的rag系统
import os
import sys
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv, find_dotenv
from zhipuai import ZhipuAI
from langchain_core.prompts import PromptTemplate
from langchain.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from embedding.zhipuai_embedding import ZhipuAIEmbeddings

_ = load_dotenv(find_dotenv())

# 加载向量数据库
embedding = ZhipuAIEmbeddings()
persist_directory = "D:\\code_project/knowledge_db/chroma_db" # 数据库存储路径
# 准备好向量的数据库
vectordb = Chroma(
    embedding_function=embedding,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)

# 这是记忆功能
memory = ConversationBufferMemory(
    memory_key="chat_history",  # 与 prompt 的输入变量保持一致。
    return_messages=True  # 将以消息列表的形式返回聊天记录，而不是单个字符串
)
# 同时指定 api_key 和 base_url
llm = ChatOpenAI(
    openai_api_key="sk-NNT0fd5cc4814d18b0c81bab0fd838b7ea542466119qPmKM",  # 你的密钥
    openai_api_base="https://api.gptsapi.net/v1",  # 自定义 API 地址
    model_name='gpt-4-turbo',  # 根据你的服务商支持的模型名称调整
    temperature = 0
)

template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
{context}
问题: {question}
"""
# 这里的context我们不需要管，lanchain会去数据库索引到相关的context填入
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                 template=template)

# 数据库的数据来源
retriever=vectordb.as_retriever()
#这是一个问答链
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=retriever ,
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
# question_1 ="南瓜书"
# result = qa_chain({"query": question_1})
# 这是一个对话链，可以存储对话历史
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory
)
question = "我可以学习到关于提示工程的知识吗？"
result = qa({"question": question})
print(result['answer'])
print(memory)
print(memory)
print(memory)
# question = "为什么这门课需要教这方面的知识？"
# result = qa({"question": question})
# print(result['answer'])