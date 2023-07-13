# Copyright 2023 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import List

from langchain.agents import initialize_agent, AgentType
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import Tool
from langchain.vectorstores import Chroma

from langchain_plantuml.core.plantuml_callback_handler import BasePlantUMLCallbackHandler


class SceneAgent:
    def __init__(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613")

        """Create the state_of_union Vectorstore"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        doc_path = os.path.join(current_path, 'data/state_of_the_union.txt')
        loader = TextLoader(doc_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings, collection_name="state-of-union")
        state_of_union = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
        )

        """Create the ruff Vectorstore"""
        loader = WebBaseLoader("https://beta.ruff.rs/docs/faq/")
        docs = loader.load()
        ruff_texts = text_splitter.split_documents(docs)
        ruff_db = Chroma.from_documents(ruff_texts, embeddings, collection_name="ruff")
        ruff = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=ruff_db.as_retriever()
        )

        """Create the Agent"""
        tools = [
            Tool(
                name="State of Union QA System",
                func=state_of_union.run,
                description="useful for when you need to answer questions about the most recent state of the union address. Input should be a fully formed question.",
            ),
            Tool(
                name="Ruff QA System",
                func=ruff.run,
                description="useful for when you need to answer questions about ruff (a python linter). Input should be a fully formed question.",
            )
        ]
        self.agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )

    def run(self, question: str, callbacks: List[BasePlantUMLCallbackHandler]):
        self.agent.run(question, callbacks=callbacks)
