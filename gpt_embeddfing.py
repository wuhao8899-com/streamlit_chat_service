import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def openai_embedding(text:str, model:str="text-embedding-3-large"):
    open_ai_key = os.getenv("OPENAI_API_KEY")
    Client = OpenAI(
        api_key = open_ai_key,
        base_url="https://api.gptsapi.net/v1",  
        # model = "t"
    )
    response = Client.embeddings.create(
        model= model,
        input=text,
    )
    return response
response  = openai_embedding(text = '要。')
# api返回json格式数据（object,data,型号model,使用的token数目（usage），）
# object是返回的embedding的类型
# print(response.object)
# print(response.data[0].object)
# print(response.model)
# print(len(response.data[0].embedding))
# print(response.usage)
# print(response.data[0].embedding[:10])



