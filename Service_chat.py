from langchain_openai import ChatOpenAI
# 调用方式（使用 LCEL 语法或直接构造 messages）
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
# 同时指定 api_key 和 base_url
llm = ChatOpenAI(
    openai_api_key="sk-NNT0fd5cc4814d18b0c81bab0fd838b7ea542466119qPmKM",  # 你的密钥
    openai_api_base="https://api.gptsapi.net/v1",  # 自定义 API 地址
    model_name='gpt-4-turbo'  # 根据你的服务商支持的模型名称调整
)

response = llm.invoke(
    [SystemMessage(content='你是一个翻译助手，可以帮助我将 中文 翻译成 英文.'),
    HumanMessage(content='我带着比身体重的行李，游入尼罗河底，经过几道闪电 看到一堆光圈，不确定是不是这里。')
])

output_parser = StrOutputParser()
aaa= output_parser.invoke(response)


