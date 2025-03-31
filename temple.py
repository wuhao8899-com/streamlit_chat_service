from langchain_openai import ChatOpenAI
# 调用方式（使用 LCEL 语法或直接构造 messages）
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate 

# 同时指定 api_key 和 base_url
llm = ChatOpenAI(
    openai_api_key="sk-NNT0fd5cc4814d18b0c81bab0fd838b7ea542466119qPmKM",  # 你的密钥
    openai_api_base="https://api.gptsapi.net/v1",  # 自定义 API 地址
    model_name='gpt-4-turbo'  # 根据你的服务商支持的模型名称调整
)
system_template = "你是一个翻译助手，可以帮助我将 {input_language} 翻译成 {output_language}"
# system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "{text}"
# human_message_prompt  = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([ ("system", system_template),
                                 
                                                 ("human", human_template)])
# text = "我带着比身体重的行李，游入尼罗河底，经过几道闪电 看到一堆光圈，不确定是不是这里。"
# messages  = chat_prompt.format_messages(input_language="中文", output_language="英文", text=text)

# output  = llm.invoke(messages)

output_parser = StrOutputParser()

chain = chat_prompt | llm | output_parser
text = "I carried luggage heavier than my body weight, diving into the depths of the Nile River. After passing through several flashes of lightning, I saw a cluster of halos, uncertain if this is the place"

result = chain.invoke({"input_language":"英文", "output_language":"中文","text": text})
# # 构建提示，填充占位符
# prompt = chat_prompt.format_prompt(topic="LLM").to_messages()

# llm = ChatOpenAI(
#     openai_api_key="sk-NNT0fd5cc4814d18b0c81bab0fd838b7ea542466119qPmKM",  # 你的密钥
#     openai_api_base="https://api.gptsapi.net/v1",  # 自定义 API 地址
#     model_name='gpt-4-turbo'  # 根据你的服务商支持的模型名称调整
# )

# output_parser = StrOutputParser()

# chain = chat_prompt | llm | output_parser
# print(chain)