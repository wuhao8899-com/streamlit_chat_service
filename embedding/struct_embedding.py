import os
import sys
import re
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter 
from langchain.vectorstores.chroma import Chroma
from langchain.schema import Document
# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from embedding.zhipuai_embedding import ZhipuAIEmbeddings

_ = load_dotenv(find_dotenv())
pdf_path = "D:\\code_project/knowledge_db/"
file_tab = []
# 收集数据
for root, dirs, files in os.walk(pdf_path):
    for file in files:
        final_path = os.path.join(root, file)
        file_tab.append(final_path)   
# 收集数据函数
def get_from_dict_or_env(file_path):
        file_type = file_path.split('.')
        if file_type[1] == 'pdf':
            loader = PyMuPDFLoader(file_path)
            return loader
        elif file_type[1] == 'md':
            loader = UnstructuredMarkdownLoader(file_path)
            return loader
 
# 收集加载后的文档
document_tab = []
for file_path in file_tab:
    # 最终文件
    page_content = get_from_dict_or_env(file_path)
    if page_content:
        document_tab.extend(page_content.load())
        
#数据清洗 #数据分块
text_splitter = RecursiveCharacterTextSplitter (
    chunk_size = 1000,
    chunk_overlap = 100,
)
split_docs_tab = []
for doc in document_tab:
    pattern = re.compile(r'[^\u4e00-\u9fff](\n)[^\u4e00-\u9fff]', re.DOTALL)
    doc.page_content = re.sub(pattern, lambda match: match.group(0).replace('\n', ''), doc.page_content)
    doc.page_content = doc.page_content.replace('•', '')
    doc.page_content = doc.page_content.replace(' ', '')
    doc.page_content = doc.page_content.replace('\n\n', '\n')
    document = Document(page_content=doc.page_content, metadata=doc.metadata)
        # 检查是否是 Document 类型
    if not isinstance(document, Document):
        raise ValueError("doc 不是 Document 类型")
    else:
        split_docs = text_splitter.split_documents([document])
        split_docs_tab.extend(split_docs)
    persist_directory = "D:\\code_project/knowledge_db/chroma_db" # 数据库存储路径
# 构建向量数据库
embedding = ZhipuAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=split_docs_tab, # 为了速度，只选择前 20 个切分的 doc 进行生成；使用千帆时因QPS限制，建议选择前 5 个doc
    embedding=embedding,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)

# question="南瓜书"

# sim_docs = vectordb.similarity_search(question,k=5)
# # print(f"检索到的内容数：{len(sim_docs)}")
# # print(enumerate(sim_docs))
# for i, sim_doc in enumerate(sim_docs):
#     print(sim_doc.page_content)