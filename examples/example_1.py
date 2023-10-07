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


from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

from langchain_plantuml import diagram
from dotenv import load_dotenv

load_dotenv()
template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

activity_diagram = diagram.activity_diagram_callback(note_max_length=2000)
sequence_diagram = diagram.sequence_diagram_callback(note_max_length=2000)

llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=memory,
    callbacks=[activity_diagram, sequence_diagram]
)

try:
    llm_chain.predict(human_input="What did biden say about ketanji brown jackson in the state of the union address?")
finally:
    activity_diagram.save_uml_content("example_1_activity-plantuml.puml")
    sequence_diagram.save_uml_content("example_1_sequence-plantuml.puml")
