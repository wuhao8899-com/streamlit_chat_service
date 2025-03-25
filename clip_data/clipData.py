import re
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter


# 知识库中单段文本长度
CHUNK_SIZE = 5
# 知识库中相邻文本重合长度
OVERLAP_SIZE = 2

pdf_path = "D:\\code_project/knowledge_db/prompt_engineering/1. 简介 Introduction.md"
# 检查文件是否存在
if os.path.exists(pdf_path):
    loader = UnstructuredMarkdownLoader(pdf_path)
    pages = loader.load()
    pdf_page = pages[0]
    #清洗数据
    pattern = re.compile(r'[^\u4e00-\u9fff](\n)[^\u4e00-\u9fff]', re.DOTALL)
    pdf_page.page_content = re.sub(pattern, lambda match: match.group(0).replace('\n', ''), pdf_page.page_content)
    text_splitter = CharacterTextSplitter(
        separator = " ",
        chunk_size = 10,
        chunk_overlap = 2,
    )
    # RecursiveCharacterTextSplitter:第一次按照字符区分割，如果超出chunk_size要求就继续按照separators递归分割，直到满足要求，然后考虑重叠问题。如果分出来的块小于chunk_size，那么块与块之间需要尝试合并，合并不了就拉倒，再考虑重叠问题。
    #核心：把递归做到极限，合并做到极限，重叠也做到极限，能做到啥程度就啥程度（就按照上述顺序来）
    # CharacterTextSplitter:第一次按照字符区分割，如果超出chunk_size要求就继续按照separators递归分割，直到满足要求，然后考虑重叠问题。如果分出来的块小于chunk_size，那么块与块之间需要尝试合并，合并不了就拉倒，再考虑重叠问题。
    #核心：合并做到极限，重叠也做到极限，能做到啥程度就啥程度（就按照上述顺序来）
    # TokenTextSplitter：我阐述一下你看对不对：假如我用的是RecursiveCharacterTextSplitter，那么它的标记数目只代表字符数，它的每块token数目可能还是会超过模型的限制大小，当我把RecursiveCharacterTextSplitter分割后的字符再进行TokenTextSplitter 分割，查阅资料，我可以限制它输出的最大标记数目也就是token数目，保证一定能让模型适应，还能保证一定的上下文联系和语义
    #MarkdownHeaderTextSplitter：可以把标题对应下内容做提取：用作标题的检索增强，上下文语义保留，注意格式问题（#跳到###分割会有问题，还有#前后有空格格式啥的，否则会解析失败）
# [
#     # {
#     #     "content": "监督学习需要标注数据。",
#     #     "metadata": {"header": "人工智能", "subheader": "机器学习"}
#     # },
#     # {
#     #     "content": "神经网络由多层组成。",
#     #     "metadata": {"header": "人工智能", "subheader": "深度学习"}
#     # }
# ]
# SentenceTransformersTokenTextSplitter ：保证与嵌入模型的兼容，切割更加保证语义和上下文，会按照段落和句子来切，甚至检索都可以用同一个模型
    str_str = "azb c d e f g h i j"
    split_docs = text_splitter.split_text(str_str)
    print(split_docs)


else:
    print("文件不存在，请检查路径")

