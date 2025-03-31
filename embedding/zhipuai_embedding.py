from __future__ import annotations
import os
import logging
from typing import Any, Dict, List, Optional
from zhipuai import ZhipuAI
from langchain.embeddings.base import Embeddings
from pydantic import BaseModel, model_validator, ConfigDict
from langchain.utils import get_from_dict_or_env
logger = logging.getLogger(__name__)


class ZhipuAIEmbeddings(BaseModel, Embeddings):
    zhipuai_api_key: Optional[str] = None
    client: ZhipuAI = None  # 定义 client 字段
    model_config = ConfigDict(arbitrary_types_allowed=True)
    @model_validator(mode='after')
    def validate_environment(self) -> 'ZhipuAIEmbeddings':
        values = {
            "zhipuai_api_key": os.getenv("ZHIPUAI_API_KEY"),
            # 其他配置项可以从环境变量中加载
        }
        api_key = get_from_dict_or_env(
            values,
            "ZHIPUAI_API_KEY",
            "zhipuai_api_key",
        )
        if not api_key:
            raise ValueError(
                "ZHIPUAI_API_KEY not found. Please set it in your environment variables."
            )
        try:
            self.client = ZhipuAI(api_key=api_key)
        except ImportError:
            raise ValueError(
                "Zhipuai package not found, please install it with "
                "`pip install zhipuai`"
            )
        return self

    def _embed(self, texts: str) -> List[float]:
        # send request
        try:
            resp = self.client.embeddings.create(
                model="embedding-2",
                input=texts
            )
        except Exception as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")
        return resp.data[0].embedding

    def embed_query(self, text: str) -> List[float]:
        """
        Embedding a text.

        Args:

            Text (str): A text to be embedded.

        Return:

            List [float]: An embedding list of input text, which is a list of floating-point values.
        """
        embeddings = self.client.embeddings.create(
            model="embedding-2",
            input=text
        )
        return embeddings.data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of text documents.

        Args:
            texts (List[str]): A list of text documents to embed.

        Returns:
            List[List[float]]: A list of embeddings for each document in the input list.
                            Each embedding is represented as a list of float values.
        """
        return [self._embed(text) for text in texts]

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        raise NotImplementedError(
            "Please use `embed_documents`. Official does not support asynchronous requests")

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        raise NotImplementedError(
            "Please use `aembed_query`. Official does not support asynchronous requests")
