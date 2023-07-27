from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

from langchain_plantuml import plantuml

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

callback_handler = plantuml.activity_diagram_callback()

llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=memory,
    callbacks=[callback_handler],
)

llm_chain.predict(human_input="Hi there my friend")
llm_chain.predict(human_input="Not too bad - how are you?")

plantuml_content = callback_handler.export_uml_content()
with open("example-activity-plantuml.puml", "w") as f:
    for line in plantuml_content:
        f.write(str(line) + "\n")
