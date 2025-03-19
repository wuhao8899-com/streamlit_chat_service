from langchain_openai import ChatOpenAI
# 调用方式（使用 LCEL 语法或直接构造 messages）
from langchain_core.messages import HumanMessage

# 同时指定 api_key 和 base_url
llm = ChatOpenAI(
    openai_api_key="sk-NNT0fd5cc4814d18b0c81bab0fd838b7ea542466119qPmKM",  # 你的密钥
    openai_api_base="https://api.gptsapi.net/v1",  # 自定义 API 地址
    model_name='gpt-4'  # 根据你的服务商支持的模型名称调整
)


response = llm.invoke([
    HumanMessage(content="请问你是chatgpt几")
])
print(response.content)

