import re
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

pdf_path = "D:\\code_project/knowledge_db/prompt_engineering/1. 简介 Introduction.md"
# 检查文件是否存在
if os.path.exists(pdf_path):
    loader = UnstructuredMarkdownLoader(pdf_path)
    pages = loader.load()
    pdf_page = pages[0]
    print(pdf_page.page_content)
    #清洗数据
    pattern = re.compile(r'[^\u4e00-\u9fff](\n)[^\u4e00-\u9fff]', re.DOTALL)
    pdf_page.page_content = re.sub(pattern, lambda match: match.group(0).replace('\n', ''), pdf_page.page_content)
    # pdf_page.page_content = pdf_page.page_content.replace('•', '')
    # pdf_page.page_content = pdf_page.page_content.replace(' ', '')
    # pdf_page.page_content = pdf_page.page_content.replace('\n\n', '\n')
    # print(pdf_page.page_content)

else:
    print("文件不存在，请检查路径")

