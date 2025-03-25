from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from langchain_core.documents import Document


import os
pdf_path = "D:\\code_project/knowledge_db/pumkin_book/pumpkin_book.pdf"
# current_directory = os.getcwd()

# 检查文件是否存在
# if os.path.exists(pdf_path):
#     loader = PyMuPDFLoader(pdf_path)
#     pages = loader.load()
#     print(pages)
#     # pdf_page = pages[1]
#     # print(f"每一个元素的类型：{type(pdf_page)}.", 
#     #     f"该文档的描述性数据：{pdf_page.metadata}", 
#     #     # f"查看该文档的内容:\n{pdf_page.page_content}", 
#     #     sep="\n------\n")

# else:
#     print("文件不存在，请检查路径")

pdf_path = "D:\\code_project/knowledge_db/prompt_engineering/1. 简介 Introduction.md"
# 检查文件是否存在
if os.path.exists(pdf_path):
    loader = UnstructuredMarkdownLoader(pdf_path)
    pages = loader.load()
    print(pages[0])

else:
    print("文件不存在，请检查路径")
