from zhipuai import ZhipuAI
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())
api_key = os.environ['ZHIPUAI_API_KEY']
def response2(text:str ,model:str = "embedding-2"):
    client=  ZhipuAI(
            api_key = api_key,
        )
    response = client.embeddings.create(
        model= model,
        input=text,
    )
    return response
# 具体结构和chatgpt的返回值一样
# print(response2("aaaa"))
